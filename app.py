import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load Mongo URI from .env
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)
app.run(debug=True, host='0.0.0.0', port=5000)

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        data = request.get_json(force=True)
        item_name = data.get("itemName")
        item_description = data.get("itemDescription")

        if not item_name or not item_description:
            return jsonify({"error": "Both itemName and itemDescription are required"}), 400

        mongo.db.todos.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return jsonify({"message": "To-Do item saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
