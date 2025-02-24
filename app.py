from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    president = db.Column(db.String(255), nullable=False)
    officers = db.Column(db.Text, nullable=False)
    constitution = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "president": self.president,
            "officers": self.officers,
            "constitution": self.constitution
        }


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    return jsonify([org.to_dict() for org in organizations])


@app.route('/organizations', methods=['POST'])
def add_organization():
    data = request.json
    new_org = Organization(
        name=data["name"],
        president=data["president"],
        officers=data["officers"],
        constitution=data["constitution"]
    )
    db.session.add(new_org)
    db.session.commit()
    return jsonify(new_org.to_dict()), 201


@app.route('/organizations/<int:org_id>', methods=['PUT'])
def update_organization(org_id):
    data = request.json
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    org.name = data.get("name", org.name)
    org.president = data.get("president", org.president)
    org.officers = data.get("officers", org.officers)
    org.constitution = data.get("constitution", org.constitution)

    db.session.commit()
    return jsonify(org.to_dict())


@app.route('/organizations/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id):
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    db.session.delete(org)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
