import uuid;
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_cors import CORS
from flask_uuid import FlaskUUID
app = Flask(__name__)
FlaskUUID(app)
CORS(app)

messages = [{
    'id' :uuid.uuid4(),
    'name': u'Tanya',
    'message': u'Nestle, Milkibar, Dairy Milk'
}]
#

@app.route('/hse_board/messages/<uuid:message_id>', methods = ['DELETE'])
def delete_message(message_id):
    message = filter(lambda t: t['id'] == message_id, messages)
    if len(message) == 0:
        abort(400)

    messages.remove(message[0])
    return jsonify({ 'result': True })


@app.route('/hse_board/messages', methods = ['POST'])
def create_message():
    if not request.json or not 'name' in request.json:
        abort(400)
    message = {
        'id': uuid.uuid4(),
        'name': request.json['name'],
        'message': request.json.get('message', "")
    }
    messages.insert(0, message)
    return jsonify({ 'message' : message }) ,201


@app.route('/hse_board/messages', methods = ['GET'])
def get_messages():
    return jsonify({ 'messages' :  messages })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({ 'error' : 'Not Found' }), 404)

if __name__ == '__main__':
    app.run(debug = True)
