from datetime import datetime


class Applogger:
    def __init__(self):
        pass
    
    def log(self,file_object,main_file,log_message):
        self.now=datetime.now()
        self.date=self.now.date()
        self.current_time=self.now.strftime("%H:%M:%S")
        file_object.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
        main_file.write(str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
        