import os
from flask import Flask, redirect, render_template, request
from flask.ext.basicauth import BasicAuth
import json
import logging
from raven.contrib.flask import Sentry
import requests
from .forms import TitleForm

app = Flask(__name__)

# Auth
if os.environ.get('BASIC_AUTH_USERNAME'):
    app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

# Sentry exception reporting
if 'SENTRY_DSN' in os.environ:
    sentry = Sentry(app, dsn=os.environ['SENTRY_DSN'])

# Logging
@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def title_form():
    form = TitleForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data
        data['registered_owners'] = filter(
            lambda o: o['name'] != '',
            data['registered_owners']
        )
        data['lenders'] = filter(
            lambda o: o['name'] != '',
            data['lenders']
        )
        data['related_titles'] = filter(
            lambda o: o['title_number'] != '',
            data['related_titles']
        )
        res = requests.post(
          'http://lr-concept-system-of-record.herokuapp.com/entries',
          data=json.dumps(data),
          headers={'content-type': 'application/json'}
        )
        if res.status_code != 201:
            res.raise_for_status()
        return redirect('/done')
    return render_template("title_form.html", form=form)

@app.route('/done')
def title_done():
    return render_template("title_done.html")
