
from flask import Flask,render_template
import os
import sys

webapp_root="webapp"
static_dir=os.path.join(webapp_root,"static")
template_dir=os.path.join(webapp_root,"templates")

app=Flask(__name__,template_folder=template_dir,static_folder=static_dir)

@app.route("/",methods=["GET"])
def home_page():
	return render_template("index.html")

@app.route("/predict",methods=["POST","GET"])
def predict_page():
    return render_template("details.html")
# @app.route('/logs', defaults={'req_path': 'logs'})
# @app.route('/logs/<path:req_path>')
# def render_log_dir(req_path):
#     os.makedirs("logs", exist_ok=True)
#     # Joining the base and the requested path
#     print(f"req_path: {req_path}")
#     abs_path = os.path.join(req_path)
#     print(abs_path)
#     # Return 404 if path doesn't exist
#     if not os.path.exists(abs_path):
#         return abort(404)

#     # Check if path is a file and serve
#     if os.path.isfile(abs_path):
#         return send_file(abs_path)

#     # Show directory contents
#     files = {os.path.join(abs_path, file):file for file in os.listdir(abs_path)}
    
#     result = {
#         "files": files,
#         "parent_folder": os.path.dirname(abs_path),
#         "parent_label": abs_path
#     }
#     return render_template('log_files.html', result=result)

if __name__=="__main__":
    app.run(port=8000,debug=True)