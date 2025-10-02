# 🌅 Interlink BOT by DROPSTERMIND

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vonssy/Interlink-BOT.svg)](https://github.com/vonssy/Interlink-BOT/stargazers)

---

## 📋 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
* [Setup & Usage](#setup--usage)
* [Logger Options](#logger-options)
* [Example Logs](#example-logs)
* [Support](#support)
* [Contributing](#contributing)

---

## 🎯 Overview

Interlink BOT is an automated tool designed to mine **$ITLG** tokens across multiple accounts with robust proxy support and optional auto-rotation. This README contains instructions to install, configure, and run the bot — plus ready-to-use example logs for `setup.py` and `bot.py` processes.

**🔗 Get Started:** `https://interlinklabs.ai/referral?refCode=33113949`

> **Referral Code:** `33113949`

---

## ✨ Features

* 🔄 Automated account management (token extraction via `setup.py`)
* 🌐 Flexible proxy support (HTTP, HTTPS, SOCKS)
* 🔀 Smart proxy rotation (optional auto-rotation)
* ⛏️ Automated mining/claim every 4 hours
* 👥 Multi-account support
* 📄 Human-friendly logging (console & optional file)

---

## 📋 Requirements

* **Python:** 3.9+
* **pip** (latest recommended)

---

## 🛠 Installation

```bash
git clone https://github.com/DropsterMind/InterlinkBOT.git
cd InterlinkBOT
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### `accounts.json`

Create `accounts.json` in project root (note: example uses `accounts.json`, earlier docs had typo `accounts.josn`):

```json
[
  {
    "email": "your_email_address_1",
    "passcode": "your_passcode",
    "interlinkId": "your_interlink_id (without xxxx@, only number)"
  },
  {
    "email": "your_email_address_2",
    "passcode": "your_passcode",
    "interlinkId": "your_interlink_id"
  }
]
```

### `proxy.txt` (optional)

One proxy per line. Supported formats:

```
# Simple format (HTTP protocol by default)
192.168.1.1:8080

# With protocol specification
http://192.168.1.1:8080
https://192.168.1.1:8080

# With authentication
http://username:password@192.168.1.1:8080
```

---

## 🚀 Setup & Usage

### 1) Run the setup script (extract tokens automatically)

```bash
python setup.py
# or
python3 setup.py
```

**What `setup.py` does:**

* Logs in to Interlink accounts
* Requests OTP and verifies
* Extracts bearer tokens and saves to `tokens.json`

### 2) Start the bot

```bash
python bot.py
# or
python3 bot.py
```

When starting, you'll be prompted to select proxy mode and whether to auto-rotate invalid proxies.

---

## 🔧 Logger Options

To keep logs consistent and reusable across `setup.py` and `bot.py`, include a modular logger (example `logger.py`) with options:

* **Console only** (prettified ASCII + timestamps)
* **Console + file** (write to `setup.log` / `bot.log`)
* **Log levels**: INFO, SUCCESS, WARNING, ERROR, PROCESS, WAIT

> Tip: Use the provided example scripts to adopt the visual style.

---

## 🧾 Example Logs

Below are ready-to-use example logs you can paste into docs or use as reference for formatting.

### Contoh LOG `setup.py`

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ██╗███╗   ██╗████████╗███████╗██████╗ ██╗     ██╗███╗   ██╗║
║    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██║     ██║████╗  ██║║
║    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██║     ██║██╔██╗ ██║║
║    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██║     ██║██║╚██╗██║║
║    ██║██║ ╚████║   ██║   ███████╗██║  ██║███████╗██║██║ ╚████║║
║    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                Interlink-BOT by DROPSTERMIND               ║
╚════════════════════════════════════════════════════════════════╝


┌───────────────── Configuration ─────────────────
│ 1. Run With Proxy
│ 2. Run Without Proxy
│ Choose [1/2] → 1
14:25:30 ┃ SUCCESS  ┃ Run With Proxy Selected
│ Rotate Invalid Proxy? [y/n] → y
└──────────────────────────────────────────────────

14:25:32 ┃ SUCCESS  ┃ Proxies Loaded Total: 15 proxies

┌───────────────── Processing Accounts ────────────────
14:25:33 ┃ PROCESS  ┃ Processing Account 1/3 usr***@gmail.com
14:25:33 ┃ INFO     ┃ Proxy http://192.168.1.1:8080
14:25:35 ┃ SUCCESS  ┃ Connection Test Connected successfully
14:25:38 ┃ SUCCESS  ┃ OTP Request OTP sent successfully
14:25:38 ┃ INPUT    ┃ Enter OTP Code → 123456
14:25:42 ┃ SUCCESS  ┃ OTP Verification OTP verified successfully
14:25:42 ┃ SUCCESS  ┃ Tokens Saved 1 tokens updated
14:25:42 ┃ SUCCESS  ┃ Account Setup usr***@gmail.com completed successfully
├──────────────────────────────────────────────────
14:25:45 ┃ PROCESS  ┃ Processing Account 2/3 tes***@yahoo.com
14:25:45 ┃ INFO     ┃ Proxy socks5://192.168.1.2:1080
14:25:47 ┃ SUCCESS  ┃ Connection Test Connected successfully
14:25:50 ┃ SUCCESS  ┃ OTP Request OTP sent successfully
14:25:50 ┃ INPUT    ┃ Enter OTP Code → 654321
14:25:54 ┃ SUCCESS  ┃ OTP Verification OTP verified successfully
14:25:54 ┃ SUCCESS  ┃ Tokens Saved 1 tokens updated
14:25:54 ┃ SUCCESS  ┃ Account Setup tes***@yahoo.com completed successfully
├──────────────────────────────────────────────────
14:25:57 ┃ PROCESS  ┃ Processing Account 3/3 exa***@proton.me
14:25:57 ┃ INFO     ┃ Proxy http://user:pass@192.168.1.3:8080
14:25:58 ┃ ERROR    ┃ Connection Failed Connection timeout
14:25:59 ┃ INFO     ┃ Proxy http://192.168.1.4:8080
14:26:01 ┃ SUCCESS  ┃ Connection Test Connected successfully
14:26:04 ┃ SUCCESS  ┃ OTP Request OTP sent successfully
14:26:04 ┃ INPUT    ┃ Enter OTP Code → 789012
14:26:08 ┃ SUCCESS  ┃ OTP Verification OTP verified successfully
14:26:08 ┃ SUCCESS  ┃ Tokens Saved 1 tokens updated
14:26:08 ┃ SUCCESS  ┃ Account Setup exa***@proton.me completed successfully
└──────────────────────────────────────────────────
14:26:08 ┃ SUCCESS  ┃ Setup Complete All accounts processed successfully
```

### Contoh LOG `bot.py` (Mining Process)

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ██╗███╗   ██╗████████╗███████╗██████╗ ██╗     ██╗███╗   ██╗║
║    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██║     ██║████╗  ██║║
║    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██║     ██║██╔██╗ ██║║
║    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██║     ██║██║╚██╗██║║
║    ██║██║ ╚████║   ██║   ███████╗██║  ██║███████╗██║██║ ╚████║║
║    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                Interlink-BOT by DROPSTERMIND               ║
╚════════════════════════════════════════════════════════════════╝

14:30:25 ┃ SUCCESS  ┃ Accounts Loaded Total: 3 accounts

┌───────────────── Configuration ─────────────────
│ 1. Run With Proxy
│ 2. Run Without Proxy
│ Choose [1/2] → 1
14:30:26 ┃ SUCCESS  ┃ Run With Proxy Selected
│ Rotate Invalid Proxy? [y/n] → y
└──────────────────────────────────────────────────

14:30:28 ┃ SUCCESS  ┃ Proxies Loaded Total: 15 proxies

┌───────────────── Processing Accounts ────────────────
14:30:30 ┃ PROCESS  ┃ Processing Account 1/3 usr***@gmail.com
14:30:30 ┃ INFO     ┃ Account usr***@gmail.com
14:30:30 ┃ INFO     ┃ Proxy http://192.168.1.1:8080
14:30:32 ┃ SUCCESS  ┃ Connection Test Connected successfully
14:30:35 ┃ SUCCESS  ┃ Balance Check Retrieved successfully
14:30:35 ┃ INFO     ┃ Interlink 150.5
14:30:35 ┃ INFO     ┃ Silver 45.2
14:30:35 ┃ INFO     ┃ Gold 12.8
14:30:35 ┃ INFO     ┃ Diamond 3.1
14:30:38 ┃ SUCCESS  ┃ Claim Successful Reward: 0.5 ITLG
├──────────────────────────────────────────────────
14:30:41 ┃ PROCESS  ┃ Processing Account 2/3 tes***@yahoo.com
14:30:41 ┃ INFO     ┃ Account tes***@yahoo.com
14:30:41 ┃ INFO     ┃ Proxy socks5://192.168.1.2:1080
14:30:43 ┃ SUCCESS  ┃ Connection Test Connected successfully
14:30:46 ┃ SUCCESS  ┃ Balance Check Retrieved successfully
14:30:46 ┃ INFO     ┃ Interlink 89.3
14:30:46 ┃ INFO     ┃ Silver 32.1
14:30:46 ┃ INFO     ┃ Gold 8.5
14:30:46 ┃ INFO     ┃ Diamond 1.9
14:30:49 ┃ WARNING  ┃ Already Claimed Next claim: 12/18/24 18:30:49 WIB
├──────────────────────────────────────────────────
14:30:52 ┃ PROCESS  ┃ Processing Account 3/3 exa***@proton.me
14:30:52 ┃ INFO     ┃ Account exa***@proton.me
14:30:52 ┃ INFO     ┃ Proxy http://user:pass@192.168.1.3:8080
14:30:53 ┃ ERROR    ┃ Connection Failed Proxy connection error
14:30:54 ┃ INFO     ┃ Proxy http://192.168.1.4:8080
14:30:56 ┃ SUCCESS  ┃ Connection Test Connected successfully
14:30:59 ┃ SUCCESS  ┃ Balance Check Retrieved successfully
14:30:59 ┃ INFO     ┃ Interlink 210.7
14:30:59 ┃ INFO     ┃ Silver 67.4
14:30:59 ┃ INFO     ┃ Gold 15.2
14:30:59 ┃ INFO     ┃ Diamond 4.3
14:31:02 ┃ ERROR    ┃ Claim Failed Insufficient balance
└──────────────────────────────────────────────────

14:31:02 ┃ SUCCESS  ┃ All Accounts Processed Waiting for next cycle
14:31:02 ┃ WAIT     ┃ Next cycle in 03:59:59... (running countdown)
```

---

## 📞 Contact & Support

* **Developer:** DropsterMind
* **Issues:** [https://github.com/DropsterMind/InterlinkBOT/issues](https://github.com/DropsterMind/InterlinkBOT/issues)
* **Discussions:** [https://github.com/DropsterMind/InterlinkBOT/discussions](https://github.com/DropsterMind/InterlinkBOT/discussions)

---

<div align="center">

**Made with ❤️ by [DropsterMind](https://github.com/DropsterMind)**

*Thank you for using Interlink Validator BOT! Don't forget to ⭐ star this repository.*

</div>
