# Peter Berens, Sian Wood, Molly Ryan
# 22 August 2023
# GUI

import tkinter

class TestSQL_GUI:
    
    def __init__(self, window):
        self.window=window
        self.window.title("TestSQL")
        
        self.label = tkinter.Label(self.window, text="Hello, OOP GUI!")
        self.label.pack(padx=20, pady=20)

        self.button = tkinter.Button(self.window, text="Click Me", command=self.button_clicked)
        self.button.pack(padx=20, pady=10)

    def button_clicked(self):
        self.label.config(text="Button Clicked!")

def main():
    window = tkinter.Tk()
    app = TestSQL_GUI(window)
    window.mainloop()

if __name__ == "__main__":
    main()