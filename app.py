from flask import Flask, request, jsonify  
from pymongo import MongoClient           
from datetime import datetime              
import os                                  


app = Flask(__name__)

client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"))

# Connect to the database named 'flask_db'
db = client.flask_db

# Connect to the collection named 'data'
collection = db.data

# Define the route for the root URL
@app.route('/')
def index():
    # Return a welcome message with the current time
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

# Define the route for '/data'
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # Get the JSON data from the POST request
        data = request.get_json()
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == 'GET':
        # Retrieve all documents except the _id field
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
