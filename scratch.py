#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alan
#
# Created:     18/06/2013
# Copyright:   (c) alan 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import mysql.connector
import xml.etree.cElementTree as et
posts_input_file = r'H:\kaggle\Stack Exchange Data Dump - Mar 2013\Content\Posts.xml'

def test():
    cnx = mysql.connector.connect(host='localhost',user='alan',password='birkbeck',database='stackoverflow2013',buffered=True)
    cursor = cnx.cursor()
    SelectStmnt=('Select CloseReasonId, creationdate from PostHistory where PostId = 4986674')
    cursor.execute(SelectStmnt)
    # need to iterate over to see if any are not null and sort by date
    something = cursor.fetchall()
    print(something)

def test1():

    # get an iterable
    context = et.iterparse(posts_input_file, events=("start", "end"))
    print(context)

    # turn it into an iterator
    context = iter(context)
    print(context)

    # get the root element
    print(context.root)
    event, root = context.__next__()

    for event, elem in context:
        if event == "end" and elem.tag == "row":
            #... process record elements ...
            root.clear()
    #for event, element in et.iterparse(posts_input_file):

def main():
    test()

if __name__ == '__main__':
    main()
