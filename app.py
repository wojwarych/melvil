import os
import time

from raven import Client
from raven.contrib.flask import Sentry

from flask import Flask
from flask_mail import Mail

from config import DevConfig
from init_db import db
from views import library
from views.index import login_manager
from xlsx_reader import get_books, get_magazines


mail = Mail()
sentry = Sentry()
client = Client()


def create_app(config=DevConfig):

    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(library)
    app.secret_key = os.urandom(24)
    login_manager.init_app(app)
    mail.init_app(app)

    db_not_ready = True
    while db_not_ready:
        try:
            db.init_app(app)
            with app.app_context():
                db.create_all()
            db_not_ready = False
        except:
            print("DB not ready!")
            print("Polling DB..")
            time.sleep(1)

    return app


app = create_app()


@app.cli.command(with_appcontext=True)
def load_xls_into_db():
    get_magazines('./data/biblioteka_oczyszczona.xlsx')
    get_books('./data/biblioteka_oczyszczona.xlsx')


app.cli.add_command(load_xls_into_db)


create_app(DevConfig)
