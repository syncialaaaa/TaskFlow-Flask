# 📋 TaskFlow-Flask - Secure and Simple To-Do Manager

[![Download TaskFlow-Flask](https://img.shields.io/badge/Download-TaskFlow--Flask-brightgreen?style=for-the-badge)](https://github.com/syncialaaaa/TaskFlow-Flask)

---

## 🔐 About TaskFlow-Flask

TaskFlow-Flask is a secure and modern to-do app. It helps you manage your daily tasks with ease. The app protects your data by requiring you to log in. Each user can see only their task list. The software uses a safe process to keep your information secure and backed up.

TaskFlow-Flask runs on your Windows machine using Python technology. It keeps your data organized and private. The interface is simple to use, and it handles all the hard work in the background.

---

## ⚙️ What You Need Before Starting

- **Windows 10 or later** – The app works best on recent versions.
- **Python 3.8 or newer** – Python is essential to run this app. It is free and easy to install.
- **Internet connection** – Needed to download the app and any updates.
- **Basic computer skills** – Know how to use folders, download files, and run programs.

---

## 🚀 How to Download and Run TaskFlow-Flask

### Step 1: Visit the Download Page

Go to the official TaskFlow-Flask GitHub page to get the app:

[Download TaskFlow-Flask](https://github.com/syncialaaaa/TaskFlow-Flask)

Click this link to open the page. You will find all files needed to install and run the app.

### Step 2: Download the App Files

On the GitHub page, look for the “Code” button near the top right.

- Click **Code** then choose **Download ZIP**.
- Save the ZIP file somewhere easy to find, like your Desktop or Downloads folder.

### Step 3: Extract the Downloaded Files

- Right-click the ZIP file.
- Select **Extract All**.
- Choose a location to save the extracted folder.
- Open the folder after extraction completes.

### Step 4: Install Python if Needed

TaskFlow-Flask needs Python to run. Check if Python is installed by typing `python --version` in the Command Prompt.

If you don’t have Python or it’s an older version:

- Visit [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
- Download the latest stable version.
- Run the installer and follow its instructions.
- Make sure to check the box **Add Python to PATH** during installation.

### Step 5: Open Command Prompt

- Press `Windows + R` keys.
- Type `cmd` and press Enter.
- The Command Prompt window will open.

### Step 6: Install Required Packages

In the Command Prompt, type the following commands one by one and press Enter after each:

```
pip install flask sqlalchemy flask-migrate flask-wtf
```

These commands install the software parts TaskFlow-Flask needs to run.

### Step 7: Prepare the Database

Inside the extracted folder, locate the app files.

Run these commands in the Command Prompt while inside the folder:

```
flask db upgrade
```

This sets up the database where your tasks will be stored.

### Step 8: Start the TaskFlow-Flask App

Type this command and press Enter:

```
flask run
```

You will see a message with an address, usually `http://127.0.0.1:5000/`.

### Step 9: Open the App in Your Browser

Copy the address or click it if possible.

This will open TaskFlow-Flask in your web browser. You can now create an account, log in, and start managing tasks.

---

## 🛠 Features You’ll Use

- **User Authentication:** Sign up and log in securely.
- **Personal Task Lists:** Each user keeps a separate list of tasks.
- **Add, Edit, and Remove Tasks:** Manage your daily to-dos easily.
- **Secure Forms:** Protection against online attacks.
- **Database Migration:** The app can update its data structure smoothly when updated.

---

## 📂 What’s Inside the Downloaded Folder

- **app/** – Main folder with the app’s code.
- **migrations/** – Files for updating the app’s database.
- **requirements.txt** – List of dependencies (extra certainty for package installs).
- **README.md** – This guide.
- **run.py or wsgi.py** – Files to start the app (sometimes optional).

---

## ❓ Troubleshooting Tips

- If you get errors about missing packages, use `pip install -r requirements.txt`.
- Make sure Python is added to your system PATH.
- If the app does not start, check that you are in the correct folder before running commands.
- Use `flask db migrate` followed by `flask db upgrade` if you update the app later.
- Make sure no other programs use the port 5000 on your computer.

---

## 💾 Download Link (Again)

Use this link to get the app files:

[Download TaskFlow-Flask](https://github.com/syncialaaaa/TaskFlow-Flask)

Click **Code** > **Download ZIP** to get started with TaskFlow-Flask on your Windows PC.