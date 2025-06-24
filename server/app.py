from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200


@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    new_message = Message(
        body=data.get('body'),
        username=data.get('username'),
        created_at=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def patch_message(id):
    message = db.session.get(Message, id)
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    if "body" in data:
        message.body = data["body"]
    db.session.commit()
    return jsonify(message.to_dict()), 200


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if not message:
        return {"error": "Message not found"}, 404

    db.session.delete(message)
    db.session.commit()
    return {}, 204


if __name__ == '__main__':
    app.run(port=5555, debug=True)
