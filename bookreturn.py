#-------------------------------------------------------------------------------
#
#  Module:      bookreturn 
#
#  Purpose:     Module which contains two functions that support the librarian 
#               to withdraw a book from the library.  
#
#  Modules/Functions:   datetime (standard library)
#                       booksearch
#                       database
#                       addReturn()
#                       loanLengthCheck()
#
#  Author:      Max Ward (F132159)        Date-Written: 16 December 2021
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imported Libraries/ Modules:
#-------------------------------------------------------------------------------
#  datetime is the standard library for Python providing a number of functions to 
#  work with dates, times and time intervals.
from datetime import datetime as dt

#  'Library Management System' specific modules: 
import booksearch as bsearch

#  Library Management System specific text file that stores all the information on each book: 
import database as db

#-------------------------------------------------------------------------------
#  Function definitions:
#
#  1. addReturn:  
#  -------------
#  Called by Modules.Functions: menu.returnBook(); 
#  Returns a book if valid based on Book ID returning an appropriate success
#  or fail message.
#
#  2. loanLengthCheck:  
#  -------------------
#  Called by Modules.Functions: menu.returnBook(); 
#  Determines whether a specific member currently has any books that have 
#  been on loan for more than 60 days. 
#-------------------------------------------------------------------------------

def addReturn(bookID):
    """ Receives a 'Book ID' to be returned. Gets the 'Book ID' details from 
    database.txt. If the book exists and is on-loan then a new record is written 
    to logfile.txt and the book information on database.txt is updated to record 
    that the book is now available. A successul book return message is prepared.
    If the book does not exist or is not currently out on-loan then an appropriate
    message is prepared.  The relevant message is returned to the calling module/ 
    function. """
    
    database = db.loadFile("database.txt")
    bookExists = False
    bookOnLoan = False
    oldRecord = []
    output = []
    newRecord = ""
    outputMessage = ""
    bookID2 = ""
    x = 0
    for x in range(len(database)):
        temp = database[x][0]
        if database[x][0] == str(bookID):
            oldRecord = database[x]
            bookExists = True
            break
    if bookExists == True:
        if oldRecord[5] != "0\n":
            bookOnLoan = True
    if bookOnLoan == True:
        currentDate = dt.now()
        currentDateString = currentDate.strftime("%d/%m/%Y")
        newRecord = oldRecord[0] + ";" + currentDateString + ";" + "~" + "\n"
        db.appendFile(newRecord, "logfile.txt")
        database[x][5] = "0"+ "\n"
        db.updateFile(database, "database.txt")
        bookID2 = oldRecord[0]
        outputMessage = "Book " + bookID + " has been successfully returned"
    if bookExists == False:
        outputMessage = "ERROR: Book does not exist"
    if bookExists == True and bookOnLoan == False:
        outputMessage = "ERROR: Book not out on loan"
    output.append(outputMessage)
    output.append(bookID2)
    return output

def loanLengthCheck(bookID):
    """ Receives a 'Book ID' and gets the last 'check out' record for that book from
        logfile.txt.  Calculates the number of days the book has been on-loan to that 
        Member and returns this to the calling module/ function. """

    logData = db.loadFile("logfile.txt")
    reversedData = logData.reverse()
    del(logData[0]) # Removes the book return logfile record just written by addReturn()   
    loanDate = ""
    daysDifference = 0
    for x in range(len(logData)):
        if logData[x][0] == bookID:
            loanDate = logData[x][1]  # This will be the last checkout record written.
            daysDifference = db.daysPassed(loanDate)
            break
    return daysDifference


#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#  Tests  
#  =====
#  ID.  Test Case                                           Test Result                                                                     Pass        
#  ~~~  ~~~~~~~~~                                           ~~~~~~~~~~~                                                                     ~~~~     
# 
#  01   Return a book with an invalid Book ID = '7810'.     Error msg: 'Book does not exist'.                                               Pass 
#
#  02   Return a book with a valid Book ID = 'FN05' that    Error msg: 'Book not out on loan'.                                              Pass
#       is not out on loan.
#
#  03   Return a valid Book ID = 'RO11' less than 60 days   Msg: 'Successfully returned' and                                                Pass
#                                                           database.txt file updated.
#
#  04   Return a valid Book ID = 'SP01' after 60 days.      Msg: 'Successfully returned'                                                    Pass
#                                                           Warning msg: 'Book SP01 has been out on loan for 110 days'
#                                                           database.txt updated.
#
#-----------------------------------------------------------------------------------------------------------------------------------------------------------