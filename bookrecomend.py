#-------------------------------------------------------------------------------
#
#  Module:      bookrecomend 
#
#  Purpose:     Module which contains three functions that support the librarian 
#               in recommending a list of books to a specific Member.  
#
#  Modules/Functions:   random (standard library)
#                       database
#                       getRecommendedBooks()
#                       getBooksInGenre()
#                       numberToRecommend()
#
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imported Libraries/ Modules:
#-------------------------------------------------------------------------------
#  random is the standard library for Python providing a number of functions to generate random numbers
import random as r

#  Library Management System specific text file that stores all the information on each book: 
import database as db

#-------------------------------------------------------------------------------
#  Function definitions:
#
#  1. getRecommendedBooks: (parm: Member ID) 
#  -----------------------
#  Called by Modules.Functions: menu.recommendBook(); 
#  Receives a 'Member ID' and returns a list of recommended book Titles in 
#  popularity order together with a count of the number of books read by the 
#  Member for each Genre.
#  
#  2. getBooksInGenre: (parm: Genre)
#  -------------------
#  Called by Modules.Functions: bookrecomend.getRecommendedBooks(); 
#  Returns a list of all potential Book Titles to recommend within a received Genre.
#
#  3. numberToRecommend: (parm: No. Member genre checkouts and Total no. Member checkouts)
#  ---------------------
#  Called by Modules.Functions: bookrecomend.getRecommendedBooks(); 
#  Returns the number of books to recommend based on the Member's Genre reading history preferences.
#-------------------------------------------------------------------------------

def getRecommendedBooks(memberID):
    """ Receives a 'Member ID' and returns a list of recommended book Titles in popularity 
    order together with a count of the number of books read by the Member for each Genre. 
    Reads logfile.txt to create a Member history of checked-out books and organises 
    these into Genre lists.  For every Genre creates a list of book Titles that 
    are available to be loaned removing any book Titles that the Member has previously read.
    In proportion to the number of books previously read by the Member, calculates the
    number of books in each Genre to recommend to the Member. For the number of 
    books to recommend for each Genre selects at random that number of books from
    the potential available books for that Genre.  """

    logData = db.loadFile("logfile.txt")
    userHistory = []
    genreCount = []
    temp1 = []
    output1 = []
    output2 = []

    scienceFictionUser = []
    horrorUser = []
    fantasyUser = []
    romanceUser = []
    classicsUser = []
    sportUser = []
    musicUser = []
    foodAndDrinkUser = []

    scienceFictionTotal = []
    horrorTotal = []
    fantasyTotal = []
    romanceTotal = []
    classicsTotal = []
    sportTotal = []
    musicTotal = []
    foodAndDrinkTotal = []

#  Read all book checkout log file records for that Member ID:
    for x in range(len(logData)): 
        if logData[x][2] == memberID + "\n":
            userHistory.append(logData[x])   

#  For each Member ID book checked-out determine the Genre and add book Title to 
#  the relevant Member checked-out Genre category list:
    for x in range(len(userHistory)): 
        genre = db.getGenre(userHistory[x][0])
        if genre == "Science Fiction":
            scienceFictionUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Horror":
            horrorUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Fantasy":
            fantasyUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Romance":
            romanceUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Classics":
            classicsUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Sport":
            sportUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Music":
            musicUser.append(db.getTitle(userHistory[x][0]))
        elif genre == "Food & Drink":
            foodAndDrinkUser.append(db.getTitle(userHistory[x][0]))

#  Maintains a count of the total number of books per Genre that the Member has checked-out:    
    totalBooks = 0
    genreCount.append(len(scienceFictionUser))
    genreCount.append(len(horrorUser))
    genreCount.append(len(fantasyUser))
    genreCount.append(len(romanceUser))
    genreCount.append(len(classicsUser))
    genreCount.append(len(sportUser))
    genreCount.append(len(musicUser))
    genreCount.append(len(foodAndDrinkUser))
    for x in range(len(genreCount)):
         totalBooks += genreCount[x]

#  Sorts the Member Genre categories in popularity order starting with the most checked-out books:
    genreSorted = genreCount.copy()
    sortedGenreIndexes = []
    for x in range(8):
        genrePosition = genreSorted.index(max(genreSorted))
        genreSorted[genrePosition] = -1
        sortedGenreIndexes.append(genrePosition)

