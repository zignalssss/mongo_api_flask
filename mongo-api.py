from pymongo.mongo_client import MongoClient
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


#       MONGO SECTION   #
uri = "mongodb+srv://User:DGb7LCLWDAWGuc95@cluster0.kqhyq1c.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
def showall_table(collection):
    print(f'found {collection.count_documents({})} records')
    all_students = collection.find()
    for std in all_students:
        print(std)

def insert_table(collection):
    id = input("Input student id:")
    name = input("Input fullname:")
    major = input("Input major:")
    gpa = input("Input gpa:")
    gpa = float(gpa)
    try:
        collection.insert_one({
            "_id": id,
            "fullname": name,
            "major": major,
            "gpa": gpa
        })
    except Exception as e:
        print(e)

def select_update_table(collection):
    print("Which column do you want to update?")
    print("choose 1: fullname")
    print("choose 2: major")
    print("choose 3: gpa")

    choose = int(input("Please select: "))
    where_id = input("Where ID?: ")

    if choose == 1:
        new_fullname = input("Please Enter new Fullname: ")
        update_table(collection, "fullname", new_fullname, where_id)
    elif choose == 2:
        new_major = input("Please Enter new Major: ")
        update_table(collection, "major", new_major, where_id)
    elif choose == 3:
        new_gpa = float(input("Please Enter new GPA: "))
        update_table(collection, "gpa", new_gpa, where_id)

def update_table(collection, title_name, new_value, where):
    try:
        myquery = {"_id": where}
        newvalues = {"$set": {title_name: new_value}}
        result = collection.update_one(myquery, newvalues)
        if result.modified_count > 0:
            print("Update successful!")
        else:
            print("No document was updated. Check your 'where' condition.")
    except Exception as e:
        print(f"Error: {e}")

def delete_table(collection):
    where = input("Where ID? : ")
    try:
        result = collection.delete_one({"_id": where})
        if result.deleted_count > 0:
            print("Delete successful!")
        else:
            print("No document found for deletion.")
    except Exception as e:
        print(f"Error: {e}")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["students"]
    collection = db["std_info"]
    while True:
        print("===MENU===")
        print("1: show all records")
        print("2: insert record")
        print("3: update record")
        print("4: delete record")
        print("5: exit")
        choice = input("Please choose:")
        choice = int(choice)
        if choice == 1:
            showall_table(collection)
        elif choice == 2:
            insert_table(collection)
        elif choice == 3:
            select_update_table(collection)
        elif choice == 4:
            delete_table(collection)
        elif choice == 5:
            break

except Exception as e:
    print(e)
finally:
    client.close()
