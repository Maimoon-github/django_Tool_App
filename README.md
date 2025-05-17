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

## Features

- Fetch YouTube video transcripts
- Age calculator tool
- Blog with categories and posts
- User authentication (login/logout)
- Admin interface for managing content

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

## Running the Project

1. Clone the repository and navigate to the project folder.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```powershell
   python Tscript_app/manage.py migrate
   ```

4. Create a superuser (optional, for admin access):

   ```powershell
   python Tscript_app/manage.py createsuperuser
   ```

5. Start the development server:

   ```powershell
   python Tscript_app/manage.py runserver
   ```

6. Open your browser and go to http://127.0.0.1:8000/

## Usage

- Use the web interface to fetch and manage transcripts.
- Customize templates and static files as needed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is for educational purposes.
