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

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    privilege = db.Column(db.Boolean,default=False, nullable=False)
    # ^^ wether person has admin privileges or not ^^
    students = db.relationship('Student', backref='user', lazy=True)
    organizations = db.relationship('Organization', backref='president_user', lazy=True)

class Organization(db.Model):
    __tablename__ = 'organization'
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    missionvision = db.Column(db.Text, nullable=True)
    president = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    active = db.Column(db.Boolean, default=True, nullable=False)
    students = db.relationship('Student', backref='organization', lazy=True)

    def org_dict1(self): # for org list
        return {
            "org_id": self.org_id,
            "name": self.name,
            "president": self.president,
        }

    def org_dict2(self): # for org details
        return {
            "org_id": self.org_id,
            "name": self.name,
            "president": self.president,
            "missionvision": self.missionvision,
            "description": self.description,
            "active": self.active,
            "students": [student.sid for student in self.students]
        }
    
    

class Student(db.Model):
    __tablename__ = 'student'
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)


    
# class Organization(db.Model):
#     org_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     president = db.Column(db.String(255), nullable=False)
#     mav = db.Column(db.Text, nullable=False)
#     desc = db.Column(db.Text, nullable=False)
#     # Relationship with Student Table (One-to-Many)
#     students = db.relationship('Student', backref='organization', lazy=True)

# class Student(db.Model):
#     sid = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     role = db.Column(db.String(50), nullable=True)
#     org_id = db.Column(db.Integer, db.ForeignKey('org.id'), nullable=False)



        # RETURN MAIN PAGE
@app.route('/')
def home():
    return render_template('index.html')

        # GET ALL ORGANIZATIONS
@app.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.filter_by(active=True).all()
    return jsonify([org.org_dict1() for org in organizations])


@app.route('/organizations/<int:org_id>', methods=['GET'])
def get_organization(org_id):
    org = Organization.query.get(org_id)
    if not org or not org.active:
        return jsonify({"error": "Organization not found"}), 404
    return jsonify(org.org_dict2())  # Detailed view

        # ADD NEW ORGANIZATION  ---------------------------------- W.I.P
@app.route('/organizations', methods=['POST'])
def add_organization():
    data = request.json
    new_org = Organization(
        name=data["name"],
        president=int(data["president"]), # uses student id
        description="Description Placeholder, Please Update",
        missionvision="Mission and Vision Placeholder, Please Update"
    )
    db.session.add(new_org)
    db.session.commit()
    return jsonify(new_org.org_dict1()), 201

        # UPDATE BY ID          ---------------------------------- W.I.P
        # put the change ability to the organ page
@app.route('/organizations/<int:org_id>', methods=['PUT'])
def update_organization(org_id):
    data = request.json
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    org.name = data.get("name", org.name)
    org.president = data.get("president", org.president)

    db.session.commit()
    return jsonify(org.org_dict1())


        #  DELETE change to disable org instead of deleting entirely, add active boolean to org table 
# @app.route('/organizations/<int:org_id>', methods=['DELETE'])
# def delete_organization(org_id):
#     org = Organization.query.get(org_id)
#     if not org:
#         return jsonify({"error": "Organization not found"}), 404

#     db.session.delete(org)
#     db.session.commit()
#     return jsonify({"message": "Deleted successfully"})

@app.route('/organizations/<int:org_id>', methods=['DELETE'])
def delete_organization(org_id):
    org = Organization.query.get(org_id)
    if not org:
        return jsonify({"error": "Organization not found"}), 404

    org.active = False  # Soft delete
    db.session.commit()
    return jsonify({"message": "Organization deactivated"})

if __name__ == '__main__':
    app.run(debug=True)
