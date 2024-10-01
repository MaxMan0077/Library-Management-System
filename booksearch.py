#-------------------------------------------------------------------------------
#
#  Module:      booksearch 
#
#  Purpose:     Module which contains two functions that support the librarian 
#               to search for a book based on its title.  
#
#  Modules/Functions:   datetime (standard library)
#                       database
#                       titleSearch()
#                       loanLengthCheck()
#
#  Author:      Max Ward (F132159)       Date-Written: 16 December 2021
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imported Libraries/ Modules:
#-------------------------------------------------------------------------------
#  datetime is the standard library for Python providing a number of functions to 
#  work with dates, times and time intervals.
from datetime import datetime as dt

#  Library Management System specific text file that stores all the information on each  book: 
import database as db

#-------------------------------------------------------------------------------
#  Function definitions:
#
#  1. titleSearch:  
#  ---------------
#  Returns a list of matching book titles.
#
#  2. loanLengthCheck:  
#  -------------------
#  Determines if a book has been on loan for more than 60 days. 
#-------------------------------------------------------------------------------

def titleSearch(searchTerm):
    """ Receives a 'search' term and compares this for a match to the book title 
        for every book record stored within 'database.txt'. List of matching 
        book information is returned to the calling module/ function. """
    
    data = db.loadFile("database.txt")
    output=[]
    for x in range(0, len(data)): # loops through all records
        if searchTerm in str(data[x][2]).lower(): # checks if the search term in a substring of current records book title
            output.append(data[x])
    return output

def loanLengthCheck(record):
    """ Receives the list of information for a book and if the book is out on loan 
        it finds the latest loan history for this book from the log file 'logfile.txt'.
        Calculates the number of days the book has been out on loan and if greater 
        than 60 days returns the number of days on loan to the calling module/ function. """
    
    if record[5] != "0\n":
        logData = db.loadFile("logfile.txt")
        reversedData = logData.reverse() # reverse logfile order to reduce number of times program loops through data
        notFound = True
        checkoutDate=""
        dayDifference = 0
        count = 0
        while notFound == True and count < len(logData): # finds the latest record of a given bookID in the log file
            if logData[count][0] == record[0]:
                checkoutDate = logData[count][1]
                dayDifference = db.daysPassed(checkoutDate)
                break
            else:
                count += 1
             
        if dayDifference > 60:
            return int(dayDifference)
        else:
            return int(0)
    else:
        return int(0)    

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Tests  
#  =====
#  ID.  Test Case                                           Test Result                                                                                     Pass        
#  ~~~  ~~~~~~~~~                                           ~~~~~~~~~~~                                                                                     ~~~~     
# 
#  01   Search term = 'Farm'                                Displayed: CL16;Classics;Animal Farm;George Orwell;14/08/2012;0                                 Loan status 'Available'   
#
#  02   Search term = 'Potter'                              Displayed: FN01;Fantasy;Harry Potter and the Philosopher's Stone;J. K. Rowling;01/01/2010;0     Pass
#                                                           Displayed: FN02;Fantasy;Harry Potter and the Philosopher's Stone;J. K. Rowling;01/01/2010;0
#                                                           Displayed: FN03;Fantasy;Harry Potter and the Philosopher's Stone;J. K. Rowling;28/02/2010;0
#                                                           Displayed: FN04;Fantasy;Harry Potter and the Philosopher's Stone;J. K. Rowling;28/02/2010;0
#                                                           Displayed: FN05;Fantasy;Harry Potter and the Chamber of Secrets;J. K. Rowling;10/06/2012;0
#                                                           Displayed: FN06;Fantasy;Harry Potter and the Chamber of Secrets;J. K. Rowling;10/06/2012;0
#                                                           Displayed: FN07;Fantasy;Harry Potter and the Chamber of Secrets;J. K. Rowling;17/09/2012;0
#                                                           Displayed: FN08;Fantasy;Harry Potter and the Chamber of Secrets;J. K. Rowling;17/09/2012;0
#                                                           Displayed: FN13;Fantasy;Harry Potter and the Order of the Phoenix;J. K. Rowling;31/01/2021;0
#
#  03   Search for an existing book = 'and'.                Displays list of books that can be scrolled across multiple screen space.                       Pass
#
#  04   Search for a non-existant book = 'Z£x2'.            Error msg: 'ERROR: No Results Found Matching Search Query:'.                                    Pass
#
#  05   Search with a BLANK search term.                    Displays ALL books in the Library Management System.                                            Pass
# 
#  05   Search for an existing book title = 'Gino' that     Displayed: FD05;Food & Drink;Gino's Italian Family Adventure;Gino D'Acampo;10/06/2012;MWD1      Pass
#       has a Book ID = FD05 on loan for more than 60       Displayed: FD06;Food & Drink;Gino's Italian Family Adventure;Gino D'Acampo;10/06/2012;0
#       days.                                               Displayed: FD07;Food & Drink;Gino's Italian Family Adventure;Gino D'Acampo;17/09/2012;0
#                                                           Displayed: FD08;Food & Drink;Gino's Italian Family Adventure;Gino D'Acampo;17/09/2012;0
#                                                           Message: 'Book FD05 on loan for more than 60 days'
#
#  05   Search with a BLANK search term with Book IDs =     Displays ALL books in the Library Management System with 3 messages:                            Pass
#       FD05, SP01 and MS15 all on-loan for more than       Message: 'Book FD05 on loan for more than 60 days'
#       60 days.                                            Message: 'Book SP01 on loan for more than 60 days'
#                                                           Message: 'Book MS15 on loan for more than 60 days'
# 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
