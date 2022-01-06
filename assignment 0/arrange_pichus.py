#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : SHUBHAM BHAGAT, snbhagat
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)

# def add_pichu1(new_house_map, row, col):

#--------------initial approach------------------------
# here I have broken down conditions for same row and same column w.r.t current row, curret column in two for loops
# before implementing diagonal-condition, I tried checking if my logic work for checking rows and columns.
# Unfortunately, it didn't work for pichu greater than 4, it was placing two pichu in same column.
#   row_flag = col_flag = False
#   for i in range(len(new_house_map)):
    #     if (new_house_map[i][col] == 'p'):
    #         row_flag = True
    #         break
    #     elif (new_house_map[i][col] == "X" or new_house_map[row][i] == "@"):
    #         break

    # for i in range(len(new_house_map[0])):
    #     if (new_house_map[row][i] == 'p'):
    #         col_flag = True
    #         break
    #     elif (new_house_map[row][i] == "X" or new_house_map[row][i] == "@"):
    #         break

    # if (row_flag== 1 and col_flag == False):
    #     return new_house_map[0:row] + [new_house_map[row][0:col] + ['p',] + new_house_map[row][col+1:]] + new_house_map[row+1:]

#------------------------approach 2- Status: partially correct-------------------------------------
# pytest output
# test_a0.py::test_question1_case1 PASSED                      [ 25%]
# test_a0.py::test_question2_case1 PASSED                      [ 50%]
# test_a0.py::test_question1_case2 PASSED                      [ 75%]
# test_a0.py::test_question2_case2 FAILED                      [100%]
# E     AssertionError: Pichus can see each other

# Here instead checking entire row or entire col in one iteration, I divided these conditions in different parts.
# such as checking row towards left of current row col in one condition, check row towards right of current row col in another condition and so on
# I studied n queens problem from "geeks for geeks" to understand how queens where place.
# link: https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/
# for n queens, n-1 queens were already placed in columns 0 to n-1
# thus they where only checking left side of the board for current location (row, col)
# ie: check left row, left upper diagonal, left bottom diagonal.
# However, for the given pichu problem, we can place two pichu in any direction if they are not in same row, col or diagonal.
# Additionly, even if two pichus are in same row, col or diagonal, we need to check if they can see each other or not.
# So for current (row,col) check all directions to see if we get a pichu first or 'X' first.
# For all 8 direction, if pichu is seen first then we can't place the current pichu at loaction (row,col).
# Else if 'X' is seen first, it means that no other pichu can see the current pichu at (row,col) since there will be a 'X' between them.
# Fisrt, I tired to combine the conditions for checking diagonal with top and bottom direction together 
# and checked left, right directions in two seperate for loops.
# when I tested the code using pytest, the code failed the test- "test_question2_case2" 
# I checked and realised that for map2, if pichu no. is greater than 6, it was placing two pichu in same diagonal who can see eacho ther.
# 
# . p . . X X X
# . X . X p . .    <===== notice pichu here
# . X . . X . .         and
# . X p X p . .    <===== 'first' pichu here. Both are in same diagonal and can see each other
# . X . X . X p
# p X . p . X @

#     top = bottom = left = right = top_left = top_right = bottom_left = bottom_right = False
#     for i in range(row - 1, -1, -1):
        
#         # check for top-left
#         for j in range(col-1, -1, -1):
#             if(new_house_map[i][j] == 'p'):
#                 top_left= True
#                 break
#             elif (new_house_map[i][j] == "X" or new_house_map[i][j] == "@"):
#                 break
        
#         # check for top-right
#         for k in range(col+1,len(new_house_map[0])):
#             if(new_house_map[i][k] == 'p'):
#                 top_left= True
#                 break
#             elif (new_house_map[i][k] == "X" or new_house_map[i][k] == "@"):
#                 break
        

#         # check for top
#         if(new_house_map[i][col] in 'p'):
#             top= True
#             break
#         elif (new_house_map[i][col] == "X" or new_house_map[i][col] == "@"):
#             break

    
#     for i in range(row+1,len(new_house_map)):
#         # check for top-left
#         for j in range(col-1, -1, -1):
#             if(new_house_map[i][j] == 'p'):
#                 bottom_left= True
#                 break
#             elif (new_house_map[i][j] == "X" or new_house_map[i][j] == "@"):
#                 break
            
