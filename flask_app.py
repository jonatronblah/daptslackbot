from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import pandas as pd

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="<db username>",
    password="<db password>",
    hostname="<db host>",
    databasename="<db name>",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Mesage(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    user = db.Column(db.String(4096))
    content = db.Column(db.String(4096))


#messages_df = pd.read_sql('SELECT * FROM messages', db.session.bind)

@app.route('/')
def index():
    #messages_df.to_csv('~/msg_out.csv')
    return render_template("index.html")



@app.route('/slack', methods=['POST'])
def inbound():
    #use this to authenticate:
    #if request.json:
        #return jsonify(request.json)
    webhook_url = '<webhook url>'
    payload = request.get_json(force=True)
    userload = payload['event']['user']
    contentload = payload['event']['text']
    timeload = payload['event_time']
    if "the channel" in contentload:
        return None
    else:
        dbpayload = Mesage(user=userload, content=contentload, time=timeload)
        db.session.add(dbpayload)
        db.session.commit()
        response = requests.post(
                webhook_url, data=json.dumps({'text': 'i just recorded someones message'}),
                headers={'Content-Type': 'application/json'}
                )
    return Response(), 200





if __name__ == "__main__":
    app.run(port=8000, debug=False)
