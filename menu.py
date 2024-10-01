#-------------------------------------------------------------------------------
#
#  Program:     menu 
#
#  Purpose:     Main control program for a Library Management System for use by 
#               a librarian. The librarian is presented with a single screen
#               comprising of five Menu options: 
#               1.  Search for books by title. 
#               2.  Check-out an available book. 
#               3.  Return a loaned book. 
#               4.  Recommend books to a member.
#               5.  Quit.   
#
#  Modules/ Functions:  tkinter (standard library)
#                       matplotlib.pyplot
#                       matplotlib.backend_tools
#                       booksearch/ titleSearch; loanLengthCheck
#                       bookcheckout/ addCheckout; LoanLengthCheck
#                       bookreturn/ addReturn; loanLengthCheck
#                       bookrecommend/ getRecommendedBooks; getBooksInGenre; numberToRecommend   
#                       searchBook()
#                       checkoutBook()
#                       returnBook()
#                       recommendBook()
#
#  Author:      Max Ward (F132159)       Date-Written: 16 December 2021
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imported Libraries/ Modules:
#-------------------------------------------------------------------------------
#  Tkinter is the standard GUI library for Python enabling the implementation of full-featured graphical user 
#  interfaces that run on all major GUI platforms.
from tkinter import *
from tkinter import ttk
from tkinter import font

#  Matplotlib is a plotting library for the Python programming language and provides an object-oriented API for 
#  embedding plots into applications using general-purpose GUI toolkits like Tkinter.
import matplotlib.pyplot as pl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backend_tools
from matplotlib.figure import Figure

#  'Library Management System' specific modules: 
import booksearch as bsearch
import bookcheckout as checkout
import bookreturn as Return
import bookrecomend as recommend

#-------------------------------------------------------------------------------
#  GUI components initialisation:
#-------------------------------------------------------------------------------
# initilize main menu window & frames
MainMenu = Tk()
MainMenu.title("Library Management System")
MainMenu.geometry("1400x1080")
checkoutReturnFrame = LabelFrame(MainMenu, width= 1400, height= 250)
searchRecommendFrame = LabelFrame(MainMenu, width=1400, height=642)

# initilize labels
titleLable = Label(MainMenu, text="Library Managment System", font="Sans-serif 35")
bookIDLableCheckoutReturn = Label(checkoutReturnFrame, text="Book ID", font="Sans-serif 13", fg='grey60')
memberIDLableCheckout = Label(checkoutReturnFrame, text="Member ID", font="Sans-serif 13", fg='grey60')
bookIDLableSearch = Label(searchRecommendFrame, text="Enter Search Keyword or Member ID", font="Sans-serif 13", fg='grey60')

# initilize Input Fields
checkoutBookIdIO = Entry(checkoutReturnFrame, width=30,font="Sans-serif 13",fg='grey60')
checkoutMemberIdIO = Entry(checkoutReturnFrame, width=30,font="Sans-serif 13", fg='grey60')
returnBookIdIO = Entry(checkoutReturnFrame, width=30,font="Sans-serif 13", fg='grey60')
searchIO = Entry(searchRecommendFrame, width=50,font="Sans-serif 13", fg='grey60')

#initilize Text Fields
checkoutReturnConfirmation = Text(checkoutReturnFrame,width=173)
#searchRecommendOutput =  Text(searchRecommendFrame,width=173, height=14)
graphOutput = Text(searchRecommendFrame,width=173, height=20)

# New code:
style = ttk.Style()
# style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Sans-serif', 11)) # Modify the font of the body
# tree=ttk.Treeview(master,style="mystyle.Treeview")
style.configure("mystyle.Treeview.Heading", font=('Sans-serif', 8,'bold', 'underline')) # Modify the font of the headings
tableData = ttk.Treeview(searchRecommendFrame, style="mystyle.Treeview", column=("Book ID","Genre","Book Title","Author","Purchase Date","Loan Status"), show="headings", height=10)

# tableData = ttk.Treeview(searchRecommendFrame, column=("Book ID","Genre","Book Title","Author","Purchase Date","Loan Status"), show="headings", height=10)
tableData.column("# 1", anchor= CENTER, width=170)
tableData.heading("# 1", text="Book ID")
tableData.column("# 2", anchor= CENTER,width=250)
tableData.heading("# 2", text="Genre")
tableData.column("# 3", anchor= CENTER, width= 300)
tableData.heading("# 3", text="Book Title")
tableData.column("# 4", anchor= CENTER,width=250)
tableData.heading("# 4", text="Author")
tableData.column("# 5", anchor= CENTER,width=250)
tableData.heading("# 5", text="Purchase Date")
tableData.column("# 6", anchor= CENTER,width=170)
tableData.heading("# 6", text="Loan Status")

