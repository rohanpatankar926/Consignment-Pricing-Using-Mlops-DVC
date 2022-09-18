import pyrebase
from flask import Flask, render_template, request, redirect, flash, request, session,url_for
import os
import sys
from flask import send_file, abort
from subprocess import call
from time import sleep
from wsgiref import simple_server
from flask_pymongo import PyMongo
import bcrypt
from call import Call
from functools import wraps
from predictor.predictor import ConsignmentData, ConsignmentPredictor
from flask_cors import CORS, cross_origin
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.engine import Engine
from datetime import datetime
import mlflow
import flask_monitoringdashboard as dashboard
dashboard.config.init_from(envvar='FLASK_MONITORING_DASHBOARD_CONFIG',file='config.cfg')

ROOT_DIR = os.getcwd()
SAVED_MODELS_DIR_NAME = "H:/consignment pricing using mlops/saved_models/"
CONSIGNMENT_DATA_KEY = "consignment_data"
LINE_ITEM_VALUE_KEY = "line_item_value"
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
ROOT_DIR = os.getcwd()
LOGS_FOLDER_NAME = "logs"
LOGS_DIR = os.path.join(ROOT_DIR, LOGS_FOLDER_NAME)


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
dashboard.bind(app)
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


def login_required(f):
    @wraps(f)
    def not_to_redirect(*args, **kwargs):
        if  "email" not in session:
            return render_template("login.html")
        return f(*args, **kwargs)
    return not_to_redirect



# LOGIN SYSTEM
@app.route("/")
@cross_origin()
def index():
    if "email" not in session:
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    users = mongo_.db.consignmentdata
    login_user = users.find_one({'email': request.form['email']})
    if login_user:
        next_url = request.form.get("next")
        email = request.form['email']
        if bcrypt.hashpw(request.form['password'].encode("utf-8"), login_user['password']) == login_user['password']:
            session['email'] = email
            if next_url:
                return redirect(next_url)
            return redirect(url_for('home_page'))
    if request.form["email"] == "" and request.form["password"] == "":
        flash("Please Fill your username/password")
        return render_template("login.html")
    else:
        flash("Invalid username/password")
        return redirect(url_for("index"))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo_.db.consignmentdata
        existing_user = users.find_one({'email': request.form['email']})
        if len(request.form["password"]) < 6:
            flash("alert: Please Enter a password of atleast 6 characters", "success")
            return redirect(url_for("register"))
        if request.form["password"] != request.form["cpassword"]:
            flash("pwd: Passwords do not match!", "alert")
            return redirect(url_for("register"))
        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one(
                {'email': request.form['email'], 'username': request.form['username'], 'password': hashpass})
            session['email'] = request.form['email']
            flash("Registered Successfully", "success")
            return redirect(url_for('index'))
        flash("alert: Email already exists", "success")
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("logged out successfully", "success")
    return render_template("login.html")


@app.route("/home", methods=["GET"])
@login_required
@cross_origin()
def home_page():
    return render_template("index.html")

# @app.route("/predict", methods=["POST", "GET"])
# @cross_origin()
# def predict():
#     return render_template("predict.html")


@app.route("/main", methods=["GET"])
@login_required
@cross_origin()
def main():
    return render_template("main.html")


@app.route("/predict", methods=["POST", "GET"])
@login_required
@cross_origin()
def predict():
    context = {
        CONSIGNMENT_DATA_KEY: None,
        LINE_ITEM_VALUE_KEY: None}
    if request.method == "POST":
        line_item_insurance = float(request.form.get("line_item_insurance"))
        line_item_quantity = float(request.form.get("line_item_quantity"))
        pack_price = float(request.form.get("pack_price"))
        days_to_process = float(request.form.get("days_to_process"))
        unit_price = float(request.form.get("unit_price"))
        freight_cost = float(request.form.get("freight_cost"))
        country = (request.form.get("country"))
        unit_of_measure = float(request.form.get("unit_of_measure"))

        consignment_data = ConsignmentData(
            line_item_insurance=line_item_insurance, line_item_quantity=line_item_quantity, pack_price=pack_price, days_to_process=days_to_process, unit_price=unit_price, freight_cost=freight_cost, country=country, unit_of_measure=unit_of_measure
        )
        consignment_dataframe = consignment_data.get_housing_input_data_frame()
        consignment_predictor = ConsignmentPredictor(model_dir=MODEL_DIR)
        line_item_value = consignment_predictor.pred(X=consignment_dataframe)
        context = {
            CONSIGNMENT_DATA_KEY: consignment_data.get_housing_data_as_dict(),
            LINE_ITEM_VALUE_KEY: line_item_value
        }
        return render_template("predict.html", context=context)
    return render_template("predict.html", context=context)


@app.route("/noaccess", methods=["GET"])
@login_required
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
        files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}
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
@login_required
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
        files = {os.path.join(abs_path, file)                 : file for file in os.listdir(abs_path)}
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
@login_required
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
        files = {os.path.join(abs_path, file)                 : file for file in os.listdir(abs_path)}
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
@login_required
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
        files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}
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
@login_required
@cross_origin()
def train():
    try:
        import subprocess
        Call().main("source/run_all_scipts.py")
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
@login_required
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
@login_required
@cross_origin()
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
