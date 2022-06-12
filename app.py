from itertools import count
import re
from flask import Flask,render_template,request,redirect,url_for,flash,request
import sqlalchemy
import os
import sys
from flask import send_file,abort
from subprocess import call
from time import sleep
from wsgiref import simple_server
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from datetime import datetime



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
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///consignment_price.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=0
app.config["SECRET_KEY"]="consignment_secret_key"

db=SQLAlchemy(app)
now=datetime.now()
db.create_all()
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

class User(db.Model):
    __tablename__="Consignment_Prices"
    id_=db.Column(db.Integer,primary_key=True)
    pq=db.Column(db.Integer,index=True)
    Po_SO=db.Column(db.Integer,index=True)
    Asn_dn=db.Column(db.String(50))
    country=db.Column(db.String(50))
    managed_by=db.Column(db.String(50))
    fullfil_via=db.Column(db.String(50))
    vendor_inco_term=db.Column(db.String(50))
    shipment_mode=db.Column(db.String(10))
    pq_client_date=db.Column(db.DateTime())
    Scheduled_Delivery_Date=db.Column(db.DateTime())
    delivered_client_date=db.Column(db.DateTime())
    delivery_recorded_date=db.Column(db.DateTime())
    product_group=db.Column(db.String(50))
    sub_classification=db.Column(db.String(50))
    vendor=db.Column(db.String(50))
    item_descr=db.Column(db.String(100))
    molecular_test=db.Column(db.String(50))
    brand=db.Column(db.String(50))
    dosage=db.Column(db.String(40))
    dosage_form=db.Column(db.String(40))
    unit_of_measure=db.Column(db.Integer)
    line_item_quantity=db.Column(db.Integer)
    line_item_value=db.Column(db.Integer)
    pack_price=db.Column(db.Integer)
    unit_price=db.Column(db.Integer)
    manufacturing_site=db.Column(db.Integer)
    first_line_designation=db.Column(db.Integer)
    weight_product=db.Column(db.Integer)
    freight_cost=db.Column(db.Integer)
    line_item_insurance=db.Column(db.Integer())
   
@app.route("/predict/upload",methods=["POST","GET"])
def upload():
   
    if request.method=="POST":
        if not request.form["pq"] or not request.form["poso"]:
            flash("Something Went Wrong While updating data to DataBase!!!")
        else:
            upload_to_db=User(pq=request.form["pq"],Po_SO=request.form["poso"])
            db.session.add(upload_to_db)
            db.session.commit()
            flash("Successfully Uploaded Data To DataBase😁😁")
            return redirect(("/predict/upload"))
    return render_template("db.html")
    


    
    
    

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
    db.create_all()
    app.run(port=port,debug=True)