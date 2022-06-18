import pyrebase
from flask import Flask, render_template, request, redirect, flash, request, session, url_for
import os
import sys
from flask import send_file, abort
from subprocess import call
from time import sleep
from wsgiref import simple_server
from flask_pymongo import PyMongo
import bcrypt
from flask_cors import CORS, cross_origin
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.engine import Engine
from datetime import datetime

ROOT_DIR = os.getcwd()
LOGS_FOLDER_NAME = "logs"
LOGS_DIR = os.path.join(ROOT_DIR, LOGS_FOLDER_NAME)

SAVED_MODELS_FOLDER_NAME = "saved_models"
SAVED_MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_FOLDER_NAME)


webapp_root = "webapp"
static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")


# firebase credentials
config = {
    "apiKey": "AIzaSyCC2_6DhJNzDo-ZbXWjxEedjlhm5OF42Iw",
    "authDomain": "consignmentpricing-1d67d.firebaseapp.com",
    "databaseURL": "https://consignmentpricing-1d67d-default-rtdb.firebaseio.com",
    "projectId": "consignmentpricing-1d67d",
    "storageBucket": "consignmentpricing-1d67d.appspot.com",
    "messagingSenderId": "56086969545",
    "appId": "1:56086969545:web:4c71167bc4821c28b5e118",
    "measurementId": "G-7WWLJ9W8JM"
}

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

CORS(app)
app.config["SECRET_KEY"] = "consignment_secret_key"
app.config["MONGO_DBNAME"] = "ConsignmentPricing"
app.config["MONGO_URI"] = "mongodb+srv://rohan:sAx4GTTSPKXcvTfY@consignment.blgtz.mongodb.net/ConsignmentPricing"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///consignment_price.sqlite3"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# db = SQLAlchemy(app)
# now = datetime.now()
# db.create_all()
mongo_ = PyMongo(app)



# LOGIN SYSTEM
@app.route("/")
@cross_origin()
def index():
    if "username" in session:
        return (f"You are logged in as {session['username']}")
    else:
        return render_template("login.html")



@app.route('/login', methods=['POST'])
def login():
    users = mongo_.db.consignmentdata
    login_user = users.find_one({'email' : request.form['email']})
    if login_user:
        email=request.form['email']
        if bcrypt.hashpw(request.form['password'].encode("utf-8"), login_user['password']) == login_user['password']:
            session['email']= email
            return redirect(url_for('home_page')) 
    if  request.form["email"]=="" and request.form["password"]=="":
        flash("Please Fill your username/password")
        return redirect(url_for('index'))
    else:
        flash("Invalid username/password")
        return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo_.db.consignmentdata
        existing_user = users.find_one({'email' : request.form['email']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'email' : request.form['email'], 'username': request.form['username'],'password' : hashpass})
            session['email'] = request.form['email']
            flash("Registered Successfully")
            return redirect(url_for('index'))
        flash("Email already exists")
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("logged out successfully")
    return redirect(url_for('index'))

@app.route("/home", methods=["GET"])
@cross_origin()
def home_page():
    return render_template("index.html")


@app.route("/predict", methods=["POST", "GET"])
@cross_origin()
def predict():
    return render_template("predict.html")


@app.route("/main", methods=["GET"])
@cross_origin()
def main():
    return render_template("main.html")


@app.route("/noaccess", methods=["GET"])
@cross_origin()
def no_access():
    return render_template("contact_me.html")


@app.route("/data", defaults={"req_path": "data"})
@app.route("/data/<path:req_path>")
@cross_origin()
def get_data(req_path):
    try:
        os.makedirs("data", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file)
                              : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("files.html", result=result)
    except Exception as e:
        error = "Error occured while getting the data"
        error = {"error": error}
        return render_template("404.html", error=error)


@app.route("/saved_models", defaults={"req_path": "saved_models"})
@app.route("/saved_models/<path:req_path>")
@cross_origin()
def saved_models(req_path):
    try:
        os.makedirs("saved_models", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file)
                              : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("saved_models_files.html", result=result)
    except Exception as e:
        error = "Error occured while getting the saved models 🤔🤔"
        error = {"error": error}
        return render_template("404.html", error=error)


@app.route("/performance", defaults={"req_path": "reports"})
@app.route("/performance/<path:req_path>")
@cross_origin()
def performance(req_path):
    try:
        os.makedirs("reports", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file)
                              : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("performance.html", result=result)
    except Exception as e:
        error = "Error occured while getting the saved models 🤔🤔"
        error = {"error": error}
        return render_template("404.html", error=error)


@app.route("/logs", defaults={"req_path": "logs"})
@app.route("/logs/<path:req_path>")
@cross_origin()
def get_logs(req_path):
    try:
        os.makedirs("logs", exist_ok=True)
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        if not os.path.exists(abs_path):
            abort(404)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = {os.path.join(abs_path, file)
                              : file for file in os.listdir(abs_path)}
        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template("log_files.html", result=result)
    except Exception as e:
        error = "Error occured while getting the log files 🤔🤔"
        error = {"error": error}
        return render_template("404.html", error=error)


