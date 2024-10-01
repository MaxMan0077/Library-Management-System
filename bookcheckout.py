#-------------------------------------------------------------------------------
#
#  Module:      bookcheckout 
#
#  Purpose:     Module which contains two functions that support the librarian 
#               to withdraw a book from the library.  
#
#  Modules/Functions:   datetime (standard library)
#                       booksearch
#                       database
#                       addCheckout()
#                       LoanLengthCheck()
#
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imported Libraries/ Modules:
#-------------------------------------------------------------------------------
#  datetime is the standard library for Python providing a number of functions to 
#  work with dates, times and time intervals.
from datetime import datetime as dt

#  unicodedata provides access to the Unicode Character Database (UCD) which 
#  defines character properties for all Unicode characters.
import unicodedata

#  'Library Management System' specific modules: 
import booksearch as bsearch

#  Library Management System specific text file that stores all the information on each book: 
import database as db

#-------------------------------------------------------------------------------
#  Function definitions:
#
#  1. addCheckout:  
#  ---------------
#  Called by Modules.Functions: menu.checkoutBook(); 
#  Withdraws a book if valid based on Memebr ID and Book ID returning an appropriate
#  success or fail message.
#
#  2. LoanLengthCheck:  
#  ------------------- 
#  Called by Modules.Functions: menu.checkoutBook(); 
#  Determines whether a specific member currently has any books that have been 
#  on loan for more than 60 days. 
#-------------------------------------------------------------------------------

def addCheckout(bookID, memberID):
    """ Receives a 'Book ID' and 'Member ID'. If the 'Book ID' exists on database.txt  
        determines if the book is available to withdraw. If available then a new 
        record is written to logfile.txt and the book information on database.txt is 
        updated to record that it is now on loan to the Member. A message is returned
        to the calling module/ function detailing that the checkout was successful, 
        the book is currently on loan or the 'Book ID' does not exist. """

    database = db.loadFile("database.txt")
    bookExists = False
    bookAvailable = False
    oldRecord = []
    newRecord = ""
    output = ""
    validID = False

    if memberID.isalnum() == True and len(memberID) == 4:
        validID = True

    if validID == True:
        x = 0
        for x in range(len(database)):
            temp = database[x][0]
            if database[x][0] == str(bookID):
                oldRecord = database[x]
                bookExists = True
                break
        if bookExists == True:
            if oldRecord[5] == "0\n":
                bookAvailable = True
        if bookAvailable == True:
            currentDate = dt.now()
            currentDateString = currentDate.strftime("%d/%m/%Y")
            newRecord = oldRecord[0] + ";" + currentDateString + ";" + memberID + "\n"
            db.appendFile(newRecord, "logfile.txt")
            database[x][5] = str(memberID) + "\n"
            db.updateFile(database, "database.txt")
            output = "Book " + bookID + " taken out by " + memberID
        if bookExists == False:
            output = "ERROR: Book Not Found"
        if bookExists == True and bookAvailable == False:
            output = "ERROR: Book Currently Out On-Loan"
        return output
    else:
        output = "N"
        return output


def LoanLengthCheck(memberID):
    """ Receives a 'Member ID' and extracts all 'Book Checkout' logfile.txt records 
        for that Member. Please note that the 'Member ID' is only set on logfile.txt 
        for records that are created for a 'Book Checkout' event. For all books that 
        have historically been withdrawn by that Member the 'Book ID' information is 
        read from database.txt to see if the Member still has that book on-loan. If
        the book is currently on-loan to that Member the number of days that the book 
        has been out on loan is calculated and if greater than 60 days the 'Book ID'
        is added to the overdue list. Once all books that have been historically 
        withdrawn by that Member have been checked then the list of overdue books is
        returned to the calling module/ function. """

    logData = db.loadFile("logfile.txt")
    dataBase = db.loadFile("database.txt")
    userHistory = []
    output = []
    for x in range(len(logData)):
        if logData[x][0] != "" and logData[x][2] == memberID + "\n":
           userHistory.append(logData[x])

    for x in range(len(userHistory)):
        bookID = userHistory[x][0]
        for y in range(len(dataBase)):
            if dataBase[y][0] == bookID and dataBase[y][5] == memberID + "\n":
                takeOutDate = userHistory[x][1]
                if db.daysPassed(takeOutDate) > 60:
                    output.append(userHistory[x][0])
                    break
    return output

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#  Tests  
#  =====
#  ID.  Test Case                                           Test Result                                                                                Pass        
#  ~~~  ~~~~~~~~~                                           ~~~~~~~~~~~                                                                                ~~~~     
# 
#  01   Checkout a book with an valid Member ID = 'DVN1'    Msg: 'Book MS18 taken out by DVN1'                                                         Pass
#       and valid Book ID = 'MS18' which is available.      database.txt file updated: MS18;Music;Set the Night on Fire;Robby Krieger;29/12/2020;DVN1
#                                                           logfile.txt file updated:  MS18;11/12/2021;DVN1
#
#  02   Checkout a book with an invalid Member ID = 'Z1££'  Error msg: 'Member ID must consist of four alphanumeric characters'.                       Pass
#       with invalid characters and valid Book ID = 'FD20'  Neither database.txt or logfile.txt are updated.
#
#  03   Checkout a book with an invalid Member ID = 'Z1'    Error msg: 'Member ID must consist of four alphanumeric characters'.                       Pass
#       with less than 4 characters and                     Neither database.txt or logfile.txt are updated.
#       valid Book ID = 'FD20'  
#
#  04   Checkout a book with a valid Member ID = 'MWD1'     Error msg: 'Book not found'.                                                               Pass
#       and invalid Book ID = 'ZZ99'                        Neither database.txt or logfile.txt are updated.
#
#  05   Checkout a book with an valid Member ID = 'JBR1'    Error msg: 'Book currently out on-loan'.                                                   Pass
#       and valid Book ID = 'HR01' already on loan          Neither database.txt or logfile.txt are updated.
#  
#  06   Checkout a book with an valid member ID = 'MWD1'    Msg: 'Book SP11 taken out by MWD1'                                                         Pass
#       and valid book ID = 'SP11' for a member who has 2   database.txt file updated: SP11;Sport;The Gladiator Mindset;Adam Peaty;14/11/2013;MWD1
#       Book ID = FD05 and SP01 checked out for more than   logfile.txt file updated: SP11;11/12/2021;MWD1
#       60 days.                                            Warning msg: 'Member MWD1 has loaned book(s) for more than 60 days'.
#
#------------------------------------------------------------------------------------------------------------------------------------------------------------