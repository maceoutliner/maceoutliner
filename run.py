# run.py
from waitress import serve
from config import wsgi
import os

if 'DATA_DB_USER' in os.environ.keys() and os.environ['DATA_DB_USER'] == 'gonano':
    # We are in a nanobox instance.
    serve_kwargs = {
        'host': '0.0.0.0',
        'port': 8000,
    }
    init_file_target = '/app/tmp/app-initialized'
else:
    # We are in some other place, use a unix socket.
    serve_kwargs = {
        'unix_socket': '/tmp/nginx.socket',
    }
    init_file_target = '/tmp/app-initialized'

# touch app-initialized
open(init_file_target, 'w').close()
# start waitress
serve(wsgi.application, **serve_kwargs)
