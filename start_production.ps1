# Function to check if a port is available
function Test-Port {
    param($Port)
    try {
        $null = New-Object System.Net.Sockets.TcpClient('localhost', $Port)
        return $false
    } catch {
        return $true
    }
}

# Verify SSL certificates
if (-not (Test-Path "ssl/server.pfx") -or -not (Test-Path "ssl/server.crt")) {
    Write-Host "SSL certificates not found. Please run generate_ssl.bat first." -ForegroundColor Red
    exit 1
}

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Green
python Tscript_app/manage.py collectstatic --noinput

# Apply database migrations
Write-Host "Applying database migrations..." -ForegroundColor Green
python Tscript_app/manage.py migrate

# Create superuser if it doesn't exist
Write-Host "Checking superuser..." -ForegroundColor Green
python Tscript_app/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Creating superuser..." -ForegroundColor Green
    python Tscript_app/manage.py createsuperuser --noinput
}

# Set environment variables
$env:DJANGO_SETTINGS_MODULE = "Tscript_app.settings"
$env:DJANGO_DEBUG = "False"
$env:DJANGO_ALLOWED_HOSTS = "localhost,127.0.0.1"

# Check if ports are available
if (-not (Test-Port 443)) {
    Write-Host "Warning: Port 443 is in use. Falling back to port 8443 for HTTPS" -ForegroundColor Yellow
    $httpsPort = 8443
} else {
    $httpsPort = 443
}

# Start Gunicorn with SSL
Write-Host "Starting Gunicorn server with HTTPS on port $httpsPort..." -ForegroundColor Green
$gunicornCmd = "gunicorn Tscript_app.wsgi:application --bind=0.0.0.0:$httpsPort --config=gunicorn.conf.py"

# Create a function to handle cleanup
function Cleanup {
    Write-Host "`nStopping server..." -ForegroundColor Yellow
    Get-Process | Where-Object { $_.Name -eq 'gunicorn' } | Stop-Process -Force
}

# Register cleanup handler
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

try {
    # Start the server
    Invoke-Expression $gunicornCmd
}
catch {
    Write-Host "Error starting server: $_" -ForegroundColor Red
}
finally {
    Cleanup
}
