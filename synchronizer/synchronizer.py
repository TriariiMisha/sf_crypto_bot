#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from utils import execute_values, get_db_connection, prepare_df

# set consts
TEMP_DIR = 'temp'
DB_PATH = 'sources/db.ini'
TABLE = 'public.bybit_records'

# get and process files
tmp_files = [f'{TEMP_DIR}/{name}' for name in os.listdir(TEMP_DIR)]
results_df = prepare_df(tmp_files)

# establish connection and write to DB
connection = get_db_connection(DB_PATH)
execute_values(connection, results_df, TABLE)
connection.close()

# delete files finally
for path in tmp_files:
    os.remove(path)
