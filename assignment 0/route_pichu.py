#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Shubham Bhagat , snbhagat
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def getPriority(x1, y1, x2, y2, curr_dist):
        gS = curr_dist
        hS = abs(x2-x1) + abs(y2-y1)
        return gS + hS

def findPath(prev, start, goal):
        current = goal
        move_string = ""
        # pathList = [current]
        while current != start:
                previous = prev[current]
                if (current[0]>previous[0] and current[1]==previous[1]):
                        move_string += "D"
                elif (current[0]<previous[0] and current[1]==previous[1]):
                        move_string += "U"
                elif (current[0]==previous[0] and current[1]>previous[1]):
                        move_string += "R"
                elif (current[0]==previous[0] and current[1]<previous[1]):
                        move_string += "L"
                current = prev[current]
        #       pathList.insert(0, current)
        # print("\nPath from source to destination")
        # print(pathList)
        # print("Number of moves: ",len(move_string),"\nActual moves: ",move_string[::-1])
        return (len(move_string), move_string[::-1])


# In fringe every elemnent is tuple where first element is again a tuple of curent_move and current_distnace and second element is the priority
# the below code sorts the pringe based on priority 
# This code is referred from : https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
def sortFringe(fringe):
        fringe.sort(key = lambda x: x[1])
        return fringe
# end of referred code

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        
        #Find goal position
        goal_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        
        # fringe as dictionary with priority as key
        # fringe = {getPriority(*pichu_loc, *goal_loc,0 ):(pichu_loc,0)} 

        # fringe as dictionary with priority as value
        # fringe = {(pichu_loc,0): getPriority(*pichu_loc, *goal_loc,0 )}
            
        # fringe as list of nested tuple
        fringe=[((pichu_loc,0), getPriority(*pichu_loc, *goal_loc,0 ))]
        
        # list of visited states
        visited = [pichu_loc]
        
        # dictionary which stores parent-successor correspondence for each node. Used to trace back the path from start to goal
        prev = {}



        
        # Initially I tried fringe as dictionary where priority was "key" and (current move, current distance) was "value"
        # However, when two moves had same priority, first move was overwritten by second, since key in dictionary should be unique.
        # Thus, we were never reaching a goal state even when path existed from start to goal
        # while fringe:
        #         minDist = min(fringe.keys())
        #         print(fringe)
        #         print("element popped is :")
        #         popped = (curr_move, curr_dist)=fringe.pop(minDist)
        #         visited.append(curr_move)
        #         print(popped,"\n")
        #         print("visited: ", visited)
        #         print("succ: ",moves(house_map, *curr_move) )
        #         for move in moves(house_map, *curr_move):
        #                 if house_map[move[0]][move[1]]=="@":
        #                         prev[move]=curr_move
        #                         return findPath(prev, pichu_loc,goal_loc)
        #                 elif move not in visited:   
        #                         #fringe.append((move, curr_dist + 1))
        #                         fringe.update({manDistance(*move, *goal_loc, curr_dist+1):(move, curr_dist+1)})
        #                         prev[move] = curr_move
        # return -1         
        
        
        
        
        
        # This time implementing fringe as dictionary with key as different moves and value as their priority.
        # This solves the overwriting issue when two moves have same priority.
        # Goal node was reached SUCCESSFULLY if a path existed 
        # while fringe:
        #         print("fringe: ",fringe)
        #         minVal = min(fringe.values())
        #         for k in fringe.keys():
        #                 if fringe[k] == minVal:
        #                         priority = (fringe.pop(k))
        #                         (curr_move,current_Dist) = k
        #                         break
        #         print("element popped: ",curr_move)
        #         print("succ: ",moves(house_map, *curr_move))
        #         print("visited: ",visited,"\n")
        #         for move in moves(house_map, *curr_move):
        #                 if house_map[move[0]][move[1]] == "@":
        #                         prev[move]=curr_move
        #                         return findPath(prev, pichu_loc,goal_loc)
        #                 elif move not in visited:
        #                         fringe[move,current_Dist+1] = getPriority(*move, *goal_loc, current_Dist+1)
        #                         visited.append(move)
        #                         prev[move]=curr_move
        # return (-1,"")

        
        #implementing fringe as list of nested tuples. Sort list based on priority and pop front element
        #sort function defined above is referred from https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
        # Goal node was reached SUCCESSFULLY if a path existed 
        while fringe:
                fringe = sortFringe(fringe)
                (curr_move, curr_dist)=fringe.pop(0)[0]
                for move in moves(house_map, *curr_move):
                        if house_map[move[0]][move[1]] == "@":
                                prev[move]=curr_move
                                return findPath(prev, pichu_loc,goal_loc)
                        elif move not in visited:
                                fringe.append(((move, curr_dist+1), getPriority(*move, *goal_loc, curr_dist+1)))
                                visited.append(move)
                                prev[move]=curr_move
        return (-1,"")

                                


# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])


