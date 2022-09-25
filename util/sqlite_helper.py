import sqlite3
from sqlite3 import Error
import pandas as pd


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

    def _create_table(self, query: str):
        """run a create table query, doesn't need to be committed

        Args:
            query (str): the create table statement to run

        """
        conn = self._create_connection()

        # create cursor and execute query
        with conn:
            cur = conn.cursor()
            cur.execute(query)

        conn.close()

    def _select_into_df(self, query: str) -> pd.DataFrame:
        """execute a select query and return the results in a dataframe

        Args:
            query (str): select query to run

        Returns:
            pd.DataFrame: results of select in a dataframe
        """
        conn = self._create_connection()

        # execute select query and return results in df
        df = pd.read_sql(query, conn)
        conn.close()

        return df

    def _query_with_replacement(self, query: str, data: list):
        """run a query against the DB that uses the ? replacement thing

        query should have ? where any variable data goes, and they get replaced from data in order

        DO NOT use for a select, this method does not return things

        Args:
            query (str): the query to run, with the ? replacement standard for variable things
            data (list): the data to insert, replaces ? in query in order of appearance
        """
        conn = self._create_connection()

        # create cursor and execute query
        with conn:
            cur = conn.cursor()
            cur.execute(query, data)

        conn.close()
