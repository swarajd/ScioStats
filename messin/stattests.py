import pandas as pd
import re
from collections import defaultdict, OrderedDict
import json

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


class Student(object):
    def __init__(self):
        self.avgRank  = AverageNumber()
        self.eventMap = defaultdict(int)
        self.teamName = None

    def __repr__(self):
        return "{}".format(self.avgRank.getAverage())


def runStats(rankFile, rosterFile):
    dataMap = {}

    rankdf = pd.read_excel(rankFile)
    rosterdfs = pd.read_excel(rosterFile, None)

    schoolPlacementNum(rankdf, dataMap)
    studentInfo(rankdf, rosterdfs, dataMap)

    # for name, table in dataMap.items():
    #     print(name)
    #     print(table)
    #     print("===================")

# basic stat
def schoolPlacementNum(rankdf, dataMap): 
    schoolNames = rankdf["Team"].map(lambda team: re.compile("(HS|SS)") \
                                       .split(team)[0] \
                                       .strip())
    
    medalNums = rankdf.iloc[:,2:23].values
    medalNums = list(map(
                    lambda ranks: len(list(filter(
                        lambda rank: rank <= 6, 
                        ranks))), 
                    medalNums
                ))

    schoolMedalMap = defaultdict(int)
    
    for i, school in enumerate(schoolNames):
        schoolMedalMap[school] += medalNums[i]
    
    # schoolMedalMap = OrderedDict(sorted(schoolMedalMap.items(), key=lambda x: x[1]))

    # for school, placement in schoolMedalMap.items():
    #     print("{} placed in {} event(s)".format(school, placement))

    dataMap["schoolMedalMap"] = schoolMedalMap
    

# advanced stat
def studentInfo(rankdf, rosterdfs, dataMap):

    # studentAverageRank = defaultdict(AverageNumber)
    # studentRanks       = defaultdict(lambda: defaultdict(int))
    studentMap         = defaultdict(Student)

    # team names
    for teamName in rosterdfs.keys():
        teamRanks = rankdf[rankdf.Team == teamName].copy()
        teamRanks.rename(columns=lambda x: x[:-1].rstrip(), inplace=True)
        # print(teamRanks)
        # events
        for _, row in rosterdfs[teamName].iterrows():
            event = row[0]
            students = row[1:4]
            students = students[students.notnull()]
            place = teamRanks[event].values[0]
            for student in students:
                studentMap[student].eventMap[event] = place
                studentMap[student].avgRank += place
                if (studentMap[student].teamName is None):
                    studentMap[student].teamName = teamName
                # studentAverageRank[student] += place
                # studentRanks[student][event] = place

    
    # for student, ranks in studentRanks.items():
    #     print(student, dict(ranks))

    for student in studentMap:
        print("{}, {}".format(student, studentMap[student]))

    # for student in studentAverageRank:
    #     print("[{}] Average Rank: {}".format(student, studentAverageRank[student]))

    # dataMap["studentAverageRank"] = studentAverageRank
    # dataMap["studentRanks"] = studentRanks
    dataMap["studentMap"] = studentMap

        



runStats(open("divc.xlsx", "rb"), open("teams.xlsx", "rb"))