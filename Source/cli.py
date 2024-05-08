import questionary
import pymongo
from datetime import datetime
import pickle

client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")

def reset_database():
    db = client["cmpe266_db"]
    collection = db["data"]
    collection.drop()
    model_collection = db["model"]
    model_collection.drop()

    db = client["cmpe266_db"]
    collection = db["data"]
    model_collection = db["model"]

    model = pickle.load(open("model.pkl", 'rb'))
    model_collection.insert_one({"model_object": model, "timestamp_field": datetime.now()})
    latest_model_document = model_collection.find().sort([("timestamp_field", pymongo.DESCENDING)]).limit(1)[0]
    model = latest_model_document["model_object"]

    initial_data = [
        {"amount": 15000.0, "interest_rate": 7.2, "tenure": 15},
        {"amount": 90000.0, "interest_rate": 12.6, "tenure": 23},
        {"amount": 5500.0, "interest_rate": 3.8, "tenure": 10},
        {"amount": 68000.0, "interest_rate": 9.1, "tenure": 18},
        {"amount": 2500.0, "interest_rate": 5.5, "tenure": 5},
    ]

    result = collection.insert_many(initial_data)
    print(f"Inserted {len(result.inserted_ids)} data documents")
    return initial_data


added_points = reset_database()

def add_data_point():
    questions = [
        {"type": "input", "name": "amount", "message": "Enter Amount:"},
        {"type": "input", "name": "interest_rate", "message": "Enter Interest Rate:"},
        {"type": "input", "name": "tenure", "message": "Enter Tenure (in years):"},
    ]
    answers = questionary.prompt(questions)
    
    answers["amount"] = float(answers["amount"])
    answers["interest_rate"] = float(answers["interest_rate"])
    answers["tenure"] = int(answers["tenure"])
    
    added_points.append(answers)
    db = client["cmpe266_db"]
    collection = db["data"]
    collection.insert_one(answers)
    # Process the data point here, e.g., store it in a database or perform calculations

def display_menu():
    print("\nMenu:")
    print("1. Add Data Point")
    print("2. Exit")

def main():
    while True:
        # display_menu()
        print("\nMenu:")
        choice = questionary.select("Enter your choice:", choices=["Add Data Point", "Pick Data Point", "Exit"]).ask()

        if choice == "Add Data Point":
            add_data_point()
        elif choice == "Pick Data Point":
            if len(added_points) > 0:
                choice = questionary.select("Enter your choice:", choices=[str(p) for p in added_points]).ask()
                index = [str(p) for p in added_points].index(choice)
                # make_inference()
                print(index)
            else:
                print("No added points")
        elif choice == "Exit":
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
