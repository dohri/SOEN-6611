import fileinput
import re
import urllib2
import os
from BeautifulSoup import BeautifulSoup as beau
import MySQLdb as mdb
import sys
import time

# Set system encoding to 'UTF-8'
reload(sys)
sys.setdefaultencoding('UTF8')

bugsStatusList = []
bugsIdList = []
bugsPriorityList = []
bugsSummaryList = []
bugsOSList = []
bugsDescriptionList = []
bugsCommentsDictionary = dict()

def getBugsID():
    elements = soup.findAll("td", {"class": "vt id col_0"})
    for i in elements:
        bug_ids_temp = i.findAll("a")
        for bugID in bug_ids_temp:
            bugsIdList.append(bugID.text)

def getBugsOS():
    elements = soup.findAll("td", {"class": "vt col_9"})
    for i in elements:
        aLink = i.findAll("a")
        for i in aLink:
            # print(i.text)
            str1 = i.text
            str1 = str1.replace('\n', '')
            bugsOSList.append(str1)

def getBugsPriority():
    elements = soup.findAll("td", {"class": "vt col_1"})
    for i in elements:
        aLink = i.findAll("a")
        for i in aLink:
            str1 = i.text
            str1 = str1.replace('\n', '')
            bugsPriorityList.append(str1)

def getBugsSummary():
    elements = soup.findAll("td", {"class": "vt col_8"})

    temp = []
    for item in elements:
        aLink = item.findAll("a")
        for link in aLink:
            str1 = link.text
            str1 = str1.replace('\n', '')
            temp.append(str1)

    temp1 = []
    for i in elements:
        aLink = i.findAll('a', {"class": "label"})
        for i in aLink:
            str1 = i.text
            str1 = str1.replace('\n', '')
            temp1.append(str1)

    temp3 = [x for x in temp if x not in temp1]
    bugsSummaryList.extend(temp3)  # append bugsSummaryList with data in temp3

def getBugsStatus():
    elements = soup.findAll("td", {"class": "vt col_6"})
    for i in elements:
        aLink = i.findAll("a")
        for i in aLink:
            str1 = str(i.text)
            str1 = str1.replace('\n', '')
            bugsStatusList.append(str1)

def getBugsDescriptionAndComments():
    elements = soup.findAll("td", {"class": "vt id col_0"})
    for i in elements:
        bug_ids_temp = i.findAll("a")
        for bugID in bug_ids_temp:
            bugURL = 'https://code.google.com/p/chromium/issues/detail?id=' + str(bugID.text)
            htm = urllib2.urlopen(bugURL)
            soupObject = beau(htm)

            # Get Issue Description
            elm = soupObject.findAll("div",{"class":"cursor_off vt issuedescription"})
            for i in elm:
                descriptionText = i.findAll("pre")
                for description in descriptionText:
                    bugsDescriptionList.append(description.text)#descriptionTemp)

            # Get Comments List
            elm = soupObject.findAll("div",{"class":"cursor_off vt issuecomment"})
            commentsList = []
            for i in elm:
                commentsText = i.findAll("pre")
                for comment in commentsText:
                    commentsList.append(comment.text)
            bugsCommentsDictionary[bugID] = commentsList

def getBugsDescriptionAndCommentsFromDump():

    filesDirectoryList = []
    for (dirPath, dirNames, fileNames) in os.walk("/Users/firasmourtada/Documents/SOEN 6611/raw_chrome_issue"):
        filesDirectoryList.extend(fileNames)
        break

    for bugID in bugsIdList:
        if (("%s.txt" % bugID) in fileNames):
            with open (("/Users/firasmourtada/Documents/SOEN 6611/raw_chrome_issue/%s.txt" % bugID), "r") as bugfile:
                htmlData = bugfile.read().replace('\n', '')
            soupObject = beau(htmlData)

            # Get Issue Description
            elm = soupObject.findAll("div",{"class":"cursor_off vt issuedescription"})
            for i in elm:
                descriptionText = i.findAll("pre")
                for description in descriptionText:
                    bugsDescriptionList.append(description.text)

            # Get Comments List
            elm = soupObject.findAll("div",{"class":"cursor_off vt issuecomment"})
            commentsList = []
            for i in elm:
                commentsText = i.findAll("pre")
                for comment in commentsText:
                    commentsList.append(comment.text)
            bugsCommentsDictionary[bugID] = commentsList
        else:
            bugsDescriptionList.append("BugID \'%s\' is not available in the dump." % bugID)

