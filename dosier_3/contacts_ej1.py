from flask import Flask, request, jsonify

app = Flask(__name__)

contacts = []

@app.route('/ej1/contacts', methods=['GET'])
def listContacts():
    return jsonify(contacts)

@app.route('/ej1/contacts', methods=['POST'])
def addContacts():
    contact = request.get_json()
    contacts.append(contact)
    return jsonify(contact), 201

@app.route('/ej1/contacts/<email>', methods=['PUT'])
def updateContacts(email):
    data = request.get_json()
    for contact in contacts:
        if contact.get('email') == email:
            contact.update(data)
            return jsonify(contact)
    return jsonify({'error': 'Contact not found'}), 404

@app.route('/ej1/contacts/<email>', methods=['DELETE'])
def deleteContacts(email):
    for i, contact in enumerate(contacts):
        if contact.get('email') == email:
            deleted = contacts.pop(i)
            return jsonify(deleted)
    return jsonify({'error': 'Contact not found'}), 404

app.run(debug=True)