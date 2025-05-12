import sys
import pymongo
import argparse
from bson import ObjectId

def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["ej3_db"]
    users_collection = db["users"]
    contacts_collection = db["contacts"]
    return users_collection, contacts_collection

def list_users_and_contacts(users_collection, contacts_collection):
    users = users_collection.find()
    for user in users:
        print(f"Usuario ID: {user['_id']}, Nombre: {user['name']}, Edad: {user['age']}")
        contacts = contacts_collection.find({"user_id": user["_id"]})
        for contact in contacts:
            print(f"  Contacto ID: {contact['_id']}, Nombre: {contact['name']}, Teléfono: {contact['phone']}")

def add_user(users_collection, name, age):
    user = {"name": name, "age": age}
    result = users_collection.insert_one(user)
    print(f"Usuario añadido con ID: {result.inserted_id}")

def update_user(users_collection, user_id, name, age):
    query = {"_id": ObjectId(user_id)}
    new_values = {"$set": {"name": name, "age": age}}
    result = users_collection.update_one(query, new_values)
    if result.matched_count > 0:
        print("Usuario actualizado correctamente.")
    else:
        print("Usuario no encontrado.")

def delete_user(users_collection, contacts_collection, user_id):
    query = {"_id": ObjectId(user_id)}
    result = users_collection.delete_one(query)
    if result.deleted_count > 0:
        contacts_collection.delete_many({"user_id": ObjectId(user_id)})
        print("Usuario y sus contactos eliminados correctamente.")
    else:
        print("Usuario no encontrado.")

def add_contact(contacts_collection, user_id, name, phone):
    contact = {"user_id": ObjectId(user_id), "name": name, "phone": phone}
    result = contacts_collection.insert_one(contact)
    print(f"Contacto añadido con ID: {result.inserted_id}")

def update_contact(contacts_collection, contact_id, name, phone):
    query = {"_id": ObjectId(contact_id)}
    new_values = {"$set": {"name": name, "phone": phone}}
    result = contacts_collection.update_one(query, new_values)
    if result.matched_count > 0:
        print("Contacto actualizado correctamente.")
    else:
        print("Contacto no encontrado.")

def delete_contact(contacts_collection, contact_id):
    query = {"_id": ObjectId(contact_id)}
    result = contacts_collection.delete_one(query)
    if result.deleted_count > 0:
        print("Contacto eliminado correctamente.")
    else:
        print("Contacto no encontrado.")

def main():
    parser = argparse.ArgumentParser(description="Gestión de usuarios y contactos en MongoDB")
    parser.add_argument("action", choices=["list", "add_user", "update_user", "delete_user", "add_contact", "update_contact", "delete_contact"], help="Acción a realizar")
    parser.add_argument("--user_id", help="ID del usuario (para contactos o actualizar/eliminar usuario)")
    parser.add_argument("--contact_id", help="ID del contacto (para actualizar/eliminar contacto)")
    parser.add_argument("--name", help="Nombre del usuario o contacto")
    parser.add_argument("--age", type=int, help="Edad del usuario")
    parser.add_argument("--phone", help="Teléfono del contacto")

    args = parser.parse_args()
    users_collection, contacts_collection = connect_to_mongo()

    if args.action == "list":
        list_users_and_contacts(users_collection, contacts_collection)
    elif args.action == "add_user":
        if args.name and args.age:
            add_user(users_collection, args.name, args.age)
        else:
            print("Debe proporcionar --name y --age para añadir un usuario.")
    elif args.action == "update_user":
        if args.user_id and args.name and args.age:
            update_user(users_collection, args.user_id, args.name, args.age)
        else:
            print("Debe proporcionar --user_id, --name y --age para actualizar un usuario.")
    elif args.action == "delete_user":
        if args.user_id:
            delete_user(users_collection, contacts_collection, args.user_id)
        else:
            print("Debe proporcionar --user_id para eliminar un usuario.")
    elif args.action == "add_contact":
        if args.user_id and args.name and args.phone:
            add_contact(contacts_collection, args.user_id, args.name, args.phone)
        else:
            print("Debe proporcionar --user_id, --name y --phone para añadir un contacto.")
    elif args.action == "update_contact":
        if args.contact_id and args.name and args.phone:
            update_contact(contacts_collection, args.contact_id, args.name, args.phone)
        else:
            print("Debe proporcionar --contact_id, --name y --phone para actualizar un contacto.")
    elif args.action == "delete_contact":
        if args.contact_id:
            delete_contact(contacts_collection, args.contact_id)
        else:
            print("Debe proporcionar --contact_id para eliminar un contacto.")

if __name__ == "__main__":
    main()