#         # check for top-right
#         for k in range(col+1,len(new_house_map[0])):
#             if(new_house_map[i][k] == 'p'):
#                 bottom_left= True
#                 break
#             elif (new_house_map[i][k] == "X" or new_house_map[i][k] == "@"):
#                 break
#         # check for bottom   
#         if(new_house_map[i][col] in 'p'):
#             bottom= True
#             break
#         elif (new_house_map[i][col] == "X" or new_house_map[i][col] == "@"):
#             break
    
#     # check only for left
#     for i in range(col-1,-1,-1):
#         if(new_house_map[row][i] in 'p'):
#             left= True
#             break
#         elif (new_house_map[row][i] == "X" or new_house_map[row][i] == "@"):
#             break
          
#     # check only for right
#     for i in range(col+1,len(new_house_map[0])):
#         if(new_house_map[row][i] == 'p'):
#             right= True
#             break
#         elif (new_house_map[row][i] == "X" or new_house_map[row][i] == "@"):
#             break

#     if (top == left== bottom == right == top_left == top_right == bottom_left == bottom_right == False):
#         return new_house_map[0:row] + [new_house_map[row][0:col] + ['p',] + new_house_map[row][col+1:]] + new_house_map[row+1:]


#-------------------approach 2 - Status : PASSED ------------------------
#pytest output:
# test_a0.py::test_question1_case1 PASSED                 [ 25%]
# test_a0.py::test_question2_case1 PASSED                 [ 50%]
# test_a0.py::test_question1_case2 PASSED                 [ 75%]
# test_a0.py::test_question2_case2 PASSED                 [100%]

# Here, to solve the problem of having two pichu in same diagonal who can see each other for map2, when pichu no. greater 6
# I kept conditons for checking left, right, top, bottom, top-left-diagonal, top-right-diagonal, bottom-left-diagonal, bottom-right-diagonal
# in differnt blocks (using loop for different range).
# idea to use 'zip' function for checking diagonal was referred from n-queens problem of "geeks for geeks"
# link: https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/
def add_pichu(new_house_map, row, col):


    
    top = down = left = right = top_left = top_right = bottom_left = bottom_right = False
    for i in range(row-1,-1,-1):
        if(new_house_map[i][col] in 'p'):
            top= True
            break
        elif (new_house_map[i][col] == "X" or new_house_map[i][col] == "@"):
            break
    
    
    for i in range(row+1,len(new_house_map)):
        if(new_house_map[i][col] in 'p'):
            down= True
            break
        elif (new_house_map[i][col] == "X" or new_house_map[i][col] == "@"):
            break
        
    
    for i in range(col-1,-1,-1):
        if(new_house_map[row][i] in 'p'):
            left= True
            break
        elif (new_house_map[row][i] == "X" or new_house_map[row][i] == "@"):
            break
          
    
    for i in range(col+1,len(new_house_map[0])):
        if(new_house_map[row][i] == 'p'):
            right= True
            break
        elif (new_house_map[row][i] == "X" or new_house_map[row][i] == "@"):
            break
    
    for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)):
        if(new_house_map[i][j] == 'p'):
            top_left= True
            break
        elif (new_house_map[i][j] == "X" or new_house_map[i][j] == "@"):
            break
    
    
    for i,j in zip(range(row-1, -1, -1),range(col+1,len(new_house_map[0]))):
        if(new_house_map[i][j] == 'p'):
            top_right= True
            break
        elif (new_house_map[i][j] == "X" or new_house_map[i][j] == "@"):
            break

    
    for i,j in zip(range(row+1,len(new_house_map)),range(col-1, -1, -1)):
        if(new_house_map[i][j] == 'p'):
            bottom_left= True
            break
        elif (new_house_map[i][j] in "X" or new_house_map[i][j] == "@"):
            break
    
    
    for i,j in zip(range(row+1,len(new_house_map)),range(col+1,len(new_house_map[0]))):
        if(new_house_map[i][j] == 'p'):
            bottom_right= True
            break
        elif (new_house_map[i][j] in "X" or new_house_map[i][j] == "@"):
            break


    if (top == left== down == right == top_left == top_right == bottom_left == bottom_right == False):
        return new_house_map[0:row] + [new_house_map[row][0:col] + ['p',] + new_house_map[row][col+1:]] + new_house_map[row+1:]





