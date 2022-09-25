from util.sqlite_helper import SqliteHelper
from tests.common import TEST_DB_PATH
import os
import sqlite3
import pytest
import pandas as pd


def test_sqlite_helper_init():
    db = SqliteHelper(TEST_DB_PATH)

    assert type(db) == SqliteHelper
    assert db.db_path == TEST_DB_PATH


def test_sqlite_helper_create_connection():
    db = SqliteHelper(TEST_DB_PATH)
    conn = db._create_connection()

    assert type(conn) == sqlite3.Connection
    assert os.path.isfile(TEST_DB_PATH)

    conn.close()


def test_sqlite_helper_create_table_query():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    db = SqliteHelper(TEST_DB_PATH)

    # see if create works
    create_table_query = "CREATE TABLE IF NOT EXISTS test (id integer PRIMARY KEY, name text UNIQUE);"
    db._create_table(create_table_query)

    # select from empty table
    select_query = "SELECT * FROM test;"
    df = db._select_into_df(select_query)

    assert type(df) == pd.DataFrame
    assert df.empty
    assert "id" in df.columns
    assert "name" in df.columns


def test_sqlite_helper_query_with_replacement():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    db = SqliteHelper(TEST_DB_PATH)

    # see if create works
    create_table_query = "CREATE TABLE IF NOT EXISTS test (id integer PRIMARY KEY, name text UNIQUE);"
    db._create_table(create_table_query)

    select_query = "SELECT * FROM test;"

    # insert a row
    data = ["name1"]
    insert_query = "INSERT INTO test(name) VALUES (?);"
    db._query_with_replacement(insert_query, data)
    df = db._select_into_df(select_query)
    assert not df.empty
    assert df.shape[0] == 1

    # bad query raises error
    with pytest.raises(sqlite3.Error):
        db._query_with_replacement("INSERT INTO test VALUES (?);", data)

    # insert another
    data = ["name2"]
    db._query_with_replacement(insert_query, data)
    df = db._select_into_df(select_query)
    assert not df.empty
    assert df.shape[0] == 2

    # delete one row
    delete_query = "DELETE FROM test WHERE name = ?;"
    db._query_with_replacement(delete_query, data)
    df = db._select_into_df(select_query)
    assert not df.empty
    assert df.shape[0] == 1
