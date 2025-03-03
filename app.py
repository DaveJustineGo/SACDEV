from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

        # SET UP DATABASE
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

        # CREATE TABLE OBJECT for database
class Organization(db.Model):
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    president = db.Column(db.String(255), nullable=False)
    mav = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    # Relationship with Student Table (One-to-Many)
    students = db.relationship('Student', backref='organization', lazy=True)

class Student(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=True)
    org_id = db.Column(db.Integer, db.ForeignKey('org.id'), nullable=False)

def org_dict1(self):
    return {
        "org_id": self.id,
        "name": self.name,
        "president": self.president,
    }

def org_dict2(self):
    return {
        "org_id": self.id,
        "name": self.name,
        "president": self.president,
    }

        # RETURN MAIN PAGE
@app.route('/')
def home():
    return render_template('index.html')

        # GET ALL ORGANIZATIONS
@app.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    return jsonify([org.org_dict1() for org in organizations])

        # ADD NEW ORGANIZATION
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
    return jsonify(new_org.org_dict1()), 201

        # UPDATE BY ID
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
    return jsonify(org.org_dict1())


        #  DELETE
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
