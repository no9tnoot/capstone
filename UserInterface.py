# Peter Berens, Molly Ryan, Sian Wood
# 14 August 2023
# UI 

import Session
import Question

""" Class to display information to the user and get input from the user """
class UserInterface():
    
    def __init__(self):
        print("Hello!")
        user = input("Please enter your student number:")
        self.session = Session.Session(user)
        choice = input("\nTo attempt a question, press enter. To exit, enter x:")
        
        # While not choosing to exit
        while (choice != 'x'):
            if (choice==''):
                self.askQuestion()
            else:
                print("Invalid selection. Please try again.")
            choice=input("\nTo attempt a question, press enter. To exit, enter x:")
        #exit
        
    def askQuestion(self):
        #generate question
        self.question = self.session.genQuestion()

        # print the english question
        print(self.question.getQuestion())

        # take user input
        stuAns = input('SQL Query:')

        # pass both to session marker ( self.session.marker )
        modalAns = self.question.getQuery()
        result = self.session.markQuery(stuAns, modalAns)

        # return feedback (store it if we have a student object)
        if result[0]:
            print('Correct.')
        else:
            print('Incorrect.', result[1]) # Display feedback on whether the entered query is valid (ran without error)
        
        print("Modal Query: ", modalAns) # display the modal answer (for prototype demo purposes)
    
        
        
        
        
        
        
