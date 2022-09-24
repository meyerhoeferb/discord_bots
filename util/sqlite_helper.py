import sqlite3
from sqlite3 import Error


class SqliteHelper:
    """base wrapper library for using a sqlite3 database

    Just the basic methods, meant to then be extended for actual use
    """

    def __init__(self, db_path: str):
        """init

        Args:
            db_path (str): path to the sqlite database this object will operate on, use :memory: to create a db in memory
        """
        self.db_path = db_path

    def _create_connection(self) -> sqlite3.Connection:
        """create a connection the database this helper is pointed at
        mainly meant to be used internally, but when used make sure
        to close the connection when done

        Not using try catch at this level, catch exceptions as needed during usage

        Returns:
            sqlite3.Connection: the created connection object
        """
        conn = sqlite3.connect(self.db_path)

        return conn
