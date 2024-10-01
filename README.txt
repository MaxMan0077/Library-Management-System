Library Management System v1.4
==============================

Introduction:
============
This application presents a simple library management system for use by a librarian.  It provides the 
following features enabling the librarian to search for books by title to check their availability, check-out 
available books and return any books the members currently have out on-loan.  The librarian is also able 
to recommend books to a member based on the member's preferred reading history.
The application is supported by two eternal text files: database.txt that stores the details of all books in 
the library; and logfile.txt that stores the transaction check-out and return history of library books.

Installation and running the application:
========================================

==WARNING==
Some IDEs that I have used have not recognised the .txt files within the project. The IDE used to develop this
project was visual studio code where the program runs without error within a workspace.

The following directory structure and file objects are provided as part of the installation package:

|----  Library Management System1.4
       |----  menu.py
       |----  booksearch.py
       |----  bookcheckout.py
       |----  bookreturn.py
       |----  bookrecomend.py
       |----  database.py
       |----  database.txt
       |----  logfile.txt
       |----  README.txt

To execute the application menu.py should be called either from a command line or a standard IDE.

Program structure:
=================

|----  menu.py
       |----  booksearch.py
                 |----  database.py
       |----  bookcheckout.py
                 |----  database.py
       |----  bookreturn.py
                 |----  database.py
       |----  bookrecommend.py
                 |----  database.py

External file structures:
========================
On installation, both database.txt and logfile.xt are provided with representative sample data.

|----  database.txt
       |----  book ID
       |----  genre
       |----  title
       |----  author
       |----  purchase date
       |----  member ID or 0

**  Member ID or 0 field denotes loan status. If the book is available, then records 0. If on-loan records Member ID. 

|----  logfile.txt
       |----  book ID
       |----  checkout/ return date
       |----  member ID or '~'

**  Member ID or '~' field denotes whether the book is being checked-out (Member ID) or returned ('~'). 

Program concepts:
================
Data manipulation and maintenance for both database.txt and logfile.txt is extensively supported in the 
use of both single and two-dimensional lists (arrays).  This is seen as a much cleaner approach than 
programming the system to update the external text files directly.   
 
The feature to recommend books to a member based on the member's preferred reading history is the 
most complex aspect of the application and as such the following provides a brief explanation to how the 
system operates:  The system establishes the reading preferences for a particular member by examining 
the member's reading history recorded by book checkout records as held on logfile.txt.  From this, totals 
by genre are calculated for the member.  Based on a maximum of ten books in total, the number of books 
to recommend is split out at the genre level for that member using a simple proportion ratio calculation. A 
random selection of the books to recommend at the genre level is performed excluding books which are 
either currently out on-loan or previously been checked-out by the member.  The list of recommended 
book titles for the member is displayed to the librarian together with a graph bar chart detailing the genre 
preferences for the member.
