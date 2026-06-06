Legal Case Management System with Intelligent Case Report Analysis

About
A web application for lawyers to manage cases, clients, legal documents with AI summarization, and automatic email reminders for court hearings.

## 🚀 Features

### Core Features
- **Case Management** - Add, edit, delete, track cases
- **Client Management** - Manage client information
- **Document Analysis** - Upload PDFs, AI generates case summary
- **Calendar** - Schedule hearings with date/time
- **Email Reminders** - Automatic emails 2 hours before hearing
- **Dashboard** - Real-time statistics and analytics
- **Activities Log** - Track all system actions

### AI Document Summary Output
```
CASE TITLE: Ravi Kumar v. State of Karnataka
COURT: High Court of Karnataka
PARTIES: Complainant: Pradeep Sharma | Accused: Ravi Kumar
KEY FACTS: [Important facts from document]
DECISION: Accused convicted under Section 420 IPC
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Tailwind CSS |
| Backend | Django, Django REST Framework |
| AI | Google Gemini API |
| Database | SQLite |
| Email | Gmail SMTP |

## 📷 Screenshots

### Dashboard
![Dashboard](dashboard.png)

### Document Analysis with AI Summary
![Document Analysis](analysis.png)

### Calendar & Hearings
![Calendar](calendar.png)

### Email Reminder
![Email](email.png)

## 🔧 Installation

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 📧 Email Setup
Add to `backend/settings.py`:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 👨‍💻 Author
**Jayasri**
- GitHub: [@Jayasri123-ja](https://github.com/Jayasri123-ja)

## ⭐ Star this repo if you like it!
```

---

## 📸 **HOW TO ADD SCREENSHOTS**

1. Take screenshots of:
   - Dashboard page
   - Document Analysis page (with AI summary)
   - Calendar page
   - Email received

2. Save them as:
   - `dashboard.png`
   - `analysis.png`
   - `calendar.png`
   - `email.png`

3. On GitHub, click **"Add file"** → **"Upload files"**

4. Drag all 4 images




