from multiprocessing.connection import Connection
from util.sqlite_helper import SqliteHelper
from tests.common import TEST_DB_PATH
import os.path
import sqlite3


def test_sqlite_helper_init():
    db = SqliteHelper(TEST_DB_PATH)

    assert type(db) == SqliteHelper
    assert db.db_path == TEST_DB_PATH


def test_sqlite_helper_create_connection():
    db = SqliteHelper(TEST_DB_PATH)
    conn = db._create_connection()

    assert type(conn) == sqlite3.Connection
    assert os.path.isfile(TEST_DB_PATH)