@app.route('/stream/train', methods=['GET', 'POST'])
@cross_origin()
def train():
    try:
        return_code = call(["python", "src/run_all_scipts.py"])
        print(return_code)
        return render_template('train.html')
    except FileNotFoundError as e:
        error = "Error occured while retraining 🤔🤔"
        error = {"error": error}
        return render_template("404.html", error=error)


LOG_DIR = "logs"
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y_%m_%d_%H')}"
file_name = f"log_{CURRENT_TIME_STAMP}.log"
log_file_path = os.path.join(LOG_DIR, file_name)


@app.route('/stream', methods=['POST', 'GET'])
@cross_origin()
def stream():
    try:
        def generate():
            with open(log_file_path, "r") as f:
                while True:
                    yield f.read()
                    sleep(0.1)
        return app.response_class(generate(), mimetype="text/plain")
    except Exception as e:
        print(e)

# class User(db.Model):
#     __tablename__ = "Consignment_Prices"
#     id_ = db.Column(db.Integer, primary_key=True)
#     pq = db.Column(db.String(50), index=True)
#     Po_SO = db.Column(db.String(50), index=True)
#     Asn_dn = db.Column(db.String(50), index=True)
#     country = db.Column(db.String(50), index=True)
#     managed_by = db.Column(db.String(50), index=True)
#     fullfil_via = db.Column(db.String(50), index=True)
#     vendor_inco_term = db.Column(db.String(50), index=True)
#     shipment_mode = db.Column(db.String(10), index=True)
#     pq_client_date = db.Column(db.String, index=True)
#     Scheduled_Delivery_Date = db.Column(db.String, index=True)
#     delivered_client_date = db.Column(db.String, index=True)
#     delivery_recorded_date = db.Column(db.String, index=True)
#     product_group = db.Column(db.String(50), index=True)
#     sub_classification = db.Column(db.String(50), index=True)
#     vendor = db.Column(db.String(50), index=True)
#     item_descr = db.Column(db.String(100), index=True)
#     molecular_test = db.Column(db.String(50), index=True)
#     brand = db.Column(db.String(50), index=True)
#     dosage = db.Column(db.String(40), index=True)
#     dosage_form = db.Column(db.String(40), index=True)
#     unit_of_measure = db.Column(db.Integer, index=True)
#     line_item_quantity = db.Column(db.Integer, index=True)
#     line_item_value = db.Column(db.Integer, index=True)
#     pack_price = db.Column(db.Integer, index=True)
#     unit_price = db.Column(db.Integer, index=True)
#     manufacturing_site = db.Column(db.Integer, index=True)
#     first_line_designation = db.Column(db.Integer, index=True)
#     weight_product = db.Column(db.Integer, index=True)
#     freight_cost = db.Column(db.Integer, index=True)
#     line_item_insurance = db.Column(db.Integer, index=True)


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if not request.form["pq"] or not request.form["poso"]:
            flash("Something went wrong while uploading data to database!!!")
        else:
            # Firebase database setup
            firebase = pyrebase.initialize_app(config)
            database = firebase.database()
            data = {"pq": request.form["pq"], "Po_SO": request.form["poso"], "Asn_dn": request.form.get("asndn"), "country": request.form.get("country"), "managed_by": request.form.get("managedby"), "fullfil_via": request.form.get("fulfil_via"), "vendor_inco_term": request.form.get("vendor"), "shipment_mode": request.form.get("shipment_mode"), "pq_client_date": request.form.get("pqdate"), "Scheduled_Delivery_Date": request.form.get("scheduled_delivery_date"), "delivered_client_date": request.form.get("delivery_client_date"), "delivery_recorded_date": request.form.get("delivery_recorded_date"), "product_group": request.form.get("product_group"), "sub_classification": request.form.get("sub_classification"), "vendor": request.form.get("vendor"), "item_descr": request.form.get(
                "item_desc"), "molecular_test": request.form.get("molecular_test"), "brand": request.form.get("brand"), "dosage": request.form.get("dosage"), "dosage_form": request.form.get("dosage_form"), "unit_of_measure": request.form.get("unit_of_measure"), "line_item_quantity": request.form.get("line_item_quantity"), "line_item_value": request.form.get("line_item_value"), "pack_price": request.form.get("pack_price"), "unit_price": request.form.get("unit_price"), "manufacturing_site": request.form.get("manufacturing_site"), "first_line_designation": request.form.get("first_line_designation"), "weight_product": request.form.get("weight_product"), "freight_cost": request.form.get("freight_cost"), "line_item_insurance": request.form.get("line_item_insurance")}
            database.push(data)
            flash("Successfully Uploaded Data To DataBase...😉")
            return redirect(("/upload"))
        return render_template("db.html")
    else:
        return render_template("db.html")


port = int(os.getenv("PORT", 8100))
if __name__ == "__main__":
    app.config["SECRET_KEY"] = "!@##$#!#EDS#@!df"
    # db.create_all()
    stream
    train
    app.run(port=port,debug=True,host="0.0.0.0")
