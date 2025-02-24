from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

# In-memory storage (can be replaced with a JSON file)
organizations = [
    {"id": 1, "name": "Sample Organization", "president": "Kyle Pimentel", "officers": "Dave, Justine, Myless", "constitution": "Link to Constitution"}
]

# Home route to serve HTML
@app.route('/')
def home():
    return render_template('index.html')

# GET all organizations
@app.route('/organizations', methods=['GET'])
def get_organizations():
    return jsonify(organizations)

# CREATE a new organization
@app.route('/organizations', methods=['POST'])
def add_organization():
    data = request.json
    new_org = {
        "id": len(organizations) + 1,
        "name": data["name"],
        "president": data["president"],
        "officers": data["officers"],
        "constitution": data["constitution"]
    }
    organizations.append(new_org)
    return jsonify(new_org), 201

# UPDATE an organization
@app.route('/organizations/<int:org_id>', methods=['PUT'])
def update_organization(org_id):
    data = request.json
    for org in organizations:
        if org["id"] == org_id:
            org.update(data)
            return jsonify(org)
    return jsonify({"error": "Organization not found"}), 404

# DELETE an organization
@app.route('/organizations/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id):
    global organizations
    organizations = [org for org in organizations if org["id"] != org_id]
    return jsonify({"message": "Deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
