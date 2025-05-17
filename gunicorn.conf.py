# Gunicorn configuration file
import multiprocessing
import os
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent

# Server socket
bind = '0.0.0.0:443'  # Changed to HTTPS default port
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Process naming
proc_name = 'Tscript_app'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# SSL Configuration
ssl_paths = {
    'certfile': str(BASE_DIR / 'ssl' / 'server.crt'),
    'keyfile': str(BASE_DIR / 'ssl' / 'server.pfx'),
}

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL settings
ssl_version = 'TLS'
do_handshake_on_connect = True
cert_reqs = 0  # ssl.CERT_NONE

# Limit request line and headers
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Initialize SSL if certificates exist
if os.path.exists(ssl_paths['certfile']) and os.path.exists(ssl_paths['keyfile']):
    certfile = ssl_paths['certfile']
    keyfile = ssl_paths['keyfile']
else:
    print("Warning: SSL certificates not found. Server may not start properly.")
