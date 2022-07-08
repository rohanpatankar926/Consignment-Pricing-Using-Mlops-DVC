from threading import Thread
from app import app
import os
from call import Call

def server1():
    Call().main("app.py")

def server2():
    Call().main("src/mlflow_run.py")

if __name__=="__main__":
    server1_=Thread(target=server1)
    server2_=Thread(target=server2)
    server1_.start()
    server2_.start()