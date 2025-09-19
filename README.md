# Temper-Serve

Temper Server is a lightweight local userscript server designed to simplify and streamline userscript development. It hosts your scripts locally, making them easily accessible and automatically updateable through userscript extensions. With built-in version tracking, Temper Server ensures your scripts stay in sync and reliably update during development.

---

## ✨ Features

- ⚡ **Lightweight Local Server** – Run a minimal server optimized for userscript development.
- 📂 **Local Hosting** – Serve your userscripts directly from your machine.
- 🔄 **Automatic Updates on Sync** – Userscripts update automatically in supported extensions when you trigger a sync (e.g., by clicking “Update” in the extension).
- 📈 **Automatic Version Increment** – The `@version` field in your userscript updates whenever the file changes, ensuring extensions detect and fetch the latest version.
- 🛠️ **Development-Friendly** – Simplifies testing and iteration, reducing friction in userscript development.
- 🌐 **Extension Compatibility** – Works with popular userscript managers (e.g., Tampermonkey, Violentmonkey).

---

## 🛠️ Requirements

Before running Temper Server, ensure you have:

- **Python** 3.9+
- **pip** (Python package manager)
- A userscript manager extension installed in your browser, such as:
  - [Tampermonkey](https://www.tampermonkey.net/)
  - [Violentmonkey](https://violentmonkey.github.io/)
  - [Greasemonkey](https://www.greasespot.net/)

---

## ⚙️ Tech Stack

Temper Server is built with:

- **Flask** – lightweight Python web framework to serve userscripts locally
- **Watchdog** – monitors file changes and triggers automatic updates
- **pip** – package management for Python dependencies

---

## 🚀 Running Temper Server

### 1. Clone the Repository

```bash
git clone https://github.com/ThoriqFathurrozi/temper-server.git
cd temper-server
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Linux / macOS
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run config.py to init config

```bash
python3 config.py
```

> 📌 **Note:** This is will create a config.ini file that u can store the configuration for temper server

### 5. Configure config.ini

Here’s a sample `config.ini` for Temper Server:

```ini
[Paths]
# Base directory for your project (root location of scripts or assets)
base_directory = /path/to/base

# Directory containing the userscripts you want to serve
target_directory = /path/to/target

[Server]
# Host address for the Flask server (use 0.0.0.0 for LAN access)
host = localhost

# Port number for the server (customize as needed)
port = 7000
```

### 6. Run/Start the server

```bash
python app.py

```

> ⚠️ **Important:** Always run the server with this command. Running it differently may prevent the Watchdog from detecting file changes properly.
> 🚀 Done! Your userscripts are now being served locally. 🌐 Open http://localhost:7000

### 7. Configure Base Userscript

To enable automatic versioning and updates through your userscript manager, ensure your script includes the correct `@updateURL` and `@downloadURL` fields pointing to your local server.

Example:

```javascript
// ==UserScript==
// @name         My Userscript
// @namespace    http://example.com/
// @version      0.1
// @description  Example userscript served from Temper Server
// @updateURL    http://localhost:7000/userscript.meta.js
// @downloadURL  http://localhost:7000/userscript.user.js
// @match        *://*/*
// @grant        none
// ==/UserScript==
```

> 📌 **Note:** If the .meta.js file does not exist in your target directory, Temper Server will automatically generate it when you run the server, based on your existing .user.js file.
> 🔄 This ensures that version tracking and update checks work seamlessly with Tampermonkey, Violentmonkey, and other managers.

### 8. Access & Install the Script

- 🌐 Open [http://localhost:7000](http://localhost:7000) in your browser to view the list of available userscripts.
- 📥 Click on a script (e.g., `myscript.user.js`) to open it in your userscript manager (Tampermonkey / Violentmonkey).

### 9. Trigger Updates During Development

Once your userscript is installed and configured:

1. Make changes to your `.user.js` file in your target directory.
2. Temper Server will automatically increment the `@version` in your script.
3. In your userscript manager (Tampermonkey, Violentmonkey, etc.):
   - Open the extension dashboard.
   - Click **Check for Updates** (or **Sync**) for the script.
   - The extension will fetch the new version from the `@updateURL` and update automatically.

> ⚡ Now you can start development with **auto version increment** + **sync-based updates**, ensuring your extension always stays up to date.
> 💡 **Tip:** This workflow lets you iterate quickly — edit locally, then sync in your extension with one click.

---

## 🔄 Development Workflow

```mermaid
flowchart TD
    A[Edit *.user.js] --> B[Temper Server detects changes<br/>and increments @version]
    B --> C[Userscript Manager<br/>(Tampermonkey / Violentmonkey)]
    C --> D[Click 'Check for Updates' / 'Sync']
    D --> E[Fetch from @updateURL<br/>and refresh script]

    style A fill:#f9f,stroke:#333,stroke-width:1px
    style B fill:#bbf,stroke:#333,stroke-width:1px
    style C fill:#bfb,stroke:#333,stroke-width:1px
    style D fill:#ffb,stroke:#333,stroke-width:1px
    style E fill:#fdd,stroke:#333,stroke-width:1px
```

---

## 🤝 Contribution

Contributions are welcome! 🎉

If you’d like to improve Temper Server, here’s how you can help:

1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/your-feature`)
3. **Commit** your changes (`git commit -m 'Add new feature'`)
4. **Push** to your branch (`git push origin feature/your-feature`)
5. **Open** a Pull Request

> 💡 Please make sure your code follows the existing style and includes relevant documentation or examples.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
