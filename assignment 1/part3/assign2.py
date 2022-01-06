#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

from itertools import combinations
import sys
import time
import copy


def sucessors(current_list, pendingList):
    succ_list= []
    combList = []
   
    
    #append single student grouplist
    list_of_1 = combinations(pendingList,1)
    for tup in list_of_1:
        combList.append(tup)

    #append group of 2 to the grouplist
    list_of_2 = combinations(pendingList,2)
    for tup in list_of_2:
        combList.append(tup)

    #append group of 3 to the grouplist
    list_of_3 = combinations(pendingList,3)
    for tup in list_of_3:
        combList.append(tup)
    
    
    #create successor list for current successor
    for comb in combList:
        succ = copy.deepcopy(current_list)
        # print(comb)
        succ.append(comb)
        # print(succ)
        succ_list.append(succ)

    # print("currentList list: ", current_list)
    # print("")
    # print("comb list: ", combList)
    # print("")
    # print("succ list: ", succ_list)
    # print("")
    return succ_list



def sortFringe(fringe):
        fringe.sort(key = lambda x: x[1])
        return fringe


def foundGoal(succ,studentList):
    count = 0
    for group in succ:
        for student in group:
            if student in studentList:
                count +=1
    if count == len(studentList):
        return True
    else:
        return False

def findTime(groupList, group_pref):
    total_time = 5 * len(groupList)

    for group in groupList: 
        for student in group:
            number_of_partners = group_pref[student]['num_of_partners']
            if((number_of_partners != len(group)) and (number_of_partners != 0) ):
                total_time += 2
            for person in group_pref[student]['include']:
                if (person == 'xxx' or person == 'zzz' ):
                    break
                if person not in group:
                    total_time += 3
            for person in group_pref[student]['exclude']:
                if person == "_":
                    break
                if person in group:
                    total_time += 10



    return total_time

def getPendingList(current_list, studentList):
    pendingList = []
    studentList = set(studentList)
    temp = set()
    if len(current_list) == 0: #handle initial condition where currentList is empty
        pendingList = studentList
    else:
        for group in current_list:
            for student in group:
                if student in studentList:
                    temp.add(student)
        pendingList = list(studentList - temp)
    return pendingList



def getGoalDict(succ, total_time):
    finalGroupList = []
    for tup in succ:
        team = '-'.join(tup)
        finalGroupList.append(team)
    return {"assigned-groups": finalGroupList, "total-cost" : total_time}





def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

 


    file = open(input_file, "r")
    studentList = []
    group_pref = {}
    num_of_partners = 0
    partners = ""
    does_not_want = ""
    for line in file:    
        word_list = line.split()
        # print(word_list)
        key = word_list[0]
        studentList.append(word_list[0])
        partners = word_list[1].split('-')
        num_of_partners = len(partners)
        group_pref[key] = {}
        group_pref[key]['num_of_partners'] = num_of_partners
        group_pref[key]['include'] = partners
        group_pref[key]['exclude'] = word_list[2].split(',')
    file.close()

    # print("list of students:")
    # print(studentList)
    # print("")
    # print("group preferences:")
    # for key in group_pref:
    #     print(key,":", group_pref[key])
    # print("")


    fringe =[ [[],0]  ]
    min_time = 10000
    while fringe:
        #fringe = sortFringe(fringe) # sort fringe
        (current_list, current_time) = fringe.pop() #dfs
        # print("current list before succ: ", current_list)
        pendingList = getPendingList(current_list,studentList)
        # print("pending list: ", pendingList)

        for succ in sucessors(current_list, pendingList):
            # print(succ)
            total_time = findTime(succ, group_pref)
            # print(succ, " ", total_time)
            if foundGoal(succ,studentList) and total_time < min_time:
                
                
                # call yeild
                # print("goal found: ", succ)
                # print("time taken: ", total_time)
                #yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"], "total-cost" : 9})
                yield(getGoalDict(succ, total_time))
                min_time = total_time
            else:
                fringe.append([succ,total_time])



    # Simple example. First we yield a quick solution
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
            #    "total-cost" : 12})

    # Then we think a while and return another solution:
    # time.sleep(10)
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
    #            "total-cost" : 10})

    # # This solution will never befound, but that's ok; program will be killed eventually by the
    # #  test script.
    # while True:
    #     pass
    


if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    # for result in solver(sys.argv[1]):
    #     print("----- Latest solution:\n" + "\n"(result["assigned-groups"]))
    #     print("\nAssignment cost: %d \n" % result["total-cost"])
    
