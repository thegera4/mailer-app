import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get("DB_HOST"),
        DATABASE_PASSWORD=os.environ.get("MYSQL_ROOT_PASSWORD"),
        DATABASE_USER=os.environ.get("MYSQL_ROOT_USER"),
        DATABASE=os.environ.get("DB_NAME"),
    )

    from . import db

    db.init_app(app)

    from . import mail

    app.register_blueprint(mail.bp)

    return app
