import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions


def get_db():
    # g is a special object that is unique for each request.
    # It is used to store data that might be accessed by multiple functions during the request.
    # The connection is stored and reused instead of creating a new connection if get_db is called a second time
    # in the same request.
    if 'db' not in g:
        # establish connection
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        # return a dictionary cursor
        g.c = g.db.cursor(dictionary=True)

    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)