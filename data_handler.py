import datetime
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

    def open_import_window():
        pass

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
