import math
import sqlite3
from typing import List, Tuple

import pandas as pd

"""
Example data:
Datetime (UTC),Timezone (minutes),Unix Timestamp (UTC),Acc magnitude avg,Eda avg,Temp avg,Movement intensity,Steps count,Rest,On Wrist
2020-01-19T23:58:00Z,-360,1579478280000,0.900365,0.078084,30.865500,0,0,0,true
"""

class DataHandler:
    database: sqlite3.Connection = sqlite3.connect("data.db")
    database.row_factory = lambda c, row: row[0]
    cursor: sqlite3.Cursor = database.cursor()

    df: pd.DataFrame = None

    time_interval = math.inf

    is_data_imported = False
    
    def clear_table():
        try:
            DataHandler.cursor.execute("DELETE FROM data")
        except sqlite3.OperationalError:
            print("Table does not exist")
            return
            
        DataHandler.database.commit()
        DataHandler.is_data_imported = False
        
        if DataHandler.df is not None:
            DataHandler.df.drop(DataHandler.df.index, inplace=True)
            DataHandler.df = None

    def import_data_from_csv(path: str) -> bool:
        print("Importing data from csv...")
        DataHandler.clear_table()
        DataHandler.df = pd.read_csv(path)

        if "Unix Timestamp (UTC)" not in list(DataHandler.df.columns):
            print("Invalid data format")
            DataHandler.clear_table()
            return False

        DataHandler.df.to_sql("data", DataHandler.database, if_exists="append", index=False)
        DataHandler.is_data_imported = True

        return True

    def get(start_timestamp: int, end_timestamp: int, column_name: str) -> List[float]:
        DataHandler.cursor.execute(f"SELECT \"{column_name}\" FROM data WHERE \"Unix Timestamp (UTC)\" BETWEEN {start_timestamp * 1000} AND {end_timestamp * 1000}")
        return DataHandler.cursor.fetchall()

    def get_all(column_name: str) -> List[float]:
        DataHandler.cursor.execute(f"SELECT \"{column_name}\" FROM data")
        return DataHandler.cursor.fetchall()

    def get_time_range() -> Tuple[int, int]:
        DataHandler.cursor.execute("SELECT MIN(\"Unix Timestamp (UTC)\") FROM data")
        start = DataHandler.cursor.fetchone()
        DataHandler.cursor.execute("SELECT MAX(\"Unix Timestamp (UTC)\") FROM data")
        end = DataHandler.cursor.fetchone()
        return (start // 1000, end // 1000)

    def get_time_interval() -> int:
        if DataHandler.time_interval == math.inf:
            DataHandler.cursor.execute("SELECT \"Unix Timestamp (UTC)\" FROM data")
            timestamps = DataHandler.cursor.fetchmany(2)
            DataHandler.time_interval = max((timestamps[1] - timestamps[0]) // 1000, 1)
        
        return DataHandler.time_interval

    def get_timestamps() -> List[int]:
        DataHandler.cursor.execute("SELECT \"Unix Timestamp (UTC)\" FROM data")
        stamps = DataHandler.cursor.fetchall()
        return [stamp // 1000 for stamp in stamps]

    def get_column_names_from_file(path: str) -> List[str] | bool:
        if not path.endswith(".csv"):
            return False

        try:
            df = pd.read_csv(path)
            names = list(df.columns.values)
            return names
        except:
            return False

