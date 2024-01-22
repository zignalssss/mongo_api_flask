from pymongo.mongo_client import MongoClient
from flask import Flask,jsonify,request
from flask_basicauth import BasicAuth

app = Flask(__name__)
uri = "mongodb+srv://User:DGb7LCLWDAWGuc95@cluster0.kqhyq1c.mongodb.net/?retryWrites=true&w=majority"
#Basic Auth
app.config['BASIC_AUTH_USERNAME'] ='somnamna'
app.config['BASIC_AUTH_PASSWORD'] ='jaifu'
basic_auth = BasicAuth(app)

def get_mongo_client():
    return MongoClient(uri)

@app.route("/")
def Greet():
    return "<center><p>Welcome to Student Management API </p></center>"

@app.route("/students", methods=["GET"])
@basic_auth.required
def show_all_student():
    try:
        client = get_mongo_client()
        db = client.students
        collection = db.std_info
        all_students = list(collection.find())
        return jsonify(all_students)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        client.close()

@app.route("/students/<int:std_id>", methods=["GET"])
@basic_auth.required
def get_student_by_id(std_id):
    try:
        client = get_mongo_client()
        db = client.students
        collection = db.std_info
        std = collection.find_one({"_id": str(std_id)})
        if not std:
            return jsonify({"error": "Student not found"}), 404
        return jsonify(std)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        client.close()
@app.route("/students", methods=["POST"])
@basic_auth.required
def add_std():
    try:
        client = get_mongo_client()
        db = client.students
        collection = db.std_info
        data = request.get_json()
        already_data = collection.find_one({"_id": data.get("_id")})
        if already_data:
            return jsonify({"error":"Cannot create new student"}), 500
        collection.insert_one(data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        client.close()
@app.route("/students/<int:std_id>", methods=["PUT"])
@basic_auth.required
def update_student(std_id):
    try:
        client = get_mongo_client()
        db = client.students
        collection = db.std_info
        data = request.get_json()
        std_data = collection.find_one({"_id": str(std_id)})
        if not std_data:
            return jsonify({"error":"Student not found"}), 404
        collection.update_one({"_id":str(std_id)}, {"$set": data})
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        client.close()
@app.route("/students/<int:std_id>", methods=["DELETE"])
@basic_auth.required
def delete_student(std_id):
    try:
        client = get_mongo_client()
        db = client.students
        collection = db.std_info
        std_data = collection.find_one({"_id": str(std_id)})
        if not std_data:
            return jsonify({"error":"Student not found"}), 404
        collection.delete_one({"_id": str(std_id)})
        return jsonify({"message":"Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        client.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)