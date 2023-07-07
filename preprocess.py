from datetime import date


class Preprocessor:

    def __init__(self, name):

        self.name = name

    
    def process_pronouns(self, query):

        query = query.split(" ")

        for i in range(len(query)):
            
            word = query[i]

            if word == "I" or word == "me" or word == "Me":
                query[i] = query[i] + "({})".format(self.name)
            

        return " ".join(query)   

    def process_time(self, query):

        today = date.today()
        query = query.split(" ")

        for i in range(len(query)):
            
            word = query[i].lower()

            if word == "today" or word == "todays":
                query[i] = query[i] + "({})".format(str(today))
            

        return " ".join(query)   

