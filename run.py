# run.py
from waitress import serve
from maceoutliner import wsgi

# touch app-initialized
open('/tmp/app-initialized', 'w').close()
# start waitress
serve(wsgi.application, unix_socket='/tmp/nginx.socket')
