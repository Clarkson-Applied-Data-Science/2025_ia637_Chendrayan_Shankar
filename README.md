# 🎓 Interfolio – Academic Workflow Management Platform

> A full-stack platform built to streamline faculty evaluations and academic document processing across higher education institutions.

---

## 👥 Team Interfolio – Project Members

- **Rishi Chendrayan** — Backend Architecture, Database Design
- **Pavithra Shankar** — Frontend Development, UI/UX, Testing & Quality Assurance

---

## 📖 Project Overview

**Interfolio** replicates a professional academic management platform designed for universities and colleges to manage faculty applications, hiring decisions, tenure evaluations, and activity reporting.

The platform provides role-specific dashboards and document handling systems for:
- **Faculty members** submitting portfolios and dossiers
- **Reviewers** providing structured feedback and scoring
- **Deans and Administrators** overseeing the entire process
- **IT/Admin users** managing roles, permissions, and workflows

Built with a modular architecture and role-based access control, the system emphasizes usability, security, and scalability.

---

## 🔐 Role-based Test User Accounts

To test the system across different roles, use the following credentials (all passwords are in plaintext for demonstration only):

| **Username**     | **Password**   | **User Role** |
|------------------|----------------|---------------|
| `r@r.com`        | `12345`        | Administrator |
| `c@c.com`        | `12345`        | Faculty       |
| `a@a.com`        | `12345`        | Reviewer      |
| `p@p.con`        | `12345`        | Dean          |

Use these users to test submission flows, review cycles, and dashboard functionalities.

---

## 🧱 System Architecture & Components

```bash
Interfolio/
├── Interfolio/                    # Main application package
│   ├── app.py                     # Flask application entry point
│   ├── baseObject.py              # Base class for SQLAlchemy models
│   ├── config.yml                 # Configuration settings (database, session)
│
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── documents.py
│   │   ├── dossier.py
│   │   ├── evaluation.py
│   │   ├── evaluation_comments.py
│   │   ├── evaluation_stage.py
│   │   ├── stage_reviewers.py
│   │   ├── user.py
│
│   ├── templates/                 # HTML templates for rendering pages
│   │   ├── base.html              # Base layout
│   │   ├── index.html             # Homepage
│   │   ├── login.html             # Login form
│   │   ├── register.html          # User registration
│   │   ├── dossiers_*             # Faculty dossier handling
│   │   ├── reviews_*              # Review workflows
│   │   └── admin/                 # Admin dashboard templates
│       └── evaluations/           # Evaluation setup and list templates
│
│   ├── static/                    # CSS, uploads, and branding
│   │   ├── style.css              # Custom styles
│   │   ├── images/                # University or project logos
│   │   └── uploads/               # Uploaded user documents (PDFs, resumes)
│
```

---

## 🗃️ Relational Database Schema

The database follows a normalized relational model covering entities like:
- Users
- Dossiers
- Evaluations
- Evaluation_stages
- Stage_reviewers
- Evaluation_comments
- Documents

![image](https://github.com/user-attachments/assets/089197a9-3928-4bca-911f-7e35d5b30c9c)

```bash
mysql -u root -p < chendrr_interfolio.sql
```

---

## 📊 Sample Analytical Queries
These queries are used for insight generation and reporting within the admin dashboard.

1. 📑 Total Dossiers Submitted per User
```bash
SELECT user_id, COUNT(*) AS total_dossiers
FROM dossiers
GROUP BY user_id;
```

2. 📄 Dossiers and Their Current Status
```bash
SELECT dossier_id, title, status, created_at
FROM dossiers
ORDER BY created_at DESC;
```

3. 📂 List of Documents Uploaded per Reviewer
```bash
SELECT reviewer_id, COUNT(*) AS total_documents
FROM documents
GROUP BY reviewer_id;
```

4. 🧾 Evaluation Count and Completion Rate
```bash
SELECT 
  COUNT(*) AS total_evaluations,
  COUNT(completed_at) AS completed_evaluations,
  ROUND(100.0 * COUNT(completed_at) / COUNT(*), 2) AS completion_rate_percent
FROM evaluations;
```

5. 🧠 Most Active Reviewers (By Document Uploads)
```bash
SELECT reviewer_id, COUNT(*) AS uploads
FROM documents
GROUP BY reviewer_id
ORDER BY uploads DESC
LIMIT 5;
```

6. 🧮 Average Time to Complete Evaluations
```bash
SELECT 
  AVG(TIMESTAMPDIFF(DAY, started_at, completed_at)) AS avg_days_to_complete
FROM evaluations
WHERE completed_at IS NOT NULL;
```

7. 💬 Number of Comments by Each Reviewer (Commenter)
```bash
SELECT commenter_id, COUNT(*) AS comment_count
FROM evaluation_comments
GROUP BY commenter_id
ORDER BY comment_count DESC;
```

8. 📋 Dossiers with Evaluations but No Comments
```bash
SELECT d.dossier_id, d.title
FROM dossiers d
JOIN evaluations e ON d.dossier_id = e.dossier_id
LEFT JOIN evaluation_comments c ON e.evaluation_id = c.stage_id
WHERE c.comment_id IS NULL;
```

9. 📥 Document Upload Timeline
```bash
SELECT DATE(uploaded_at) AS upload_date, COUNT(*) AS uploads
FROM documents
GROUP BY upload_date
ORDER BY upload_date DESC;
```

10. 🧾 Evaluation Status Breakdown
```bash
SELECT status, COUNT(*) AS count
FROM evaluations
GROUP BY status;
```
---

## 📦 SQL Assets Included
The file chendrr_interfolio.sql contains:
  - ✅ Schema Definitions (CREATE TABLE)
  - ✅ Primary and Foreign Key Constraints
  - ✅ Role Initialization and Permissions
  - ✅ Sample Users and Test Data
  - ✅ Table Relationships and Indexes

---

## 🎯 Features and Highlights
  - 📁 Document Submission & Storage for Faculty
  - 🗂️ Custom Evaluation Rubrics and Review Forms
  - 🔒 Secure Role-based Login
  - 📈 Admin Dashboard with Analytics
  - 🔄 Dynamic Application Routing Between Reviewers
  - 🧾 Reviewer Comments & Final Recommendations

---

## 🔐 Security Best Practices
  - ⚠️ Passwords are stored in plain text in demo mode.
  - Use hashed passwords (e.g., bcrypt) in production.
  - CSRF protection is recommended for form submissions
  - JWT or session-based auth can be integrated easily
  - Use role-checks in all backend endpoints

---

## 🚧 Known Issues & Future Improvements
 - Email notification system for status updates
 - File upload type and size restrictions
 - Full audit trail logging for reviews and comments
 - Reviewer reassignment logic improvement
