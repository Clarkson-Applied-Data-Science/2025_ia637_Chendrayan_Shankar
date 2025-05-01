# 🎓 Interfolio V9 – Academic Workflow Management Platform

> A full-stack platform built to streamline faculty hiring, evaluations, and academic document processing across higher education institutions.

---

## 👥 Team Interfolio – Project Members

- **Rishi Chendrayan** — Backend Architecture, Database Design
- **Pavithra Shankar** — Frontend Development, UI/UX, Testing & Quality Assurance

---

## 📖 Project Overview

**Interfolio V9** replicates a professional academic management platform designed for universities and colleges to manage faculty applications, hiring decisions, tenure evaluations, and activity reporting.

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
| `admin_user`     | `adminpass`    | Administrator |
| `faculty_jane`   | `janefac123`   | Faculty       |
| `reviewer_john`  | `johnrev456`   | Reviewer      |
| `dean_smith`     | `deanpass789`  | Dean          |

Use these users to test submission flows, review cycles, and dashboard functionalities.

---

## 🧱 System Architecture & Components

```bash
Interfolio_V9/
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
- Users and Roles
- Applications
- Departments
- Evaluation Reports
- Reviewer Assignments

![image](https://github.com/user-attachments/assets/089197a9-3928-4bca-911f-7e35d5b30c9c)

```bash
mysql -u root -p < chendrr_interfolio.sql

```

---

## 📊 Sample Analytical Queries
These queries are used for insight generation and reporting within the admin dashboard.

-- 1. Total faculty in each department
SELECT department, COUNT(*) AS faculty_count
FROM faculty
GROUP BY department;

-- 2. Applications pending per reviewer
SELECT reviewer_id, COUNT(*) AS pending_reviews
FROM applications
WHERE status = 'Submitted'
GROUP BY reviewer_id;

-- 3. Average evaluation turnaround time
SELECT AVG(DATEDIFF(review_end, review_start)) AS avg_review_time
FROM evaluations;

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
