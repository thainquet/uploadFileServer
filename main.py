import flask
from flask import request, jsonify, make_response, send_from_directory
from pathlib import Path
import os, time, math, shutil

def getThisDir():
    return Path(__file__).parents[0]

path = str(getThisDir()).replace("\\","/") + "/upload"


def create_app():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    app.config["UPLOAD_FOLDER"] = path

    @app.route('/', methods=['GET'])
    def home():   
        print(path, flush=True)
        return "Hello, flask app works ! - Thainq"

    
    @app.route('/download/<path:filename>', methods=['GET'])
    def download(filename):
        dir = path
        return send_from_directory(dir, filename, as_attachment=True)

        
    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files["fileToUpload"]
        filename = file.filename
        # check duplicate
        pathToNewFile = path + "/" + filename

        file.save(pathToNewFile)
        data = []

        name = filename
        size = round(os.path.getsize(pathToNewFile) / 1024, 2)
        date = time.strftime('%d/%m/%Y',time.gmtime(os.path.getmtime(pathToNewFile)))
        data.append({"fileName" : name, "fileSize": size, "filePath": pathToNewFile, "fileDate": date})
        
        resp = make_response(jsonify({"message": "ok", "data": data}), 200)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Credentials'] = "true"

        return resp

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')