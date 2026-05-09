from Tkinter import *

def closeApp():
    app.quit()


def calculateLabel(*args):
    loan = float(loanAmount.get())
    yearlyinterest = float(loanInterest.get())
    interest = (yearlyinterest/100)/12
    term = int(loanTerm.get())
    total = loan * (interest/(1-(1+interest) ** (-term)))
    #loanAmount.delete(0,END)
    #loanInterest.delete(0,END)    
    labelText.set("$" + str(round(total,2)))

app = Tk()
app.title("Loan Calculator")
app.geometry('500x200+200+200')
app.bind("<Return>",calculateLabel)

menubar = Menu(app)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit",command=app.quit)
menubar.add_cascade(label="File",menu=filemenu)

label2 = Label(app, text='Loan Amount')
label2.grid(row=1)

loanAmount = IntVar()
loanAmount.set("")
loanAmount = Entry(app, textvariable=loanAmount)
loanAmount.focus_set()
loanAmount.grid(row=1, column=1)


label3 = Label(app, text='Interest Rate')
label3.grid(row=2)

loanInterest = IntVar()
loanInterest.set("")
loanInterest = Entry(app, textvariable=loanAmount)
loanInterest.grid(row=2, column=1)

label4 = Label(app, text='Term in Months')
label4.grid(row=3)

loanTerm = IntVar()
loanTerm.set("")
loanTerm = Entry(app, textvariable=loanTerm)
loanTerm.grid(row=3, column=1)

paymentLabel = Label(app, text='Your monthly payment will be ')
paymentLabel.grid(row=8, column=0)

labelText = StringVar()
labelText.set("Payment")
label1 = Label(app, textvariable=labelText, height=4)
label1.grid(row=8, column=1)


calculateButton = Button(app, text="Click to calculate", width=20, command=calculateLabel)
calculateButton.grid(row=10,column=2)

closeButton = Button(app, text="Close", width=20, command=closeApp)
closeButton.grid(row=10,column=1)

app.config(menu=menubar)

app.mainloop()
