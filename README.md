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

## Production Deployment

### Prerequisites
- Python 3.x
- pip
- Gunicorn

### Setup Instructions

1. Clone the repository and navigate to the project folder
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your production settings:
   ```
   DJANGO_SECRET_KEY=your-secure-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

4. Run the production setup script:
   ```powershell
   .\setup_production.ps1
   ```

5. Start the production server:
   ```powershell
   .\start_production.ps1
   ```

The application will be available at http://localhost:8000

### Production Considerations

1. **SSL/HTTPS**: Configure SSL certificates for production use
2. **Database**: Consider using PostgreSQL for production
3. **Static Files**: Configure proper static file serving
4. **Logging**: Set up proper logging
5. **Monitoring**: Implement monitoring and error tracking
6. **Backup**: Set up regular database backups

## HTTPS Configuration

The application is configured to run with HTTPS in production. Here's how to set it up:

1. Generate SSL certificates (for development/testing):
   ```powershell
   .\generate_ssl.ps1
   ```
   Note: For production, use proper SSL certificates from a trusted Certificate Authority.

2. Configure your environment:
   ```
   DJANGO_SECRET_KEY=your-secure-secret-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

3. Start the production server:
   ```powershell
   .\start_production.ps1
   ```

The application will be available at https://localhost

### Production SSL Certificates

For production deployment:
1. Obtain SSL certificates from a trusted Certificate Authority
2. Replace the self-signed certificates in the `ssl` directory
3. Update the paths in `gunicorn.conf.py` if necessary

### Security Notes
- Always use HTTPS in production
- Keep SSL certificates secure and up to date
- Regularly update security settings
- Monitor SSL certificate expiration
- Consider using Let's Encrypt for free, automated SSL certificates

## Security

- Keep DEBUG=False in production
- Use strong SECRET_KEY
- Keep .env file secure and never commit it
- Regularly update dependencies
- Use HTTPS in production
- Set up proper firewall rules
