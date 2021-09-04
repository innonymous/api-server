from os import cpu_count

bind = '0.0.0.0:8000'

workers = cpu_count()
worker_class = 'uvicorn.workers.UvicornH11Worker'
