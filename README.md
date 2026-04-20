# PM2UI - PM2 Process Dashboard

PM2UI is a modern, lightweight, and fast cross-platform graphical user interface (GUI) for the popular Node.js process manager, [PM2](https://pm2.keymetrics.io/). Built with Python and PyQt6, it offers a strict, professional dashboard experience.

## Features

- **Process Management**: Start, Stop, Restart, Reload, Delete, and Reset Meta (restarts counter) for your processes with a single click.
- **Global Actions**: Easily Save your PM2 configuration (`pm2 save`) or Flush all logs (`pm2 flush`).
- **Real-time Monitoring**: The dashboard automatically updates every 2 seconds, providing live stats on Status, CPU, Memory, Uptime, and Restarts without flashing or losing your selection.
- **Log Viewer**: View the latest 100 lines of logs for any process in a built-in terminal-like window (cleaned of ANSI color codes for better readability).
- **Process Info**: Deep dive into the raw JSON data provided by PM2 for any selected process. Perfect for debugging hidden environment variables.
- **Telegram Error Monitoring (Optional)**: Get instant notifications in your Telegram when any of your PM2 processes throws an error.

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) & [PM2](https://pm2.keymetrics.io/) installed globally (`npm install -g pm2`)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Grobofhik/PM2UI.git
   cd PM2UI
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the application by running:
```bash
python main.py
```

### Setting up Telegram Error Monitoring
1. Open the application.
2. Click on the **Settings** button.
3. Check the box to enable Telegram logging.
4. Enter your Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather)).
5. Enter your Chat ID (get it from bots like [@userinfobot](https://t.me/userinfobot)).
6. Click **Save**. The application will now listen to `pm2 logs --err` and forward any errors directly to you.

*(Note: Your settings are securely saved locally in `settings.json` which is ignored by git).*
