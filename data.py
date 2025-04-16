
import sqlite3
import pandas as pd
import streamlit as st
import config

def init_db(csv_path="pima-dataset.csv"):
    try:
        conn = sqlite3.connect(config.DB_NAME)
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{config.TABLE_NAME}'")
        if not cursor.fetchone():
            df = pd.read_csv(csv_path)
            df.to_sql(config.TABLE_NAME, conn, if_exists="replace", index=False)
            conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Failed to initialize database: {e}")

def load_data():
    try:
        conn = sqlite3.connect(config.DB_NAME)
        df = pd.read_sql_query(f"SELECT * FROM {config.TABLE_NAME}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def add_record(data_dict):
    """Insert a new record into the database."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["?" for _ in data_dict])
        values = list(data_dict.values())
        conn.execute(f"INSERT INTO {config.TABLE_NAME} ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to add record: {e}")
        return False

def update_record(record_id, data_dict):
    """Update an existing record in the database by ID."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        set_clause = ", ".join([f"{key} = ?" for key in data_dict.keys()])
        values = list(data_dict.values()) + [record_id]
        conn.execute(f"UPDATE {config.TABLE_NAME} SET {set_clause} WHERE rowid = ?", values)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to update record: {e}")
        return False

def delete_record(record_id):
    """Delete a record from the database by ID."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        conn.execute(f"DELETE FROM {config.TABLE_NAME} WHERE rowid = ?", (record_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to delete record: {e}")
        return False

def get_last_record():
    """Fetch the most recently added record."""
    try:
        conn = sqlite3.connect(config.DB_NAME)
        query = f"SELECT rowid, * FROM {config.TABLE_NAME} ORDER BY rowid DESC LIMIT 1"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df if not df.empty else None
    except Exception as e:
        st.error(f"Failed to fetch last record: {e}")
        return None

def clean_data(df):
    if df is None:
        return None
    for col in ["Glucose", "BloodPressure", "BMI", "Insulin"]:
        df[col] = df[col].replace(0, df[col].median())
    return df