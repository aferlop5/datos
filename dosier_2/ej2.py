import redis
import sys
import json

# Conexión a Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def list_users():
    """Lista todos los usuarios almacenados."""
    keys = redis_client.keys("user:*")
    if not keys:
        print("No hay usuarios registrados.")
        return
    for key in keys:
        user = redis_client.get(key)
        print(f"{key}: {user}")

def add_user(user_id, name, email):
    """Añade un nuevo usuario."""
    key = f"user:{user_id}"
    if redis_client.exists(key):
        print(f"El usuario con ID {user_id} ya existe.")
        return
    user_data = {"name": name, "email": email}
    redis_client.set(key, json.dumps(user_data))
    print(f"Usuario {user_id} añadido correctamente.")

def update_user(user_id, name=None, email=None):
    """Actualiza un usuario existente."""
    key = f"user:{user_id}"
    if not redis_client.exists(key):
        print(f"El usuario con ID {user_id} no existe.")
        return
    user_data = json.loads(redis_client.get(key))
    if name:
        user_data["name"] = name
    if email:
        user_data["email"] = email
    redis_client.set(key, json.dumps(user_data))
    print(f"Usuario {user_id} actualizado correctamente.")

def delete_user(user_id):
    """Elimina un usuario."""
    key = f"user:{user_id}"
    if not redis_client.exists(key):
        print(f"El usuario con ID {user_id} no existe.")
        return
    redis_client.delete(key)
    print(f"Usuario {user_id} eliminado correctamente.")

def main():
    """Función principal para manejar la CLI."""
    if len(sys.argv) < 2:
        print("Uso: python ej2.py <comando> [<args>]")
        print("Comandos disponibles: list, add, update, delete")
        return

    command = sys.argv[1]

    if command == "list":
        list_users()
    elif command == "add":
        if len(sys.argv) != 5:
            print("Uso: python ej2.py add <user_id> <name> <email>")
            return
        user_id, name, email = sys.argv[2], sys.argv[3], sys.argv[4]
        add_user(user_id, name, email)
    elif command == "update":
        if len(sys.argv) < 3:
            print("Uso: python ej2.py update <user_id> [<name>] [<email>]")
            return
        user_id = sys.argv[2]
        name = sys.argv[3] if len(sys.argv) > 3 else None
        email = sys.argv[4] if len(sys.argv) > 4 else None
        update_user(user_id, name, email)
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Uso: python ej2.py delete <user_id>")
            return
        user_id = sys.argv[2]
        delete_user(user_id)
    else:
        print(f"Comando desconocido: {command}")
        print("Comandos disponibles: list, add, update, delete")

if __name__ == "__main__":
    main()