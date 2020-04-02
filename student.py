
class student():

    def __init__(self):
        pass

    def chatbot(self):
        print("This is the chatbot, please say what subject you would like to learn more about")
        subject = self.listen()
        if (subject == "Algebra"):
            print("ALG")
        elif (subject == "Geometry"):
            print("GEO")
        elif (subject == "Calculus"):
            print("CALC")
            return "Done"
        elif (subject == "Statistics"):
            print("STATS")
        else:
            print("ERROR, please repeat")
            subject = self.listen()
    
    def listen(self):
        return "Calculus"
