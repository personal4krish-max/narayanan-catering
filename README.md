# 🍽️ Narayanan's Catering Workforce Management System

A full-featured web application built with **Python + Streamlit + SQLite/MySQL** to digitize and automate catering workforce operations — from worker registration and event management to AI-based allocation, attendance tracking, and digital payments with **UPI QR Code** and **Credit/Debit Card** support.

---

## 🚀 Live Demo (Streamlit Cloud)

> Deploy to [share.streamlit.io](https://share.streamlit.io) — see **Cloud Deployment** section below.

**Demo Login Credentials:**
| Role    | Username / Phone | Password        |
|---------|-----------------|-----------------|
| Manager | `admin`         | `admin123`      |
| Worker  | `9000000001`    | `0001@wms`      |
| Worker  | `9000000005`    | `0005@wms`      |

---

## ⭐ Features

| Feature | Description |
|---------|-------------|
| 🔐 Auth | Secure login for managers and workers (phone or username) |
| 👥 Worker Mgmt | Add, edit, delete workers; track availability by skill |
| 🎉 Event Mgmt | Create events with worker slot requirements |
| 👷 Worker Allocation | Manual assignment + AI-based smart allocation |
| 📋 Leave Management | Workers apply for leave; managers approve/reject |
| ✅ Attendance | Record and report attendance per event |
| 💰 Payments | UPI QR code (dynamic, amount-based) + Credit/Debit card + Cash |
| 🤖 AI Agent | Rule-based scoring engine — skill + experience + attendance rate |
| 📊 Dashboard | KPIs, charts, quick actions |

---

## 💳 Payment Methods

### UPI (QR Code)
- Dynamic QR code generated per payment with exact amount pre-filled
- UPI ID: `9080599509@naviaxis`
- Compatible with GPay, PhonePe, Paytm, any UPI app

### Credit / Debit Card
- Full card form with live card-type detection (Visa, MasterCard, Amex, etc.)
- Visual animated card preview
- Luhn algorithm validation
- CVV & expiry verification

### Cash
- One-click cash payment confirmation with auto-generated transaction ID

---

## 📁 Project Structure

```
catering_wms/
├── app.py                        # Main entry point (login/register)
├── requirements.txt
├── schema.sql                    # MySQL schema for local use
├── .streamlit/
│   └── config.toml               # Theme & server config
├── modules/
│   ├── __init__.py
│   ├── database.py               # All DB operations (SQLite + MySQL)
│   ├── auth.py                   # Authentication utilities
│   ├── ai_agent.py               # Rule-based AI worker allocation
│   └── payment_utils.py          # UPI QR code + card utilities
└── pages/
    ├── 01_Manager_Dashboard.py
    ├── 02_Worker_Dashboard.py
    ├── 03_Worker_Management.py
    ├── 04_Event_Management.py
    ├── 05_Leave_Management.py
    ├── 06_Attendance.py
    ├── 07_Payments.py
    └── 08_AI_Allocation.py
```

---

## 🖥️ Local Setup (SQLite — Quick Start)

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone or extract the project
cd catering_wms

# 2. Create a virtual environment (recommended)
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**. The SQLite database (`catering_wms.db`) is created automatically on first run with demo data.

---

## 🛢️ Local Setup with MySQL

### Step 1 — Create the database

```bash
mysql -u root -p < schema.sql
```

Or run it manually in MySQL Workbench / phpMyAdmin.

### Step 2 — Set environment variables

**Windows (PowerShell):**
```powershell
$env:USE_MYSQL="true"
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_password"
$env:MYSQL_DATABASE="catering_wms"
```

**macOS/Linux (Terminal):**
```bash
export USE_MYSQL=true
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=catering_wms
```

### Step 3 — Run

```bash
streamlit run app.py
```

---

## ☁️ Streamlit Cloud Deployment

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit — Narayanan's Catering WMS"
git remote add origin https://github.com/YOUR_USERNAME/catering-wms.git
git push -u origin main
```

### Step 2 — Deploy on share.streamlit.io

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository
5. Set **Main file path** → `app.py`
6. Click **Deploy!**

> ✅ Streamlit Cloud uses SQLite by default — no database setup needed!

### Step 3 (Optional) — Add MySQL secrets on Streamlit Cloud

In your app dashboard → **Settings → Secrets**:

```toml
USE_MYSQL = "true"
MYSQL_HOST = "your-cloud-mysql-host"
MYSQL_USER = "your_user"
MYSQL_PASSWORD = "your_password"
MYSQL_DATABASE = "catering_wms"
```

---

## 🤖 AI Allocation Algorithm

The rule-based AI agent scores each worker using:

```
Score = Skill Weight + Experience Bonus + Attendance Rate

Skill Weight    : 1.0 (all skills), 1.2 (Supervisor)
Experience Bonus: min(years × 0.1, 1.0)
Attendance Rate : present/total (new workers default 0.8)
Conflict Check  : workers already on same date are excluded
Availability    : only is_available=1 workers considered
```

Workers are ranked by score descending. Auto-allocate picks top-N per skill slot.

---

## 🔐 Default Credentials

| Role    | Username | Password  |
|---------|----------|-----------|
| Manager | `admin`  | `admin123`|

Worker passwords: last 4 digits of phone + `@wms`  
Example: phone `9000000001` → password `0001@wms`

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `qrcode[pil]` | Dynamic UPI QR code generation |
| `Pillow` | Image processing for QR codes |
| `pandas` | Data tables |
| `plotly` | Charts & visualizations |
| `mysql-connector-python` | MySQL support (optional) |

---

## 📞 Support

System built for **Narayanan's Catering Services**  
UPI Payment ID: `9080599509@naviaxis`

---

*© 2025 Narayanan's Catering Workforce Management System*
