import pandas as pd
import requests
import pymysql
from datetime import datetime
import streamlit as st
import credentials

API_URL = "http://api.open-notify.org/iss-now.json"  

def fetch_api_data():
    """
    Fetches data from the API and returns it as a dictionary.
    """
    try:
        print(f"Fetching data from API: {API_URL}")
        response = requests.get(API_URL, timeout=40)
        response.raise_for_status()
        data = response.json()
        print("Data fetched from API:", data)
        return data
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def save_to_rds(data):
    """
    Saves the API data to the RDS instance.
    """
    try:
        connection = pymysql.connect(
            host=credentials.MYSQL_CRED['host'],
            user=credentials.MYSQL_CRED['user'],
            password=credentials.MYSQL_CRED['password'],
            database=credentials.MYSQL_CRED['database'])
        with connection.cursor() as cursor:
            # Create table (if not exists) and insert data logic... 
            create_table_query = """
                CREATE TABLE IF NOT EXISTS iss_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp BIGINT NOT NULL,
                    latitude VARCHAR(50) NOT NULL,
                    longitude VARCHAR(50) NOT NULL,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            cursor.execute(create_table_query)

            insert_query = """
                INSERT INTO iss_data (timestamp, latitude, longitude)
                VALUES (%s, %s, %s);
            """
            iss_position = data.get("iss_position", {})
            cursor.execute(insert_query, (data["timestamp"], iss_position["latitude"], iss_position["longitude"]))
            connection.commit()

            print("Data saved to RDS successfully.")

    except pymysql.MySQLError as e:
        print(f"Error saving data to RDS: {e}")

def query_rds():
    """
    Queries the data from the RDS instance.
    """
    try:
        connection = pymysql.connect(
            host=credentials.MYSQL_CRED['host'],
            user=credentials.MYSQL_CRED['user'],
            password=credentials.MYSQL_CRED['password'],
            database=credentials.MYSQL_CRED['database'])
        with connection.cursor() as cursor:
            # Query the table
            query = "SELECT * FROM iss_data ;"
            cursor.execute(query)
            rows = cursor.fetchall()

            # Convert the result to a Pandas DataFrame
            df = pd.DataFrame(rows, columns=["id", "timestamp", "latitude", "longitude", "fetched_at"])
            print("\nPrint records from RDS:")
            print(df)
            st.title("Query the data from RDS")
            st.markdown(" Showing records stored in the iss_data table  \n **Query:**  \nselect * from iss_data")
            st.dataframe(df)

    except pymysql.MySQLError as e:
        print(f"Error querying data from RDS: {e}")

if __name__ == "__main__":
    # Fetch data from API
    data = fetch_api_data()
    if data:
        # Save the data to RDS
        save_to_rds(data)
        # Query the saved data
        query_rds()