# Hostel Complaint Portal

A full-stack web application built with Django for students to submit and track hostel-related complaints, and for staff to manage and resolve them.

## ✨ Key Features

* **Google OAuth Authentication:** Secure login for students using the university email addresses.
* **Role-Based Access Control:**
    * **Students:** Can create, view, and track the status of their own complaints.
    * **Staff:** Can view all complaints, assign them to departments, change their status, and add remarks.
* **Complaint Management:** A full CRUD (Create, Read, Update, Delete) system for managing hostel issues, including image uploads and a detailed history timeline for each complaint.
* **Email Notifications:** Automatic email notifications are sent to students when their complaint is marked as "Resolved."
* **Modern UI:** A clean, responsive interface built with the [Tabler UI Kit](https://tabler.io/).
* **Robust Backend:**
    * **Search & Pagination:** Easily find complaints and navigate through long lists.
    * **Rate-Limiting:** Protects the complaint submission form from spam.

---
## 🚀 Getting Started

### Prerequisites
* Python 3.10+
* An active Google Cloud project for OAuth2 credentials.

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Dhanvantg/Hostel-Complaint-Portal.git
    cd Hostel-Complaint-Portal
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the project root and add your credentials. Use the `.env.example` file as a template.
    ```ini
    SECRET_KEY="your-django-secret-key"
    DEBUG=True
    
    # Google OAuth Credentials
    GOOGLE_CLIENT_ID="your-google-client-id"
    GOOGLE_CLIENT_SECRET="your-google-client-secret"
    
    # Email Settings (for development)
    EMAIL_HOST_USER="your.email@gmail.com"
    EMAIL_HOST_PASSWORD="your16characterapppassword"
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser and run the server:**
    ```bash
    python manage.py createsuperuser
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

### Google Accounts
Since this project was setup using django allauth, google auth has to be configured for the first time from the admin panel. Go to `http://127.0.0.1:8000/admin` -> Social Applications -> Add new application -> Set provider as google

### Creating Staff users
Staff can access the server on a whitelist-only basis. To add emails to the staff whitelist, simply head to the admin panel, create a new user for that email in `Users` (with password-based authentication disabled), and create a new whitelist for this user in `Staff whitelists`. Now head to `Profiles` and set Role to Staff.

## Quick Glimpses

![Dashboard](https://raw.githubusercontent.com/Dhanvantg/Hostel-Complaint-Portal/main/screenshots/dashboard.png)

![Complaint List](https://raw.githubusercontent.com/Dhanvantg/Hostel-Complaint-Portal/main/screenshots/complaint_list.png)

![Staff View](https://raw.githubusercontent.com/Dhanvantg/Hostel-Complaint-Portal/main/screenshots/staff_view.png)

![Mail](https://raw.githubusercontent.com/Dhanvantg/Hostel-Complaint-Portal/main/screenshots/mail.png)