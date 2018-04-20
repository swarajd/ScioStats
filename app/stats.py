import pandas as pd
import re, difflib
from collections import defaultdict, OrderedDict

#
# a class that can keep track of averages over time
#
class AverageNumber(object):
    def __init__(self, v=0):
        self.count = 0
        self.value = v

    def __iadd__(self, n):
        self.count += 1
        self.value += n
        return self

    def getAverage(self):
        return (self.value * 1.0) / self.count

    def __repr__(self):
        return str(self.getAverage())

#
# a class that encapsulates
# - the average rank
# - the individual ranks
# - the team name
# of a student. This doesn't have name since it's being mapped to by name
#
class Student(object):
    def __init__(self):
        self.avgRank  = AverageNumber()
        self.eventMap = defaultdict(int)
        self.teamName = None

    def __repr__(self):
        return "[{}] {}".format(self.teamName, self.avgRank.getAverage())


def getStats(rankFile, rosterFile, dataMap):
    # first do basic statistics
    rankdf = pd.read_excel(rankFile)
    schoolPlacementNum(rankdf, dataMap)

    # if we have a roster file, go ahead and do advanced statistics
    if (rosterFile is not None):
        rosterdfs = pd.read_excel(rosterFile, None)
        studentInfo(rankdf, rosterdfs, dataMap)


#
# basic statistics
# this function maps the school to the number of events they placed in
#
def schoolPlacementNum(rankdf, dataMap): 
    # generalize the school names from the dataframe
    schoolNames = rankdf["Team"].map(lambda team: re.compile("(HS|SS)") \
                                       .split(team)[0] \
                                       .strip())
    
    # going through the rows and counting the number of times 
    # there is a place that is 1-6
    medalNums = rankdf.iloc[:,2:23].values
    medalNums = list(map(
                    lambda ranks: len(list(filter(
                        lambda rank: rank <= 6, 
                        ranks))), 
                    medalNums
                ))

    # creating the map from school to number of times the school placed
    schoolMedalMap = defaultdict(int)
    
    # populating the map
    for i, school in enumerate(schoolNames):
        schoolMedalMap[school] += medalNums[i]

    # add the school medal map to the overall data map
    dataMap["schoolMedalMap"] = schoolMedalMap
    

#
# advanced statistics
# this method gives the following info about each student from
# a given school's roster
# - ranks in each event
# - average rank
# - specific team from the school (A team, B team, etc)
#
def studentInfo(rankdf, rosterdfs, dataMap):

    # the map of students to their info
    studentMap = defaultdict(Student)

    # regex to parse out B or C at the end
    regex = re.compile('(B|C)$')

    # get event names
    eventNames = list(map(
        lambda x: regex.sub('', x).rstrip(), 
        rankdf.columns[2:-2].tolist()
    ))

    # loop through all the teams
    for teamName in rosterdfs.keys():

        # get the ranks for the relevant team
        teamRanks = rankdf[rankdf.Team == teamName].copy()

        # rename the columns so they match with the roster headers
        teamRanks.rename(columns=lambda x: regex.sub('', x).rstrip(), inplace=True)
        
        # parse the appropriate roster dataframe and populate the student map
        for _, row in rosterdfs[teamName].iterrows():

            # get the event name (account for spelling errors)
            event = difflib.get_close_matches(row[0], eventNames, 1)[0]

            # get the names of the students that partook in this event
            students = row[1:4]
            students = students[students.notnull()]

            # get the place that they got
            place = teamRanks[event].values[0]

            # populate the student map using the values obtained above
            for student in students:
                studentMap[student].eventMap[event] = place
                studentMap[student].avgRank += place
                if (studentMap[student].teamName is None):
                    studentMap[student].teamName = teamName
    
    # add the student map to the overall data map
    dataMap["studentMap"] = studentMap
