import multiprocessing

# worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8000'
workers = 2 or multiprocessing.cpu_count() * 2 + 1
forwarded_allow_ips = '*'
max_requests = 5000
max_requests_jitter = 20
timeout = 120
access_log_format = '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = '-'
