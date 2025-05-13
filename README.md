# django_Tool_App

A Django-based web application for managing and fetching transcripts.

## Project Structure

- `Tscript_app/` - Main Django project folder
  - `db.sqlite3` - SQLite database file
  - `manage.py` - Django management script
  - `transcripts/` - Django app for transcript management
    - `models.py` - Database models
    - `views.py` - Application views
    - `admin.py` - Admin interface registration
    - `templates/transcripts/` - HTML templates
    - `static/transcripts/` - Static files (CSS)
    - `migrations/` - Database migrations
  - `Tscript_app/` - Project settings and configuration
    - `settings.py` - Django settings
    - `urls.py` - URL routing

## Setup Instructions

1. **Install dependencies**

   Ensure you have Python 3 and pip installed. Then, install Django:

   ```powershell
   pip install django
   ```

2. **Apply migrations**

   ```powershell
   python manage.py migrate
   ```

3. **Run the development server**

   ```powershell
   python manage.py runserver
   ```

4. **Access the app**

   Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

- Use the web interface to fetch and manage transcripts.
- Customize templates and static files as needed.

## License

This project is for educational purposes.
