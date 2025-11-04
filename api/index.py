from flask import Flask
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
        result = cursor.fetchone()
        print("Current Time:", result)
    
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Connection closed.")
        return f"current time:{result}"
    
    except Exception as e:
        return f"Failed to connect: {e}"

@app.route("/sensor/<int:sensor_id>", methods=["POST"])
def insert_sensor_value(sensor_id):
    value = request.args.get("value", type=float)
    if value is None:
        return jsonify({"error": "Missing 'value' query parameter"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Insert into sensors table
        cur.execute(
            "INSERT INTO sensors (sensor_id, value) VALUES (%s, %s)",
            (sensor_id, value)
        )
        conn.commit()

        return jsonify({
            "message": "Sensor value inserted successfully",
            "sensor_id": sensor_id,
            "value": value
        }), 201

    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'conn' in locals():
            conn.close()
