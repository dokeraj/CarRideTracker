import dataclasses
import sqlite3
from dataclasses import dataclass
from sqlite3 import Error

import config


@dataclass
class Counts:
    user: str
    count: int


@dataclass
class Record:
    log_id: int
    user: str
    timestamp: int


def init_db():
    conn = None
    try:
        conn = sqlite3.connect(config.sqllite_db_location)

        conn.execute('''CREATE TABLE IF NOT EXISTS TRACKING
                     (LOG_ID INTEGER PRIMARY KEY,
                     USER        CHAR(100) NOT NULL,
                     TIMESTAMP   INT       NOT NULL);''')

        conn.commit()
        print(f"Successfully initialized sqlite db: {sqlite3.version}")
    except Error as e:
        print(f"Error initializing sqlite: {e}")
    finally:
        if conn:
            conn.close()


def insert_record(user: str, timestamp: int):
    conn = sqlite3.connect(config.sqllite_db_location)
    cur = conn.cursor()
    cur.execute(
        f"""INSERT OR IGNORE INTO TRACKING (USER,TIMESTAMP) VALUES (\'{user}\', {timestamp})""")

    conn.commit()
    result = cur.rowcount == 1

    conn.close()
    return result


def update_record(record_id: int, timestamp: int):
    conn = sqlite3.connect(config.sqllite_db_location)
    cur = conn.cursor()
    cur.execute(f"UPDATE TRACKING SET TIMESTAMP = {timestamp} WHERE LOG_ID={record_id};")

    conn.commit()
    result = cur.rowcount == 1

    conn.close()

    return result


def get_users_and_counts():
    conn = sqlite3.connect(config.sqllite_db_location)
    cur = conn.cursor()
    cur.execute(f"""SELECT USER, count(USER) FROM TRACKING GROUP BY USER;""")

    counts_list = []

    rows = cur.fetchall()
    for row in rows:
        counts_list.append(dataclasses.asdict(Counts(row[0], row[1])))

    conn.close()

    return counts_list


def delete_record(record_id):
    conn = sqlite3.connect(config.sqllite_db_location)
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM TRACKING WHERE LOG_ID == {record_id}""")

    conn.commit()
    result = cur.rowcount == 1

    conn.close()

    return result


def get_logs(skip, count, ordering):
    conn = sqlite3.connect(config.sqllite_db_location)
    cur = conn.cursor()
    cur.execute(f"""SELECT LOG_ID,USER,TIMESTAMP FROM TRACKING ORDER BY TIMESTAMP {ordering} LIMIT {skip}, {count};""")

    rows = cur.fetchall()

    records = []

    for row in rows:
        records.append(dataclasses.asdict(Record(row[0], row[1], row[2])))

    conn.close()

    conn = sqlite3.connect(config.sqllite_db_location)
    cur = conn.cursor()
    cur.execute(f"""SELECT count(*) FROM TRACKING;""")
    total = cur.fetchone()[0]

    conn.close()

    return records, total
