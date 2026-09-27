from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from functools import wraps
import os
load_dotenv()
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
API_TOKEN=os.getenv("API_TOKEN")
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(150),unique=True,nullable=False)
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email
        }
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth_header=request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error":"Authorization header required"}),401
        parts=auth_header.split()
        if len(parts)!=2 or parts[0]!="Bearer":
            return jsonify({
                "error":"Authorization header required"
            }),401
        if parts[1]!=API_TOKEN:
            return jsonify({"error":"Invalid Authorization format"}),401
        return f(*args,**kwargs)
    return decorated
@app.route("/users", methods=["POST"])
@token_required
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "name and email are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 409

    user = User(
        name=name,
        email=email
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": user.to_dict()
    }), 201
@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify([
        user.to_dict()
        for user in users
    ])
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(user.to_dict())
@app.route("/users/<int:user_id>", methods=["DELETE"])
@token_required
def delete_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "User deleted"
    })

@app.route("/health")
def health():

    return jsonify({
        "service": "user-service",
        "status": "UP"
    })


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(port=5002, debug=True)