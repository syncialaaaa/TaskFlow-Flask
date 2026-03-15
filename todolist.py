import os
from functools import wraps

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFError, CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', '0') == '1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    task_lists = db.relationship('TaskList', backref='owner', lazy=True, cascade='all, delete-orphan')

class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='task_list', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    task_list_id = db.Column(db.Integer, db.ForeignKey('task_list.id'), nullable=False)

def is_logged_in():
    return 'user_id' in session


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not is_logged_in():
            flash('Veuillez vous connecter pour continuer.', 'warning')
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)

    return wrapped


def get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        return None
    return db.session.get(User, user_id)


def get_user_list_or_404(list_id):
    task_list = db.session.get(TaskList, list_id)
    if task_list is None:
        abort(404)
    if task_list.user_id != session.get('user_id'):
        abort(403)
    return task_list


def get_user_task_or_404(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    if task.task_list.user_id != session.get('user_id'):
        abort(403)
    return task

@app.context_processor
def inject_user():
    return dict(is_logged_in=is_logged_in)

@app.route('/')
@login_required
def index():
    user = get_current_user()
    if user is None:
        session.pop('user_id', None)
        flash('Session invalide, veuillez vous reconnecter.', 'warning')
        return redirect(url_for('login'))

    task_lists = TaskList.query.filter_by(user_id=user.id).order_by(TaskList.id.desc()).all()
    return render_template('index.html', user=user, task_lists=task_lists)

@app.route('/list/<int:list_id>')
@login_required
def view_list(list_id):
    task_list = get_user_list_or_404(list_id)
    tasks = Task.query.filter_by(task_list_id=task_list.id).order_by(Task.id.desc()).all()
    return render_template('list.html', task_list=task_list, tasks=tasks)

@app.route('/add_task/<int:list_id>', methods=['POST'])
@login_required
def add_task(list_id):
    task_list = get_user_list_or_404(list_id)
    title = request.form.get('title', '').strip()
    if not title:
        flash('Le titre de la tâche est obligatoire.', 'warning')
        return redirect(url_for('view_list', list_id=list_id))
    if len(title) > 100:
        flash('Le titre de la tâche doit faire 100 caractères max.', 'warning')
        return redirect(url_for('view_list', list_id=list_id))

    new_task = Task(title=title, task_list_id=task_list.id)
    db.session.add(new_task)
    db.session.commit()
    flash('Tâche ajoutée.', 'success')
    return redirect(url_for('view_list', list_id=list_id))


@app.route('/toggle_task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = get_user_task_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    flash('Statut de la tâche mis à jour.', 'success')
    return redirect(url_for('view_list', list_id=task.task_list_id))


@app.route('/remove_task/<int:task_id>', methods=['POST'])
@login_required
def remove_task(task_id):
    task = get_user_task_or_404(task_id)
    task_list_id = task.task_list_id
    db.session.delete(task)
    db.session.commit()
    flash('Tâche supprimée.', 'success')
    return redirect(url_for('view_list', list_id=task_list_id))

@app.route('/create_list', methods=['POST'])
@login_required
def create_list():
    list_name = request.form.get('list_name', '').strip()
    if not list_name:
        flash('Le nom de la liste est obligatoire.', 'warning')
        return redirect(url_for('index'))
    if len(list_name) > 100:
        flash('Le nom de la liste doit faire 100 caractères max.', 'warning')
        return redirect(url_for('index'))

    user = get_current_user()
    if user is None:
        session.pop('user_id', None)
        flash('Session invalide, veuillez vous reconnecter.', 'warning')
        return redirect(url_for('login'))

    new_list = TaskList(name=list_name, user_id=user.id)
    db.session.add(new_list)
    db.session.commit()
    flash('Liste créée.', 'success')
    return redirect(url_for('index'))

@app.route('/delete_list/<int:list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    task_list = get_user_list_or_404(list_id)
    db.session.delete(task_list)
    db.session.commit()
    flash('Liste supprimée.', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if len(username) < 3 or len(username) > 30:
            flash('Le nom utilisateur doit contenir entre 3 et 30 caractères.', 'warning')
            return render_template('register.html')

        if len(password) < 8:
            flash('Le mot de passe doit contenir au moins 8 caractères.', 'warning')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        if User.query.filter_by(username=username).first():
            flash('Ce nom utilisateur existe déjà.', 'warning')
            return render_template('register.html')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Compte créé avec succès. Vous pouvez vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Connexion réussie.', 'success')
            return redirect(url_for('index'))
        flash('Nom utilisateur ou mot de passe invalide.', 'danger')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('Déconnexion effectuée.', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden(_e):
    flash('Accès interdit à cette ressource.', 'danger')
    return redirect(url_for('index'))


@app.errorhandler(CSRFError)
def handle_csrf_error(_e):
    flash('Session expirée ou formulaire invalide. Veuillez réessayer.', 'danger')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1', port=3000)