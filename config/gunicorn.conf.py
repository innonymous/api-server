from os import cpu_count, environ
from pathlib import Path

bind = environ.get('API_BIND_URL', '0.0.0.0:8000')

workers = cpu_count()
worker_class = 'uvicorn.workers.UvicornH11Worker'

_logs_path = Path(environ.get('API_LOGS_PATH', './logs'))
accesslog = str(_logs_path / 'access.log')
errorlog = str(_logs_path / 'error.log')
