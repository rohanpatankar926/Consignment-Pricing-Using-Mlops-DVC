
from site import abs_paths
from unittest import result
from flask import Flask,render_template
import os
import sys
from flask import send_file,abort
from subprocess import call

ROOT_DIR=os.getcwd()
LOGS_FOLDER_NAME="logs"
LOGS_DIR=os.path.join(ROOT_DIR,LOGS_FOLDER_NAME)

SAVED_MODELS_FOLDER_NAME="saved_models"
SAVED_MODEL_DIR=os.path.join(ROOT_DIR,SAVED_MODELS_FOLDER_NAME)


webapp_root="webapp"
static_dir=os.path.join(webapp_root,"static")
template_dir=os.path.join(webapp_root,"templates")

app=Flask(__name__,template_folder=template_dir,static_folder=static_dir)

@app.route("/",methods=["GET"])
def home_page():
	return render_template("index.html")

@app.route("/predict",methods=["POST","GET"])
def predict():
    return render_template("predict.html")

@app.route("/main",methods=["GET"])
def main():
    return render_template("main.html")

@app.route("/data",defaults={"req_path":"data"})
@app.route("/data/<path:req_path>")
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

@app.route('/train', methods=['GET', 'POST'])
def train():
    try:
        return_code = call(["python", "source/retraining_model.py"])
        print(return_code)
        return render_template('train.html')
    except FileNotFoundError as e:
        error="Error occured while retraining 🤔🤔"
        error={"error":error}
        return render_template("404.html",error=error)
port = int(os.environ.get("PORT", 5000))        
if __name__=="__main__":
    app.run(debug=True,port=port)
