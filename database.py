#-------------------------------------------------------------------------------
#
#  Module:      database 
#
#  Purpose:     Module which contains two functions that support the librarian 
#               to withdraw a book from the library.  
#
#  Modules/Functions:   datetime (standard library)
#                       loadFile()
#                       updateFile()
#                       appendFile()
#                       daysPassed()
#                       getGenre()
#                       getTitle()
#
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imported Libraries/ Modules:
#-------------------------------------------------------------------------------
#  datetime is the standard library for Python providing a number of functions to 
#  work with dates, times and time intervals.
from datetime import datetime as dt

#-------------------------------------------------------------------------------
#  Function definitions:
#
#  1. loadFile:  
#  ------------
#  Called by Modules.Functions: booksearch.titleSearch(); booksearch.loanLengthCheck(); bookcheckout.addCheckout(); bookcheckout.LoanLengthCheck(); bookreturn.addReturn()
#  bookreturn.loanLengthCheck(); bookrecommend.getRecommendedBooks(); bookrecommend.getBooksInGenre(); 
#  Reads all book entries from database.txt and for each book stores all book
#  information in a returned two-dimensional list.
#
#  2. updateFile:  
#  -------------- 
#  Called by Modules.Functions: bookcheckout.addCheckout(); bookreturn.addReturn()
#  Writes all book information stored on the two-dimensional list to database.txt
#  which stores information for all books.
#  
#  3. appendFile:  
#  -------------- 
#  Called by Modules.Functions: bookcheckout.addCheckout(); bookreturn.addReturn()
#  Writes a new entry to the transaction log logfile.txt to store the loan 
#  history of library books.
#  
#  4. daysPassed:  
#  -------------- 
#  Called by Modules.Functions: booksearch.loanLengthCheck(); bookreturn.loanLengthCheck()
#  Returns the number of days between the current date and the date when a 
#  specific unreturned book was checked-out.
#  
#  5. getGenre:  
#  ------------ 
#  Called by Modules.Functions: bookrecommend.getRecommendedBooks(); 
#  Searches book entries from database.txt and returns the Genre for a given Book ID.
#  
#  6. getTitle:  
#  ------------ 
#  Called by Modules.Functions: bookrecommend.getRecommendedBooks(); 
#  Searches book entries from database.txt and returns the Title for a given Book ID.
#
#-------------------------------------------------------------------------------

def loadFile(filepath):
    """ xxxxxx. """

    contents = []
    with open(str(filepath)) as data: 
        contents = data.readlines() # import every line in database.txt into a list
    dataBase_Data = []
    splitData=[]
    for x in range(len(contents)):
        splitData = contents[x].split(";") # splits fields into their own list creating a 2D list
        dataBase_Data.append(splitData)
    data.close()
    return dataBase_Data

def updateFile(newData, filePath):
    """ xxxxxx. """

    file = open(str(filePath), "w")
    importData = []
    for x in range(len(newData)):
        temp = newData[x]
        importData.append(";".join(temp))
    for x in range(len(importData)):
            file.write(str(importData[x]))
    file.close()

def appendFile(newData, filePath):
    """ xxxxxx. """

    file = open(str(filePath), "a")
    file.write(str(newData))
    file.close()

def daysPassed(date):
    """ xxxxxx. """

    currentDate = dt.now()
    checkoutDate = dt.strptime(date, "%d/%m/%Y") # converts date from string to datetime object
    difference = currentDate - checkoutDate
    return difference.days

def getGenre(bookID):
    """ xxxxxx. """    

    dataBaseData = loadFile("database.txt")
    genre = ""
    for x in range(len(dataBaseData)):
        if dataBaseData[x][0] == bookID:
            genre = dataBaseData[x][1]
            break
    return genre

def getTitle(bookID):
    """ xxxxxx. """

    dataBaseData = loadFile("database.txt")
    title = ""
    for x in range(len(dataBaseData)):
        if dataBaseData[x][0] == bookID:
            title = dataBaseData[x][2]
            break
    return title