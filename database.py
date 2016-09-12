import sqlite3
from flask import g

class database:

    app = None

    def __init__(self, app):
        self.app = app

        @app.teardown_appcontext
        def close_db(error):
            """Closes the database again at the end of the request."""
            if hasattr(g, 'sqlite_db'):
                g.sqlite_db.close()

        " 'flask initdb' command available over cli, so no sqlite is needed "
        " creates pyda.db from schema.sql "
        @app.cli.command('initdb')
        def initdb_command():
            """Initializes the database."""
            self.init_db()
            print('Initialized the database.')


    def connect_db(self):
        """Connects to the specific database."""
        rv = sqlite3.connect(self.app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        return rv

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = self.connect_db()
        return g.sqlite_db

    def init_db(self):
        db = self.get_db()
        with self.app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

   