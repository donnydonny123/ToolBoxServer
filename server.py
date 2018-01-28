from flask import Flask, send_from_directory, Response, jsonify
import os
import config
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/files")
def get_file_list():
    return jsonify(os.listdir(config.file_directory))

@app.route("/files/<filename>", methods=["GET"])
def get_file_by_name(filename):
    print(filename, os.listdir(config.file_directory))
    if filename in os.listdir(config.file_directory):
        return send_from_directory(directory=os.path.abspath(config.file_directory), filename=filename)
    else:
        return Response(
            filename + " is not found in the server\n",
            400,
            {'ContentType': 'application/json'}
        )



        
if __name__ == '__main__':
    app.run(host=config.bind_IP)