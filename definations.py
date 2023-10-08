import uuid
import random
import string
from datetime import datetime
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import sqlite3

class mydef:
    def generate_user_id():
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        unique_id = f"{random_chars}"
        return unique_id
    
    def Daily_sma_50_crossed(data):
        try:
            data["SMA_S"] = data["Close"].rolling(50).mean()
            data.dropna(inplace = True)
            data["position"] = np.where(data["SMA_S"] > data["Close"], -1, 1)
            if data.iloc[-2][9]!=data.iloc[-1][9]:
                if data.iloc[-1][9]==1:
                    return [data.iloc[-1][7],'Buy',round(data.iloc[-1][4])]
                else:
                    return [data.iloc[-1][7],'Sell',data.iloc[-1][4]]
                    pass
            else:
                pass
        except:
            pass

    def connect_db():
        conn = sqlite3.connect('kissdb.db')
        conn.row_factory = sqlite3.Row
        return conn
    def connect_mysql():
        import mysql.connector

        # Replace these placeholders with your MySQL database credentials
        hostname = 'localhost'
        username = 'root'
        password = 'Aniket@9'
        database = 'kissdb'

        try:
            # Create a database connection
            connection  = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password,
                database=database
            )

            # # Check if the connection was successful
            # if connection.is_connected():
            #     print("Connected to the MySQL database!")

            #     # Create a cursor object for executing SQL queries
            #     cursor = connection.cursor()

                # # Define your parameterized SQL query
                # query = "SELECT * FROM users"

                # # Define the parameter value(s)
                # parameter_value = 'some_value'

                # # Execute the query with the parameter
                # cursor.execute(query)
                # data = cursor.fetchall()
                # for i in data:
                #     for j in i:
                #         if j=='9010170701':
                #             global l_id
                #             l_id=i[3]
                #             global name
                #             name=i[6]
                #             global ref_id
                #             ref_id=i[4]

                # # Fetch and print the results
                # for row in cursor.fetchall():
                #     print(row)

        except mysql.connector.Error as error:
            print("Error connecting to the database or executing the query:", error)
        # finally:
        #     # Close the cursor and the database connection when done
        #     if 'connection' in locals() and connection.is_connected():
        #         cursor.close()
        #         connection.close()
        #         print("Database connection closed.")
        return connection 
    def level_in(self,l_id,d_amt,ref_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users_tdata WHERE uid = ?', (l_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            query = "INSERT INTO users_daily_income (uid, d_amt) VALUES (?,?)"
            cursor.execute(query, (self.l_id,self.d_amt,))
            query = "INSERT INTO users_daily_income (uid, d_amt) VALUES (?,?)"
            cursor.execute(query, (self.ref_id,self.d_amt,))
            conn.commit()
            
