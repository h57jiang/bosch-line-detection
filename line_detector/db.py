import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """create new tables files based on schema."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """defines a command line command called init-db that
    calls the init_db function and shows a success message to the user"""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def file_already_uploaded(file_name):
    """Determine if a file has already been uploaded"""
    db = get_db()
    result = db.execute(
        'SELECT 1 FROM files WHERE name = ? LIMIT 1', (file_name,)
    ).fetchall()
    return len(result) > 0


def insert_new_file(file_name):
    """insert information of a new file to db"""
    db = get_db()
    db.execute(
        'INSERT INTO files (name, uploaded_on)'
        ' VALUES (?, ?)',
        (file_name, datetime.datetime.now())
    )
    db.commit()


def update_file(file_name, file_type):
    """update db to indicate if a file is used by training or prediction"""
    db = get_db()
    db.execute(
        'UPDATE files SET type = ?, is_used = true'
        ' WHERE name = ?',
        (file_type, file_name)
    )
    db.commit()