#-------------------------------------------------------------------------------
#  Function definitions: 
#
#  1. searchBook:  
#  --------------
#  Search for a book based on its title. 
#
#  2. checkoutBook:  
#  ----------------
#  Check-out an available book from the library. 
#
#  3. returnBook:  
#  --------------
#  Return a checked-out (loaned) book. 
#
#  4. recommendBook:  
#  -----------------
#  Recommends books to a member. 
#-------------------------------------------------------------------------------
graphCheck = False

def searchBook():
    """ Activated when the librarian selects the 'Search' button.  Gets the 
        user entered 'search' term and calls the 'booksearch.titleSearch()' 
        module function to obtain a list of matching book titles and all their
        associated information. Displays all matching book details on the screen 
        and calls the 'booksearch.loanLengthCheck()' module function to highlight
        any books that have been on loan for more than 60 days. """
    
    BookID1 = ""
    Genre1 = ""
    Title1 = ""
    Author1 = ""
    PurchaseDate1 = ""
    LoanStutus1 = ""
    global graphCheck
    if graphCheck == True:
        graphCanvas.get_tk_widget().destroy()
        graphCheck = False
    searchTerm1 = searchIO.get().lower()

    results = bsearch.titleSearch(searchTerm1)
    for x in tableData.get_children():
        tableData.delete(x)
    graphOutput.delete("1.0", END)

    if len(results)==0:
         graphOutput.insert(END, "ERROR: No results found that match the Search term:")
    for x in range(len(results)):
        output = ""
        for y in range(7):
            if y == 0:
                BookID1 = str(results[x][0])
            elif y == 1:
                Genre1 = str(results[x][1])
            elif y == 2:
                Title1 = str(results[x][2])
            elif y == 3:
                Author1 = str(results[x][3])
            elif y == 4:
                PurchaseDate1 = str(results[x][4])
            elif y == 5:
                LoanStutus1 = str(results[x][5])
                if bsearch.loanLengthCheck(results[x]) > 60:
                    output +=  "BOOK " + str(results[x][0]) + "**** On-Loan for more than 60 days ****\n"
            else:
                graphOutput.insert(END, output)
        tableData.insert(parent="", index="end", iid=x, values=(BookID1,Genre1,Title1,Author1,PurchaseDate1,LoanStutus1))

def checkoutBook():
    """ Activated when the librarian selects the 'Checkout' button.  Gets a valid 
    librarian entered 'Book ID' and 'Member ID' terms and calls the 'bookcheckout.addCheckout()' 
    module function to withdraw (loan) an available book from the library.  Calls the
    'bookcheckout.LoanLengthCheck()' module function to determine if the Member is 
    currently holding any books for more than 60 days and if so a warning message
    is displayed to the librarian. """
    
    global graphCheck
    if graphCheck == True:
        graphCanvas.get_tk_widget().destroy()
        graphCheck = False
    bookID = checkoutBookIdIO.get()
    memberID = checkoutMemberIdIO.get()
    message = checkout.addCheckout(bookID, memberID)
    if message != "N":
        overDueBooks = checkout.LoanLengthCheck(memberID)

    checkoutReturnConfirmation.delete("1.0", END)
    if message != "N":
        if len(overDueBooks) > 0:
            message += "\nMember " + memberID + "**** Has loaned book(s) " + ",".join(overDueBooks) + " for more than 60 days ****"
    if message != "N":    
        checkoutReturnConfirmation.insert(END, str(message))
    else:
        checkoutReturnConfirmation.insert(END, "Member ID must be in the format of four alphanumeric characters")

def returnBook():
    """ Activated when the librarian selects the 'Return' button.  Gets a valid 
    librarian entered 'Book ID' term and calls the 'bookreturn.addReturn()' 
    module function to record the book as returned.  Calls the 'bookreturn.loanLengthCheck()'
    module function to determine if the book has been on-loan for more than 60 days and if 
    so a warning message is displayed to the librarian. """
    
    global graphCheck
    loanLength = 0
    if graphCheck == True:
        graphCanvas.get_tk_widget().destroy()
        graphCheck = False
    bookID = returnBookIdIO.get()
    message = Return.addReturn(bookID)
    text = message[0]
    bookID = message[1]
    if message[1] != "":
        loanLength = Return.loanLengthCheck(bookID)
    if loanLength > 60:
        text += "\nWARNING: Book " + bookID + " has been out on loan for " + str(loanLength) + " days"
    checkoutReturnConfirmation.delete("1.0", END)
    checkoutReturnConfirmation.insert(END, str(text))

