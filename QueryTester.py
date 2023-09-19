# Peter Berens, Molly Ryan, Sian Wood
# 14 August 2023
# UI 

from Session import Session
from QuestionFactory import QuestionFactory
#import Question

""" Class to display information to the user and get input from the user """
class QueryTester():
    
    def __init__(self):
        
        self.db = Session.loadDatabase(self)
        self.factory = QuestionFactory(self.db)
        
        #print("Hello!")
        #user = input("Please enter your student number:")
        user = 'me'
        self.session = Session(user)
        #choice = input("\nTo attempt a question, press enter. To exit, enter x:")
        choice=''
        while (choice != 'x'):
            if (choice==''):
                self.askQuestion('hard')
            else:
                print("Invalid selection. Please try again.")
            choice=input("\nTo attempt a question, press enter. To exit, enter x:")
        #exit
        
    def askQuestion(self, difficulty):
        #generate question
        
        q = self.factory.getQuestion(difficulty)
        print(q.getSqlQuery())
        if q.getSqlQuery()=="": print("The query is empty")
        else: print("the query is not empty")
        #print(q.getEnglishQuery())
        
        # print the english question
        #print(self.question.getQuestion())

        # take user input
        stuAns = 'test'

        # pass both to session marker ( self.session.marker )
        modalAns = q.getSqlQuery()
        result = self.session.markQuery(stuAns, modalAns)

        # return feedback (store it if we have a student object)
        if result[0]:
            print('Correct.')
        else:
            print('Incorrect.', result[1]) # Display feedback on whether the entered query is valid (ran without error)
        
        print("Modal Query: ", modalAns) # display the modal answer (for prototype demo purposes)
    
        
        
        
        
QueryTester()
        
        
