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

The system is divided into the following core components:

---

## 🗃️ Relational Database Schema

The database follows a normalized relational model covering entities like:
- Users and Roles
- Applications
- Departments
- Evaluation Reports
- Reviewer Assignments

> 📌 Refer to `docs/ERD.png` for the complete **Entity-Relationship Diagram (ERD)**.

To initialize the database from scratch:
```bash
mysql -u root -p < chendrr_interfolio.sql