def recommendBook():
    """ Activated when the librarian selects the 'Recommend' button.  Gets a valid 
        librarian entered 'Member ID' term and calls the 'recommend.getRecommendedBooks()' 
        module function to obtain the Member's reading history by Genre along with a list of 
        between 3 and 10 recommended books in proportion to those Genre preferences. A graph
        bar chart is built and displayed showing the reading preferences for that Member 
        based on Genre popularity.  The list of recommended book titles is displayed in 
        popularity order based on the Genre preferences and weightings as shown on the graph. """
   
    global graphCheck, graphCanvas
    graphOutput.delete("1.0", END)
    memberID = searchIO.get()
    Xaxis = ["Science Fiction","Horror","Fantasy","Romance","Classics","Sport","Music","Food & Drink"]
    Yaxis = []
    output = ""
    
    #  Get list of recommended books.
    recommendData = recommend.getRecommendedBooks(memberID)
    recommendedBooks = recommendData[0]
    Yaxis = recommendData[1]
    if len(recommendedBooks) < 3:
        output += "Insufficient information to make any recommendations for Member: " + memberID
    else:
        for x in range(len(recommendedBooks)):  # Format list of recommended books for display.
            output += str(recommendedBooks[x]) + "\n"
            
    if graphCheck == True:
        graphCanvas.get_tk_widget().destroy()
        graphCheck = False
        
    #  Build graph structure and details.
    fig  = Figure(figsize = (10,4), dpi =72, tight_layout = True)
    axis = fig.add_subplot(111)
    axis.set_title("Genre Count For Member " + memberID, fontsize = 15, color = 'goldenrod', fontweight = 'bold')
    axis.set_xlabel("Genres", fontsize = 10)
    axis.set_ylabel("Number Of Books Read By Member", fontsize = 10)
    graph = axis.bar(Xaxis, Yaxis)
    axis.xaxis.label.set_color('cornflowerblue')        
    axis.yaxis.label.set_color('cornflowerblue')         

    #  Display graph on the screen.
    graphCanvas = FigureCanvasTkAgg(fig, master=graphOutput)
    graphCanvas.draw()
    graphCanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    graphCheck = True

   
    for x in tableData.get_children():
        tableData.delete(x)
    for x in range(len(recommendedBooks)):
        tableData.insert(parent="", index="end", iid=x, values=("-","-",recommendedBooks[x],"-","-","-"))

#-------------------------------------------------------------------------------
#  GUI buttons widgets initialistion and corresponding Function activation:
#-------------------------------------------------------------------------------
quitButton = Button(MainMenu,bg="red",text="Quit", font="Sans-serif 10 bold", fg="white", width= 100, height=2, command= MainMenu.quit)
checkoutButton = Button(checkoutReturnFrame,bg="SeaGreen3",text="Checkout", font="Sans-serif 10 bold", fg="white", width=40, height=4, command= checkoutBook)
returnButton = Button(checkoutReturnFrame,bg="RoyalBlue3",text="Return", font="Sans-serif 10 bold", fg="white", width=40, height=4, command= returnBook)
searchButton = Button(searchRecommendFrame,bg="gray80",text="Search", font="Sans-serif 10 bold", width=40, height=4, command= searchBook)
recommendButton = Button(searchRecommendFrame,bg="gray80",text="Recommend", font="Sans-serif 10 bold", width=40, height=4, command= recommendBook)

#-------------------------------------------------------------------------------
#  Position Main Menu GUI:
#-------------------------------------------------------------------------------
# set position of frames & non-frame entities
titleLable.grid(row=0, column=0)
checkoutReturnFrame.grid(row=1, column=0)
searchRecommendFrame.grid(row=2, column=0)
quitButton.grid(row=3, column=0)

# position checkoutReturnFrame entities on screen
checkoutReturnFrame.grid_propagate(0)
bookIDLableCheckoutReturn.grid(row=0, column=1)
memberIDLableCheckout.grid(row=0, column=2)
checkoutButton.grid(row=1,column=0)
checkoutBookIdIO.grid(row=1,column=1)
checkoutMemberIdIO.grid(row=1,column=2)
returnButton.grid(row=2,column=0)
returnBookIdIO.grid(row=2,column=1)
checkoutReturnConfirmation.grid(row=3, column=0, columnspan=3)

# position searchRecommendFrame entities on screen
searchRecommendFrame.grid_propagate(0)
bookIDLableSearch.grid(row=0, column=2)
searchButton.grid(row=1, column=0)
recommendButton.grid(row=1,column=1)
searchIO.grid(row=1,column=2)
tableData.grid(row=2,column=0,columnspan=3)
graphOutput.grid(row=3, column=0, columnspan=3)


MainMenu.mainloop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#  Tests  
#  =====
# 
#  Note: Majority of test cases specified within the relevant Search, Checkout, Return and Recommend modules.
#
#  ID.  Test Case                                                Test Result                                                                Pass/ Fail        
#  ~~~  ~~~~~~~~~                                                ~~~~~~~~~~~                                                                ~~~~~~~~~~     
#
#  01   On launching the application the screen should be        All button functions available and clearly presented.                      Pass    
#       presented with options to Search, Check-out,          
#       Return, Recommend books and present a Quit function.
#
#  02   Clear instruction to Exit the application.               Application closes correctly when 'Quit' button selected.                  Pass   
#
#  03   All input fields allow text to be entered.               Text can be entered into Book ID, Member ID and Search Keyword-Member ID.  Pass   
#
#  04   Clicking anywhere on the screen other than Buttons or    No effect to application.                                                  Pass
#       input fields has zero effect.                             
#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------