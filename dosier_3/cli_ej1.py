import requests

BASE = "http://localhost:5000/ej1/contacts"

resp = requests.get(BASE)
print("LISTAR:", resp.json())


contact = {"email": "a", "name": "a", "surname": "a"}
resp = requests.post(BASE, json=contact)
print("CREAR:", resp.json())


update = {"name": "nuevo_nombre", "surname": "nuevo_apellido"}
resp = requests.put(f"{BASE}/a", json=update)
print("ACTUALIZAR:", resp.json())


resp = requests.delete(f"{BASE}/a")
print("ELIMINAR:", resp.json())


resp = requests.get(BASE)
print("LISTAR FINAL:", resp.json())