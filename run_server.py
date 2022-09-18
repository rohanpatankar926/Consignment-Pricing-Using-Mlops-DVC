from threading import Thread
from app import app,stream,train
import os
from call import Call
port = int(os.getenv("PORT", 5000))

    
def server1():
    app.config["SECRET_KEY"] = "!@##$#!#EDS#@!df"
    stream
    train
    app.run(port=port,host="0.0.0.0",debug=False)
    Call().main("app.py")

def server2():
    Call().main("source/mlflow_run.py")

if __name__=="__main__":
    server1_=Thread(target=server1)
    server2_=Thread(target=server2)
    server1_.start()
    server2_.start()