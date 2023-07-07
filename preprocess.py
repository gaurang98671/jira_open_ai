

class Preprocessor:

    def __init__(self, name):

        self.name = name

    
    def process_pronouns(self, query):

        query = query.split(" ")

        for i in range(len(query)):
            
            word = query[i]

            if word == "I" or word == "me" or word == "Me":
                query[i] = query[i] + "({})".format(self.name)
            

        return "".join(query)   

            