#  Creates a recommended list (between 3-10 books) of Titles for each Genre of those books that are available (i.e. not out on-loan):
    potentialBooks = []
    for x in range(8): 
        if sortedGenreIndexes[x] == 0:
            scienceFictionTotal = getBooksInGenre("Science Fiction")  # Get list of all available books in Genre.
            for element in scienceFictionUser:
                if element in scienceFictionTotal:
                    scienceFictionTotal.remove(element)  # Remove any book that the Member has previously checked-out.
            potentialBooks.append(scienceFictionTotal)
            recommendAmount = round(numberToRecommend(len(scienceFictionUser), totalBooks)) #  Determine how many books to recommend to Member for that Genre.
            temp1 = potentialBooks[0]
            for x in range(recommendAmount):  # Randomly select the books to recommend based on the number of books to recommend for that Genre.
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 1: 
            horrorTotal = getBooksInGenre("Horror")
            for element in horrorUser:
                if element in horrorTotal:
                    horrorTotal.remove(element)
            potentialBooks.append(horrorTotal)
            recommendAmount = round(numberToRecommend(len(horrorUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 2: 
            fantasyTotal = getBooksInGenre("Fantasy")
            for element in fantasyUser:
                if element in fantasyTotal:
                    fantasyTotal.remove(element)
            potentialBooks.append(fantasyTotal)
            recommendAmount = round(numberToRecommend(len(fantasyUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 3: 
            romanceTotal = getBooksInGenre("Romance")
            for element in romanceUser:
                if element in romanceTotal:
                    romanceTotal.remove(element)
            potentialBooks.append(romanceTotal)
            recommendAmount = round(numberToRecommend(len(romanceUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 4: 
            classicsTotal = getBooksInGenre("Classics")
            for element in classicsUser:
                if element in classicsTotal:
                    classicsTotal.remove(element)
            potentialBooks.append(classicsTotal)
            recommendAmount = round(numberToRecommend(len(classicsUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 5: 
            sportTotal = getBooksInGenre("Sport")
            for element in sportUser:
                if element in sportTotal:
                    sportTotal.remove(element)
            potentialBooks.append(sportTotal)
            recommendAmount = round(numberToRecommend(len(sportUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 6: 
            musicTotal = getBooksInGenre("Music")
            for element in musicUser:
                if element in musicTotal:
                    musicTotal.remove(element)
            potentialBooks.append(musicTotal)
            recommendAmount = round(numberToRecommend(len(musicUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break

        elif sortedGenreIndexes[x] == 7: 
            foodAndDrinkTotal = getBooksInGenre("Food & Drink")
            for element in foodAndDrinkUser:
                if element in foodAndDrinkTotal:
                    foodAndDrinkTotal.remove(element)
            potentialBooks.append(foodAndDrinkTotal)
            recommendAmount = round(numberToRecommend(len(foodAndDrinkUser), totalBooks))
            temp1 = potentialBooks[x]
            for x in range(recommendAmount):
                if len(temp1) > 0:
                    random = r.randint(0, (len(temp1))-1)
                    output1.append(temp1[random])
                    temp1.remove(temp1[random])
                else:
                    break
#  Return the list of recommended books and the current Genre count of read books for the Member ID:
    output2.append(output1)
    output2.append(genreCount)

    return output2      


def getBooksInGenre(genre):
    """ Returns a list of all potential Book Titles to recommend within a received Genre that are not 
    currently on-loan and not already extracted due to multiple versions of same book. """

    output = []
    books = db.loadFile("database.txt")
    for x in range(len(books)):
        if books[x][1] == genre and books[x][5] == "0\n" and books[x][2] not in output: # makes sure books are not on loan to another Member or have already been added due to multiple versions of same book
            output.append(books[x][2])
    return output

def numberToRecommend(genreNumber, totalNumber):
    """ Returns the number of books to recommend (based on a maximum recommendation of 10 books) for a 
    specific Genre category based on the Member's Genre reading history preferences. """
    
    output = 0
    if totalNumber > 0:
        output = (genreNumber/totalNumber) * 10
    return output  

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#  Tests  
#  =====
#  ID.  Test Case                                           Test Result                                                                       Pass/ Fail        
#  ~~~  ~~~~~~~~~                                           ~~~~~~~~~~~                                                                       ~~~~~~~~~~     
# 
#  01   Recommend a book with an invalid Member ID = 'Z1££' Error msg: 'Member ID must consist of four alphanumeric characters'.              Fail
#        
#  02   Recommend a book with an invalid Member ID = 'Z1'   Error msg: 'Member ID must consist of four alphanumeric characters'.              Fail
#       with less than 4 characters 
#
#  03   Recommend a book with a valid Member ID = 'MWD1'    List of between 3 and 10 books displayed in popularity proportions for MWD1:      Partial  
#       MWD1 book checkout history:                         5 Sport, 2 Music, 1 Classic and 1 Food & Drink.                                   Improve selection to prioritise books   
#       2 Classics                                          Correctly listed in Genre popularity order.                                       popular with other Members.  
#       7 Sport                                             Bar chart showing Genre popular preferences for MWD1 correctly.
#       3 Music
#       2 Food and Drink
#
#  04   Recommend a book for a valid Member ID = 'ZZZ1'     Error msg: 'Member ID has no book checkout history'.                
#       that has zero history of book checkouts
#-----------------------------------------------------------------------------------------------------------------------------------------------------------