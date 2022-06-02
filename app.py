
from site import abs_paths
from unittest import result
from flask import Flask,render_template
import os
import sys
from flask import send_file,abort

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


@app.route("/saved_models",defaults={"req_path":"saved_models"})
@app.route("/saved_models/<path:req_path>")
def saved_models(req_path):
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

@app.route("/logs",defaults={"req_path":"logs"})
@app.route("/logs/<path:req_path>")
def get_logs(req_path):
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

@app.route('/train', methods=['GET', 'POST'])
def train():
    from subprocess import call
    return_code = call(["python", "source/retraining_model.py"])
    print(return_code)
    return render_template('train.html')


if __name__=="__main__":
    app.run(debug=True,port=5000)
