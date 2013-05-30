"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)


# query parser
app.add_url_rule('/api/query', 'say_hello', view_func=views.say_hello, methods=['POST'])
app.add_url_rule('/database', 'manual_write', view_func=views.manual_write)
app.add_url_rule('/api/add/<title>', 'tester_toast', view_func=views.tester_toast)
app.add_url_rule('/api/flush/<title>', 'flush_toast', view_func=views.flush_toast)
app.add_url_rule('/api/index', 'flush_toast', view_func=views.flush_toast)


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

