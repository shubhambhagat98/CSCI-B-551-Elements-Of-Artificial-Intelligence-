from itertools import combinations
from itertools import product

students = ['A', 'B', 'C', 'D','E', 'F']

print("team of 2 students:")
# list_of_1 = combinations(students,1)
# for team in list_of_1:
#     print(team)

# list_of_2 = combinations(students,2)
# for team in list_of_2:
#     print(team)

# list_of_3 = list(combinations(students,3))
# # print(type(list_of_3))
# for team in list_of_3:
#     print(team)
    # print(type(team))

# def sortFringe(fringe):
#         fringe.sort(key = lambda x: x[1])
#         return fringe

# fringe = [[[1,2,3,4], 3], [[4,5,6,7],2],[[7,8,9,10],1]]
# print(sortFringe(fringe))

# def printList(demoList):
#     print("list: ",demoList)

demoList  = ('g', 'e', 'e', 'k', 's')
output = '-'.join(demoList)
print(output)
