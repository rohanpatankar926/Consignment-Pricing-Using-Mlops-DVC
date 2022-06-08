from flask import Flask,render_template,request,redirect,url_for,flash
import os
import sys
from flask import send_file,abort
from subprocess import call
from time import sleep
from wsgiref import simple_server
from flask_cors import CORS, cross_origin
ROOT_DIR=os.getcwd()
LOGS_FOLDER_NAME="logs"
LOGS_DIR=os.path.join(ROOT_DIR,LOGS_FOLDER_NAME)

SAVED_MODELS_FOLDER_NAME="saved_models"
SAVED_MODEL_DIR=os.path.join(ROOT_DIR,SAVED_MODELS_FOLDER_NAME)


webapp_root="webapp"
static_dir=os.path.join(webapp_root,"static")
template_dir=os.path.join(webapp_root,"templates")

app=Flask(__name__,template_folder=template_dir,static_folder=static_dir)
CORS(app)

@app.route("/",methods=["GET"])
@cross_origin()
def home_page():
	return render_template("index.html")

@app.route("/predict",methods=["POST","GET"])
@cross_origin()
def predict():
    return render_template("predict.html")

@app.route("/main",methods=["GET"])
@cross_origin()
def main():
    return render_template("main.html")

@app.route("/noaccess",methods=["GET"])
@cross_origin()
def no_access():
    return render_template("contact_me.html")

@app.route("/data",defaults={"req_path":"data"})
@app.route("/data/<path:req_path>")
@cross_origin()
def get_data(req_path):
    try:
        os.makedirs("data",exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path=os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files={os.path.join(abs_path,file):file for file in os.listdir(abs_path)}
        result={
            "files":files,
            "parent_folder":os.path.dirname(abs_path),
            "parent_label":abs_path
        }
        return render_template("files.html",result=result)
    except Exception as e:
        error="Error occured while getting the data"
        error={"error":error}
        return render_template("404.html",error=error)
    
@app.route("/saved_models",defaults={"req_path":"saved_models"})
@app.route("/saved_models/<path:req_path>")
@cross_origin()
def saved_models(req_path):
    try:
        os.makedirs("saved_models",exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path=os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files={os.path.join(abs_path,file):file for file in os.listdir(abs_path)}
        result={
            "files":files,
            "parent_folder":os.path.dirname(abs_path),
            "parent_label":abs_path
        }
        return render_template("saved_models_files.html",result=result)
    except Exception as e:
        error="Error occured while getting the saved models 🤔🤔"
        error={"error":error}
        return render_template("404.html",error=error)
    
    
@app.route("/performance",defaults={"req_path":"reports"})
@app.route("/performance/<path:req_path>")
@cross_origin()
def performance(req_path):
    try:
        os.makedirs("reports",exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path=os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files={os.path.join(abs_path,file):file for file in os.listdir(abs_path)}
        result={
            "files":files,
            "parent_folder":os.path.dirname(abs_path),
            "parent_label":abs_path
        }
        return render_template("performance.html",result=result)
    except Exception as e:
        error="Error occured while getting the saved models 🤔🤔"
        error={"error":error}
        return render_template("404.html",error=error)
    
    
    
@app.route("/logs",defaults={"req_path":"logs"})
@app.route("/logs/<path:req_path>")
@cross_origin()
def get_logs(req_path):
    try:
        os.makedirs("logs",exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path=os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files={os.path.join(abs_path,file):file for file in os.listdir(abs_path)}
        result={
            "files":files,
            "parent_folder":os.path.dirname(abs_path),
            "parent_label":abs_path
        }
        return render_template("log_files.html",result=result)
    except Exception as e:
        error="Error occured while getting the log files 🤔🤔"
        error={"error":error}
        return render_template("404.html",error=error)

@app.route('/stream', methods=['GET', 'POST'])
@cross_origin()
def stream():
    def generate():
            with open('logs/logs.log') as f:
                while 1:
                    yield f.read()
                    sleep(0.1)
    return app.response_class(generate(),mimetype="text/plain")

@app.route('/stream/train', methods=['GET', 'POST'])
@cross_origin()
def train():
    try:
       
        return_code = call(["python", "source/run_all_logs_scipt.py"])
        print(return_code)
        return render_template('train.html')
    except FileNotFoundError as e:
        error="Error occured while retraining 🤔🤔"
        error={"error":error}
        return render_template("404.html",error=error)
    

port = int(os.getenv("PORT", 5000))
if __name__=="__main__":
    host="127.0.0.1"
    https=simple_server.make_server(host,port,app)
    https.serve_forever()