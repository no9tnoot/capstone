# Peter Berens, Molly Ryan, Sian Wood
# 14 August 2023
# UI 

import Session
import Question

class UserInterface:
    
    def __init__(self):
        print("Hello!")
        user = input("Please enter your student number:")
        self.session = Session.Session(user)
        choice = input("To attempt a question, enter q, to exit, enter x:")
        while (choice != 'x'):
            if (choice=='q'):
                self.askQuestion()
            else:
                print("Invalid selection. Please try again.")
            choice=input("To attempt a question, enter q, to exit, enter x:")
        
    def askQuestion(self):
        question = self.session.getQuestion()
        # print the question
        # take user input
        # pass both to session marker
        # return feedback
    
        
        
            
        
        
        
        
        
