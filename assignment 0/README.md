# a0

# Part 1: Navigation	

1] Set of valid states:
Set of all states with pichu is located on the house map

2] Initial state:
Initial state for given problem is house map with pichu’s starting position 

3] Successor function
Takes a house map and pichu’s current location as input and returns a set of valid successors where a pichu moves by 1 unit in top, bottom, left or right direction

4] Heuristic function:
Heuristic function tells us how promising a state is to reach the goal state. Here, we have used Manhattan Distance to calculate the likelihood of reaching the goal state.
Thus, h(s) = abs(x2-x1) + abs(y2-y1), where (x1, y1) is pichu’s current location and (x2, y2) is goal state.

5] Cost function:
Cost function calculates that cost of reaching goal states from initial state through pichu’s current location.
Here, we have implemented A* algorithm which considers the cost of reaching current state from initial state (g(s)) and cost of reaching goal state from current state (h(s)).
Thus, we get cost function f(s) = g(s) + h(s), where h(s) is an admissible heuristic function.

6] Goal State
State where pichu reaches the goal location “@”

Some Implications:
Why did program go in infinite loop?
Ans: The default skeleton given wasn’t keeping track of visited nodes. Hence, the program kept visiting already visited and never reached the goal state.

Improvements:
In the default skeleton, fringe.pop() operation was being perfomed, which was always expanding the last node entered in the fringe. i.e. given program was using DFS instead of BFS

I modified the code and used fringe.pop(0) to expand the node which was inserted first. Moreover, I implemented A* algorithm using priority queue to pop the element which had highest priority. Priority was calculated using cost function mentioned above

Finding Path from start to goal:
I implemented backtracking my maintaining a dictionary which stored elements in form - (previous, current) which indicates that current state was reached from previous state, for all states(moves).

Once goal state was reached, I backtracked the dictionary starting from goal state till I reached the start state and calculated all the moves (L, R, U, D) made along that path and stored it in reverse order to get a list of moves from starting state to goal state.

Approach 1: Part 1 – Failed 

Initially I tried fringe as dictionary where priority was "key" and (current move, current distance) was "value". However, when two moves had same priority, first move was overwritten by second, since key in dictionary should be unique. Thus, we were never reaching a goal state even when path existed from start to goal

Approach 1: Part 2 – Successful 

This time implementing fringe as dictionary with key as different moves and value as their priority. This solves the overwriting issue when two moves have same priority. 
After that for any current iteration I popped that element from fringe where value of that element in fringe is minimum (~ lowest number - highest priority). Thus, goal node was reached SUCCESSFULLY if a path existed

Approach 2: Successful

In this approach I implemented fringe as list of nested tuples of the form -  ((pichu_loaction, current distance), priority)

Pichu_loaction = current location of pichu on house map
Current distance = cost of reaching current location from start state
Priority = cost function mentioned above. (g(s) + h(s))

After than I sorted the list based on priority and popped front element. Sort function defined above is referred from https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item. Goal node was reached successfully if a path existed



 
# Part 2 – Hide and Seek


1] Set of valid states: 
Set of all states (house map) where a nth pichu is placed on the house map which already has n-1 pichu placed in such a way that no pichu can see one another

2] Initial state:
Initial state is the initial house map with first pichu placed on the house map.

3] Successor function
For given problem of placing k number of pichus, (for n = 2 to k) successor function takes a house map where n-1 pichus are already placed and places nth pichu on housemap such that no pichu can see other pichus and returns the housemap 

4] Cost Function
Cost function will increase by 1 for placing each pichu on house map, thus cost of reaching any valid state from previous state is 1.

5] Goal State:

State where all n pichus are placed on the house map such that no pichu can see other pichus.


Logic for placing pichu:

For each location in house map, if that location is a ‘.’, check  whether other pichus see the current pichu, if current pichu is placed on that location, 

1] Place a pichu at current location if it is not in same row, column and diagonal as already placed pichu.

2] Place a pichu at current location, when current pichu is in same row, column or diagonal but there is a ‘x’ between them.


Working

1] Initial Approach Approach 
For initial approach I was traversing all rows, columns diagonals and ‘location of all X’ to check if previously placed pichus can see current pichu. Here I placed all the conditions to check rows, columns and diagonals in same iteration while traversing the house map. I maintained a pichu-list and X-List to compare against location of current pichu. Unfortunately, the code didn't work.

2] Approach 2

Part: 1
Initially, I have broken down conditions for same row and same column w.r.t current row, curret column in two different loops for loops. Before implementing diagonal-condition, I tried checking if my logic work for checking rows and columns. Unfortunately, it didn't work for pichu greater than 4, it was placing two pichu in same column. 

Modified Approach:
Here instead checking entire row or entire col in one iteration, I divided these conditions in different parts, such as checking row towards left of current row col in one condition, check row towards right of current row col in another condition and so on.  I studied n queens problem from "geeks for geeks" to understand how queens where placed. link: https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/. 
For n queens, n-1 queens were already placed in columns 0 to n-1. Thus, they were only checking left side of the board for current location (row, col) ie: check left row, left upper diagonal, left bottom diagonal. However, for the given pichu problem, we can place two pichu in any direction if they are not in same row, col or diagonal. Additionly, even if two pichus are in same row, col or diagonal, we need to check if they can see each other or not. So for current (row,col) check all directions to see if we get a pichu first or 'X' first. 

For all 8 direction, if pichu is seen first then we can't place the current pichu at loaction (row,col).
Else if 'X' is seen first, it means that no other pichu can see the current pichu at (row,col) since there will be a 'X' between them.

First, I tired to combine the conditions for checking diagonal with top and bottom direction together and checked left, right directions in two seperate for loops. However, when I tested the code using pytest, the code failed the test- "test_question2_case2". I checked and realized that for map2, if pichu no. is greater than 6, it was placing two pichu in same diagonal who can see each other.

. p . . X X X  
. X . X p . .    <===== notice pichu here  
. X . . X . .         and  
. X p X p . .    <===== 'first' pichu here. Both are in same diagonal and can see each other  
. X . X . X p  
p X . p . X @  


Part 2 – Final Approach
Here, to solve the problem of having two pichu in same diagonal who can see each other for map2, when pichu no. greater 6, I kept conditions for checking left, right, top, bottom, top-left-diagonal, top-right-diagonal, bottom-left-diagonal, bottom-right-diagonal in different blocks (using loop for different range).
Idea to use 'zip' function for checking diagonal was referred from n-queens problem of "geeks for geeks". Link: https://www.geeksforgeeks.org/python-program-for-n-queen-problem-backtracking-3/. 







