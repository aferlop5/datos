import sys
import pymongo
import argparse
from bson import ObjectId

def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ej1_db"]
    collection = db["users"]
    return collection

def list_users(collection):
    users = collection.find()
    for user in users:
        print(f"ID: {user['_id']}, Nombre: {user['name']}, Edad: {user['age']}")

def add_user(collection, name, age):
    user = {"name": name, "age": age}
    result = collection.insert_one(user)
    print(f"Usuario añadido con ID: {result.inserted_id}")

def update_user(collection, user_id, name, age):
    query = {"_id": ObjectId(user_id)}
    new_values = {"$set": {"name": name, "age": age}}
    result = collection.update_one(query, new_values)
    if result.matched_count > 0:
        print("Usuario actualizado correctamente.")
    else:
        print("Usuario no encontrado.")

def delete_user(collection, user_id):
    query = {"_id": ObjectId(user_id)}
    result = collection.delete_one(query)
    if result.deleted_count > 0:
        print("Usuario eliminado correctamente.")
    else:
        print("Usuario no encontrado.")

def main():
    parser = argparse.ArgumentParser(description="Gestión de usuarios en MongoDB")
    parser.add_argument("action", choices=["list", "add", "update", "delete"], help="Acción a realizar")
    parser.add_argument("--name", help="Nombre del usuario")
    parser.add_argument("--age", type=int, help="Edad del usuario")
    parser.add_argument("--id", help="ID del usuario (para actualizar o eliminar)")

    args = parser.parse_args()
    collection = connect_to_mongo()

    if args.action == "list":
        list_users(collection)
    elif args.action == "add":
        if args.name and args.age:
            add_user(collection, args.name, args.age)
        else:
            print("Debe proporcionar --name y --age para añadir un usuario.")
    elif args.action == "update":
        if args.id and args.name and args.age:
            update_user(collection, args.id, args.name, args.age)
        else:
            print("Debe proporcionar --id, --name y --age para actualizar un usuario.")
    elif args.action == "delete":
        if args.id:
            delete_user(collection, args.id)
        else:
            print("Debe proporcionar --id para eliminar un usuario.")

if __name__ == "__main__":
    main()