#----------------------------------intial approach----------------------------
# Check if two pichu are in conflict
# for current location (row, col) if there was no other pichu in same row, same column or same diaginal- return false
# if there was a pichu in same row, same column and same diaonal, check if there is 'X' between them. if yes then return true
# unfortunately, the code didn't work.
# def checkAttack(curr_row, curr_col, pichu_loc, x_loc):   
#     for r in range(0, len(house_map)):
#         for c in range(0,len(house_map[0])):
#            if house_map[r][c] in pichu_loc:
        #         for x in x_loc:
        #             if ((curr_row != r) and (curr_col != c) and ( abs(c - curr_col) != abs(r - curr_row))):
        #                 return False
        #             elif ((curr_row == r == x[0]) and ((c < x[1] < curr_col) or (c > x[1] > curr_col))):
        #                 return False
        #             elif ((curr_col == c == x[1]) and ((r < x[0] < curr_row) or (r > x[0] > curr_row))):
        #                 return False
        #             elif ((abs(c - curr_col) == (abs(r - curr_row))) and ((r,c) < x < (curr_row,curr_row) or ((r,c) > x > (curr_row,curr_row)))):
        #                 return False
#     return True
#-------------------------------------------------------------------------------
    

# Get list of successors of given house_map state
#----------------------initial approach-----------------------------------------
# For every successor-housemap, I tried traversed the housemap and tried to compare each location with pichu-list and x-list
# if there was no pichu at that location, and if there was a '.', I tried to check whether another pichu can see(attack) current pichu
# if there was no attack, add pichu to that location.
# def successors(house_map, pichu_loc, x_loc):
#     successor_list = []
#     for r in range(0, len(house_map)):
#         for c in range(0,len(house_map[0])):
#              if (r,c) not in pichu_loc:
#                 if (house_map[r][c] == '.'):
#                     if (checkAttack(r, c, pichu_loc, x_loc)):
#                         continue
#                     else:
#                         successor_list.append(add_pichu(house_map, r, c))
#                         pichu_loc.append((r,c))
#     return successor_list
#-----------------------------------------------------------------------------

def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]






# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    visited = [initial_house_map]

    #-------------code for initial approach- status: FAILED -------------------------------
    #store location of all walls on map
    # x_loc= [ (r, c) for r in range(0, len(initial_house_map)) for c in range(0,len(initial_house_map[0])) if initial_house_map[r][c] == 'X' ]
    # print(x_loc)

    # store initial pichu location and all walls on initial housemap
    # found_pichu = False
    # x_loc = []
    # for r in range(0, len(initial_house_map)):
    #     for c in range(0,len(initial_house_map[0])):
    #         if ((found_pichu == False) and (initial_house_map[r][c] == 'p')):
    #             pichu_loc= [(r,c)]
    #             found_pichu == True
    #         if (initial_house_map[r][c] == 'X'):
    #             x_loc.append((r,c))
    # print("initial pichu: ", pichu_loc)
    # print("wallls: ", x_loc)
    #------------------------------------------------------------------------------


    while len(fringe) > 0:

        #-------------code for initial approach- status: FAILED -------------------------------
        # current_map= fringe.pop()
        # for r in range(0, len(current_map)):
        #     for c in range(0,len(current_map[0])):
        #         if (current_map[r][c] == 'p' and ((r,c) not in pichu_loc)):
        #             pichu_loc.append((r,c))
        
        # for new_house_map in successors(current_map, pichu_loc, x_loc):
        #     if is_goal(new_house_map,k):
        #         return (new_house_map, True)
        #     elif new_house_map not in visited:
        #         fringe.append(new_house_map)
        #         visited.append(new_house_map)
        #------------------------------------------------------------------------------
        
        # pichu_count = 0
        # current_map= fringe.pop()

        # for r in range(0, len(current_map)):
        #     for c in range(0,len(current_map[0])):
        #         if current_map[r][c] == 'p':
        #             pichu_count += 1
        # print("pichu placed: ", pichu_count )

        
        # for row in current_map:
        #     print(*row)
        # print("")


        for new_house_map in successors( fringe.pop()):
            if new_house_map is not None:   # nonetype object not iterable
                if is_goal(new_house_map,k):
                    return(new_house_map, True)               
                elif new_house_map not in visited: # if no goal then it takes lot of computational time by revisiting the same state again
                    fringe.append(new_house_map)
                    visited.append(new_house_map)
    return ("", False)
   

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k) # goal not found, nothing is return, nonetype is not iterable, so removed indexing of solution
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


