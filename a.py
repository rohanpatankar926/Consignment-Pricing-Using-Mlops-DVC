from subprocess import call
def train():
        return_code = call(["python","src/run_all_scipts.py"])
        print(return_code)
if __name__=="__main__":
    train()