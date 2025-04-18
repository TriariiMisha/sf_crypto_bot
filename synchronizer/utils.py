import pickle
from configparser import ConfigParser

import pandas as pd
import psycopg2
import psycopg2.extras as extras


def get_db_connection(credentials_file: str):
    cp = ConfigParser()
    _ = cp.read(credentials_file)

    db_params = cp['pg.client']

    connection = psycopg2.connect(
        database=db_params['db_name'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port'],
    )

    return connection


def execute_values(conn, df, table):
    tuples = [tuple(x) for x in df.values]

    cols = ','.join(list(df.columns))

    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()

    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        cursor.close()
        conn.close()
        raise Exception(str(error))
    finally:
        print("execute_values() done")
        cursor.close()


def process_file(path: str) -> list:
    with open(path, 'rb') as file:
        record = pickle.load(file)

        return record


def prepare_df(paths):
    items = [process_file(path) for path in paths]

    # flatten results
    items_flatten = []
    for item in items:
        items_flatten.extend(item)

    # process to pandas
    return pd.DataFrame.from_records(items_flatten)
