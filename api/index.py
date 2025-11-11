from flask import Flask, request, jsonify, render_template
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
app = Flask(__name__)

def get_connection():
        connection = psycopg2.connect(CONNECTION_STRING)
        print("Connection successful!")
        return connection
    

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/sensor')
def sensor():
    # Connect to the database
    try:
        conn = get_connection()
        # Create a cursor to execute SQL queries
        cursor = conn.cursor()
        # Example query
        cursor.execute("select * from sensores;")
        result = cursor.fetchall()
        for i in result:
                print(f"Current Time:{i}")
    
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Connection closed.")
        return f"current time:{result}"
    
    except Exception as e:
        return f"Failed to connect: {e}"

@app.route("/sensor/<int:sensor_id>")
def get_sensor(sensor_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Get the latest 10 values
        cur.execute("""
            SELECT value, created_at
            FROM sensores
            WHERE sensores_id = %s
            ORDER BY created_at DESC
            LIMIT 10;
        """, (sensor_id,))
        rows = cur.fetchall()

        # Convert to lists for graph
        values = [r[0] for r in rows][::-1]        # reverse for chronological order
        timestamps = [r[1].strftime('%Y-%m-%d %H:%M:%S') for r in rows][::-1]
        
        return render_template("sensor.html", sensor_id=sensor_id, values=values, timestamps=timestamps, rows=rows)

    except Exception as e:
        return f"<h3>Error: {e}</h3>"

    finally:
        if 'conn' in locals():
            conn.close()
                
@app.route('/pagina')
def pagina():
        return render_template("pagina.html")
