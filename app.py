from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Configure MongoDB (replace URI if needed)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tododb"
mongo = PyMongo(app)

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
