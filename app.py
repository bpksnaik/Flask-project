from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'planets.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'planets.db')}"

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command("db_create")
def db_create():
    db.create_all()
    print("db created")


@app.cli.command("db_drop")
def db_drop():
    db.drop_all()
    print("db droped")


@app.cli.command("db_seed")
def db_seed():
    mercury = Planets(planet_name="Mercury",
                      planet_type="Class D",
                      home_star="Solr",
                      mass=3.25e25,
                      radius=1516)

    venus = Planets(planet_name="Venus",
                    planet_type="Class D",
                    home_star="Solr",
                    mass=3.25e25,
                    radius=1516)

    db.session.add(mercury)
    db.session.add(venus)

    test_user = User(first_name="Praveen",
                     last_name="Kumar",
                     password="2323",
                     email="ab@gmail.com")
    db.session.add(test_user)
    db.session.commit()
    print("Db seeded")


@app.route('/welcome')
def hello():
    return jsonify(message="Hello world!"), 201


# getting url parameter
@app.route("/param")
def welcome() -> str:
    name = request.args.get("name")
    age = request.args.get("age")
    return f"Hi boss {name} ur {age} old"


# getting url variable
@app.route("/url_variable/<string:name>/<int:age>")
def url_variables(name: str, age: int) -> jsonify:
    return jsonify(name=name, age=age), 200  # by default


# retrieving data from sqlite db
@app.route("/planets", methods=["GET"])
def plantes():
    plantes_list = Planets.query.all()
    # return jsonify(data=plantes_list)
    result = planets_schema.dump(plantes_list)
    return jsonify(result)


@app.route("/users", methods=["GET"])
def users():
    user_list = User.query.all()
    # return jsonify(data=plantes_list)
    result = user_schema.dump(user_list)
    return jsonify(result.data)


#  Database Models
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planets(db.Model):
    __tablename__ = "planets"
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)


# Schema for database tables
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius')


# creating user instance from UserSchema class
user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
