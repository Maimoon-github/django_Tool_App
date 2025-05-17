# Create necessary directories
Write-Host "Creating necessary directories..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "Tscript_app/staticfiles" | Out-Null
New-Item -ItemType Directory -Force -Path "Tscript_app/media" | Out-Null

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Green
python Tscript_app/manage.py collectstatic --noinput

# Apply database migrations
Write-Host "Applying database migrations..." -ForegroundColor Green
python Tscript_app/manage.py migrate

Write-Host "Setup completed successfully!" -ForegroundColor Green
