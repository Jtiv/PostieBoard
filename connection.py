import datetime
from peewee import *
from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict, dict_to_model


db = PostgresqlDatabase('pstboard', user='jamesthompson', password='12345', host='localhost')

db.connect()

class BaseModel(Model):
    class Meta:
        database = db

class Postie(BaseModel):
    poster = CharField()
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)

db.create_tables([Postie])

firstPost = Postie(poster='James', message='first post, welcome to the baords!')
firstPost.save()

app = Flask(__name__)

@app.route('/postie/', methods=['GET', 'POST'])
@app.route('/postie/<id>', methods=['GET', 'PUT', 'DELETE'])

def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Postie.get(Postie.id == id)))
        else:
            postieList = []
            for postie in Postie.select():
                postieList.append(model_to_dict(postie))
            return jsonify(postieList)
    
    if request.method == 'PUT':
        return 'PUT request'

    if request.method == 'POST':
        new_postie = dict_to_model(Postie, request.get_json())
        new_postie.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        return 'DELETE request'


app.run(debug=True)



