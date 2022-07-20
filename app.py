from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'planets.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{ os.path.join(basedir, 'planets.db')}"

db = SQLAlchemy(app)


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

    db.session.add(mercury)

    test_user = User(first_name="Praveen",
                     last_name="Kumar",
                     password="2323",
                     email="abc@gmail.com")
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


if __name__ == '__main__':
    app.run(debug=True)
