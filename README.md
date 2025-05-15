# ShareChat

**ShareChat** is a simple terminal-based tool that lets you share messages or files to your Google Chat space effortlessly — just using a single command. No switching apps, no pasting links manually!

---

## 🚀 Features

* Send instant messages to your Google Chat group.
* Upload and share files (e.g., images, scripts, documents) using GoFile.io.
* Automatically organizes files into dedicated folders: Images, Python files, and Others.
* Set up once and use with simple terminal commands from anywhere.

---

## 🛠️ Setup Instructions

### 1. Clone or Download the Repo

```bash
git clone https://github.com/yourusername/ShareChat.git
cd ShareChat
```

### 2. Run the Setup Script

```bash
bash setup.sh
```

The script will:

* Install the required Python library (`requests`).
* Prompt you to enter:

  * Your **Google Chat Webhook URL**
  * Your **GoFile.io API Token**
  * Folder IDs for: Image\_Files, Python\_Files, Other\_Files
* Automatically update your `~/.bashrc` with environment variables and helpful aliases.
* Reload your shell config so you can start using it immediately.

> 📌 Instructions will be shown step-by-step as you run the setup.

---

## ✅ Usage

After setup, use the following commands from any terminal directory:

### 📤 Send a Message:

```bash
sendtext "Hello, team! Quick update…"
```

### 📁 Share a File:

```bash
sendfile "/path/to/report.pdf"
```

Files are uploaded to your GoFile folders based on file type, and the download link is posted to your Google Chat group.

---

## 👨‍💻 Author

**Ram Bikkina**
📧 [rambikkina@yahoo.com](mailto:rambikkina@yahoo.com)

---

## 📃 License

MIT License. Use freely and improve it if you like ✨
