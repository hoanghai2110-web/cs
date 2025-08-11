import os
from flask import Flask, request
from flask.helpers import get_debug_flag
from werkzeug.middleware.proxy_fix import ProxyFix

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # needed for url_for to generate with https

# Performance optimizations
if not get_debug_flag():
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year cache for static files

# Security headers for performance
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    # Optimized performance headers for high traffic
    if request.endpoint == 'index':
        response.headers['Cache-Control'] = 'public, max-age=14400, stale-while-revalidate=86400, immutable'
        response.headers['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
    elif request.endpoint in ['country', 'inbox']:
        response.headers['Cache-Control'] = 'public, max-age=3600, stale-while-revalidate=14400'
    elif request.endpoint == 'sitemap_xml':
        response.headers['Cache-Control'] = 'public, max-age=86400'
    elif request.endpoint in ['robots_txt']:
        response.headers['Cache-Control'] = 'public, max-age=604800'  # 1 week
    else:
        response.headers['Cache-Control'] = 'public, max-age=7200, stale-while-revalidate=86400'

    # Additional performance optimizations for high traffic
    response.headers['Connection'] = 'keep-alive'
    response.headers['Keep-Alive'] = 'timeout=5, max=1000'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Server-Timing'] = 'app;dur=0'

    return response

# Enable compression for better performance
from flask_compress import Compress
Compress(app)

# Import routes
import routes  # noqa: F401