bind = 'unix:/var/www/god.goals.glory/gunicorn_btg.sock'
workers = 3
timeout = 120
umask = 0o007  # Ensures socket permissions are rw-rw---- (owner and group access)