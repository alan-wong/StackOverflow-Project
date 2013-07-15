#-------------------------------------------------------------------------------
# Name:        convertxmltocsv
# Purpose:
#
# Author:      alanwong
#
# Created:     10/06/2013
# Copyright:   (c) alanwong 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xml.etree.cElementTree as et
import csv
import collections
from datetime import datetime
#import mysql.connector

posts_input_file = r'H:\kaggle\Stack Exchange Data Dump - Mar 2013\Content\Posts.xml'
posts_output_dest = r'H:\kaggle\Stack Exchange Data Dump - Mar 2013\Content\PostsCorrected.csv'
post_xml_headers_to_use = [ 'PostId',
                            'PostCreationDate',
                            'OwnerUserId',
                            'OwnerCreationDate',
                            'ReputationAtPostCreation',
                            'OwnerUndeletedAnswerCountAtPostTime',
                            'Title',
                            'BodyMarkdown',
                            'Tag1',
                            'Tag2',
                            'Tag3',
                            'Tag4',
                            'Tag5',
                            'PostClosedDate',
                            'OpenStatus',
                            'Score',
                            'FavoriteCount',
                            'LastEditDate',
                            'CommentCount',
                            'AnswerCount',
                            'ViewCount',
                            'LastEditorUserId',
                            'AcceptedAnswerId',
                            'LastActivityDate']

post_xml_date_headers = ['LastEditDate',
                         'LastActivityDate']

def split_tags(line, tags):
    kLess = '<'
    kMore = '>'

    index = 0
    while (line.find(kLess, index)) != -1:
        less_than = line.find(kLess, index)
        if (line.find(kMore, less_than)) != 1:
            greater_than = line.find(kMore, less_than)
            val = line[less_than+1:greater_than]
            index = greater_than+1
            #print(val)
            if val not in tags:
                tags.append(val)

def convert_db_time_to_str(time):
    # get rid of the T
    test = time.replace('T', ' ')
    # find the microsecond . separator
    i  = test.find('.')
    # trim it
    test = test[0:i]
    # convert to datetime object
    src_date_time = datetime.strptime(test, '%Y-%m-%d %H:%M:%S')
    # convert to our desired format
    dst_date_time = src_date_time.strftime('%d/%m/%Y %H:%M:%S')
    return dst_date_time

def convert_post_xml_to_csv():
    n = 0
    count = 0
    stored_header = False
    header_written = False
    append = False
    lines1 = []
    headers = []
    # get an iterable
    context = et.iterparse(posts_input_file, events=("start", "end"))
    # turn it into an iterator
    context = iter(context)
    # get the root element
    event, root = context.__next__()

    for event, element in context:
        if event == "end" and element.tag == "row":
            if (stored_header is False):
                headers = (element.attrib.keys())
                #print(element.attrib.keys())
                stored_header = True

            headers1 = element.attrib
            if element.attrib.get('PostTypeId') is '1':
                  # split the tags that are stored in a single string in angle brackets
                tags=[]
                split_tags(element.attrib.get('Tags'),tags)
               #print(tags)
               # construct our list in order
                id = 1
                for tag in tags:
                   title = 'Tag' + str(id)
                   element.attrib[title] = tag
                   id += 1

                #reformat the headers to Kaggle style
                element.attrib['PostId'] = element.attrib.get('Id')
                element.attrib['PostCreationDate'] = convert_db_time_to_str(element.attrib.get('CreationDate'))
                element.attrib['BodyMarkdown'] = element.attrib.get('Body')
                element.attrib['PostClosedDate'] = convert_db_time_to_str(element.attrib.get('ClosedDate'))
                lines1.append(element.attrib)
               # convert the daft dates
                for dateStr in post_xml_date_headers:
                   if element.attrib.get(dateStr) is not None:
                      element.attrib[dateStr] = convert_db_time_to_str(element.attrib.get(dateStr))

            #print element.tag, element.attrib
            root.clear()
            del element
            n+=1
            count+=1
            # flush every 100000 rows
            if n > 100000:
                if append is False:
                    with open(posts_output_dest, 'w',encoding='utf-8') as hw:
                        header_witer = csv.DictWriter(hw, post_xml_headers_to_use, extrasaction = "ignore", lineterminator='\n')
                        if header_written is False:
                            header_witer.writeheader()
                            header_written = True
                            #print(headers1)
                            header_witer.writerows(lines1)
                            lines1 = []
                            n = 0
                            print('count ' + str(count))
                            append = True
                else:
                    with open(posts_output_dest, 'a',encoding='utf-8') as hw:
                        header_witer = csv.DictWriter(hw, post_xml_headers_to_use, extrasaction = "ignore", lineterminator='\n')
                        #print(headers1)
                        header_witer.writerows(lines1)
                        lines1 = []
                        n = 0
                        print('count ' + str(count))

    with open(posts_output_dest, 'a',encoding='utf-8') as hw:
         header_witer = csv.DictWriter(hw, post_xml_headers_to_use, extrasaction = "ignore", lineterminator='\n')
         #print(headers1)
         header_witer.writerows(lines1)

def get_open_close_reason(post_id):
    cnx = mysql.connector.connect(host='localhost',user='alan',password='birkbeck',database='stackoverflow2013',buffered=True)
    cursor = cnx.cursor()
    SelectStmnt=('Select CloseReason from PostHistory where PostId =%s')
    cursor.execute(SelectStmnt, post_id)
    for closeReason in cursor:
        return closeReason
    return ''

def add_reputation_at_post_creation(user_id):
    pass

def get_owner_undeleted(user_id):
    pass

def main():
    convert_post_xml_to_csv()
    pass

# snippet to count the numer of rows
def count_csv_rows(csvFile):
    f = open(csvFile, encoding = 'utf-8')
    count = 0
    for row in csv.reader(f):
        # handle empty rows
        if len(row) is not 0:
            count +=1

    # this will count empty rows
    otherCount = sum(1 for row in csv.reader(open(posts_output_dest, encoding = 'utf-8')))
    print(csvFile)
    print('total without blank lines is: ' + str(count))
    print('total with possible blank lines is: ' + str(otherCount))



if __name__ == '__main__':
    count_csv_rows(r'h:\kaggle\basic_benchmark.csv')
    count_csv_rows(r'h:\kaggle\basic_benchmark_Oct.csv')
    count_csv_rows(r'h:\kaggle\public_leaderboard.csv')
