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

    time_interval = math.inf
    
    def clear_table():
        try:
            DataHandler.cursor.execute("DELETE FROM data")
        except sqlite3.OperationalError:
            print("Table does not exist")
            return
            
        DataHandler.database.commit()

    def import_data_from_csv(path: str):
        print("Importing data from csv...")
        DataHandler.clear_table()
        df = pd.read_csv(path)
        df.to_sql("data", DataHandler.database, if_exists="append", index=False)

    #added bc of +/- value
    def load_straight_to_db(df):
        DataHandler.clear_table()
        print("DATA HANDLER:")
        print(df)
        #df is the same, is it not being stored???
        #its stored in the table right
        df.to_sql("data", DataHandler.database, if_exists="append", index=False)

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

        print("START")
        print(start)
        print("END")
        print(end)
        
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