def creatDatabase(dbConnection, dbName):
    with dbConnection:
        cur = dbConnection.cursor()
        cur.execute("DROP DATABASE IF EXISTS %s" % dbName)
        print "Database Name: %s" % dbName
        cur.execute("CREATE DATABASE %s" % dbName)
        cur.execute("ALTER DATABASE Chrome_Performance CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cur.execute("USE %s" % dbName)

def creatDatabaseSchema(dbConnection, dbTablesSchema):
    with dbConnection:
        cur = dbConnection.cursor()
        for dbTableName, dbTableAttributes in dbTablesSchema.iteritems():
            cur.execute("DROP TABLE IF EXISTS %s" % dbTableName)

            # Create Table
            print "Table Name: %s" % dbTableName
            query = "CREATE TABLE " + dbTableName + "("
            for attribute in dbTableAttributes:
                if (attribute.split(" ")[0] != "Primary" or attribute.split(" ")[0] != "Foreign"):       # Skip the attribute for Primary/Foreign Key setup Ex: ('PRIMARY KEY (BugID,KeywordID)')
                    query += attribute + ", "
            query = query[:-2] + ");"       # Removing the last comma
            print query
            cur.execute(query)

        # Setting Character set to 'UTF-8'
        cur.execute("ALTER TABLE Keyword CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cur.execute("ALTER TABLE Bug CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cur.execute("ALTER TABLE Comment CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;")
        cur.execute("ALTER TABLE Keyword_Bug CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;")
        #  Manually Setting Primary/Foreign Keys
        cur.execute("ALTER TABLE Keyword_Bug ADD PRIMARY KEY(BugID,KeywordID);")
        cur.execute("ALTER TABLE Keyword_Bug ADD FOREIGN KEY fk_bug(BugID) REFERENCES Bug(BugID) ON DELETE NO ACTION ON UPDATE CASCADE;")
        cur.execute("ALTER TABLE Keyword_Bug ADD FOREIGN KEY fk_keyword(KeywordID) REFERENCES Keyword(KeywordID) ON DELETE NO ACTION ON UPDATE CASCADE;")
        cur.execute("ALTER TABLE Comment ADD FOREIGN KEY fk_bug(BugID) REFERENCES Bug(BugID) ON DELETE NO ACTION ON UPDATE CASCADE;")

def insertDatabaseRecords(dbConnection, dbTableName, dbTableAttributes, dbTableAttributesData):
    with dbConnection:
        cur = dbConnection.cursor()
        baseQuery = "INSERT INTO " + dbTableName + " ("
        for attribute in dbTableAttributes:
            baseQuery += attribute + ", "
        baseQuery = baseQuery[:-2]      # Removing the last comma

        if(type(dbTableAttributesData[0]) != dict):
            for row in xrange(0, len(dbTableAttributesData[0])):
                query = baseQuery + ") VALUES ("
                try:
                    for column in xrange(0, len(dbTableAttributesData)):
                        recordEntryValue = dbTableAttributesData[column][row].strip().replace("\'","")
                                         # dbTableAttributesData[column][row] => Returns each data element from each list in the dbTableAttributesData list
                                         # .strip().replace("\'","")   => Removes single quotes from the data
                                         #                              to avoid messing the query
                        try:
                            query += "\'" + recordEntryValue.encode('utf-8',errors='strict') + "\',"
                        except TypeError:
                            query += "\'" + recordEntryValue + "\',"
                    query = query[:-1] + ");"       # Removing the last comma
                    cur.execute(query)
                except mdb.Error, e:
                    print "Database Error %d: %s" % (e.args[0],e.args[1])
                    continue
                except StandardError, e:
                    print "Error in BugID = %s" % dbTableAttributesData[1][row]
                    continue
        else:
            for bugID, bugComments in dbTableAttributesData[0].iteritems():
                for comment in bugComments:
                    try:
                        recordEntryValue = comment.strip().replace("\'","")#.encode('utf-8',errors='strict')
                        if (dbTableName == 'Comment'):
                            query = "%s) VALUES (\'%s\', \'%s\');" % (baseQuery,recordEntryValue,bugID)
                        else:
                            query = "%s) VALUES (\'%s\', \'%d\');" % (baseQuery,recordEntryValue,bugID)
                        cur.execute(query)
                    except mdb.Error, e:
                        print "Database Error %d: %s" % (e.args[0],e.args[1])
                        continue
                    except StandardError, e:
                        print "Error in BugID = %s" % bugID
                        continue

def getDatabaseRecords(dbConnection, dbTableName, dbTableAttributesParameters):
    with dbConnection:
        cur = dbConnection.cursor()
        columns = ""
        parameters = ""
        for column, parameter in dbTableAttributesParameters.iteritems():
            columns += "%s, " % column
            parameters += "%s=\'%s\' and " % (column,parameter)
            " %s from %s where "

        query = "select %s from %s where %s" % (columns, dbTableName, parameters)
        query = query[-4] + ";"
        result = cur.execute(query)
        return cur.fetchall()

def getKeywordID(dbConnection, searchKeyword):
    with dbConnection:
        cur = dbConnection.cursor()
        query = "select KeywordID from Keyword where SearchKeyword = \'%s\'" % searchKeyword
        print "getKeywordID query: %s" % query
        keywordID = cur.execute(query)
        return cur.fetchall()

############################################# Main Script ################################################

ConfigAttributes = fileinput.input()
url = ConfigAttributes[0].split()[2].split('|')
searchKeywords = ConfigAttributes[1].split(' = ')[1].split('|')    # Contains a list of all keywords

######################################## DATABASE Initialization #########################################

try:
    dbConnection = mdb.connect('localhost', 'root');

    DATABASE_NAME = "Chrome_Performance"
    DATABASE_TABLES_SCHEMA = {'Keyword': ['KeywordID INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
                                          'SearchKeyword VARCHAR(255)'],

                               'Bug': ['BugID VARCHAR(255) PRIMARY KEY',
                                       'Priority VARCHAR(255)','Status VARCHAR(255)',
                                       'Summary VARCHAR(255)',
                                       'OS VARCHAR(255)',
                                       'BugDescription LONGTEXT'],

                               'Comment': ['CommentID INT NOT NULL AUTO_INCREMENT PRIMARY KEY',
                                           'CommentDescription LONGTEXT',
                                           'BugID VARCHAR(255)'],

                               'Keyword_Bug': ['BugID VARCHAR(255)','KeywordID INT']}

    DATABASE_TABLES_Attributes = {'Keyword': ['SearchKeyword'],
                                  'Bug': ['BugID','Priority','Status','Summary','OS','BugDescription'],
                                  'Comment': ['CommentDescription','BugID'],
                                  'Keyword_Bug': ['BugID','KeywordID']}

    # Create database and database schema
    creatDatabase(dbConnection, DATABASE_NAME)
    creatDatabaseSchema(dbConnection, DATABASE_TABLES_SCHEMA)

    # Inserting Keywords to database
    keywordsTableAttributesData = [searchKeywords]
    insertDatabaseRecords(dbConnection, 'Keyword', DATABASE_TABLES_Attributes['Keyword'], keywordsTableAttributesData)

######################################## Information Extraction #########################################

    for keyword in searchKeywords:
        bugUrl = url[0] + keyword.strip() + url[1] + '0'
        htmlResponse = urllib2.urlopen(bugUrl)
        soup = beau(htmlResponse)
        elements = soup.findAll("div", {"class": "pagination"})

        numericMatch =  re.match(r"([0-9]+)([a-zA-Z]*)(&*)([a-zA-Z]*)", elements[-1].text.split("\n")[-1].split(" ")[-1]) # Extract numeric section
        if numericMatch:
            numericItems = numericMatch.groups()
            print "Total No. of Bugs = %s, for search criteria: %s" % (numericItems[0], keyword)
            totalNoOfIssues = int(numericItems[0])
            if (totalNoOfIssues > 1000):
                if ((totalNoOfIssues % 1000) > 0):
                    totalNoOfPages = totalNoOfIssues / 1000 + 1         # Ex: 2323 issues are listed in 3 pages
                else:
                    totalNoOfPages = totalNoOfIssues / 1000             # Ex: 2000 issues are listed in 2 pages
            else:
                totalNoOfPages = 1                                      # 1000 issues and less are listed in 1 page

            startingIssueNo = 0
            range = totalNoOfPages + 1
            for pageNumber in xrange(1, range):
                bugUrl = url[0] + keyword.strip() + url[1] + str(startingIssueNo)
                htmlResponse = urllib2.urlopen(bugUrl)
                soup = beau(htmlResponse)
                getBugsID()
                getBugsPriority()
                getBugsStatus()
                getBugsSummary()
                getBugsOS()
                getBugsDescriptionAndCommentsFromDump()
                startingIssueNo = (pageNumber * 1000) + 1
                time.sleep(60)

        # Inserting bugs to database
        bugsTableAttributesData = [bugsIdList,bugsPriorityList,bugsStatusList,bugsSummaryList,bugsOSList,bugsDescriptionList]
        insertDatabaseRecords(dbConnection, 'Bug', DATABASE_TABLES_Attributes['Bug'], bugsTableAttributesData)

        # Link bugs with keywords
        results = getKeywordID(dbConnection, keyword.strip())
        searchKeywordID = results[0][0]
        Keyword_BugTableAttributesData = [{searchKeywordID : bugsIdList}]
        insertDatabaseRecords(dbConnection, 'Keyword_Bug', DATABASE_TABLES_Attributes['Keyword_Bug'], Keyword_BugTableAttributesData)

        # Inserting bugs' comments to database
        commentsTableAttributesData = [bugsCommentsDictionary]
        insertDatabaseRecords(dbConnection, 'Comment', DATABASE_TABLES_Attributes['Comment'], commentsTableAttributesData)
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:
    if dbConnection:
        dbConnection.close()


