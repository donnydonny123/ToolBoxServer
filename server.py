from flask import Flask, send_from_directory, Response, jsonify, request
from functools import wraps
import os
import config
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"


# auth from http://flask.pocoo.org/snippets/8/
def check_auth(username, password):
    """This function is called to check if a username / password combination is valid."""
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/files")
@requires_auth
def get_file_list():
    return jsonify(os.listdir(config.file_directory))

@app.route("/files/<int:fileIndex>", methods=["GET"])
@requires_auth
def get_file_by_name(fileIndex):
    listOfFiles = os.listdir(config.file_directory)
    print(fileIndex, listOfFiles)
    if fileIndex < len(os.listdir(config.file_directory)):
        return send_from_directory(directory=os.path.abspath(config.file_directory), filename=listOfFiles[fileIndex])
    else:
        return Response(
            filename + " is not found in the server\n",
            400,
            {'ContentType': 'application/json'}
        )



        
if __name__ == '__main__':
    app.run(host=config.bind_IP)