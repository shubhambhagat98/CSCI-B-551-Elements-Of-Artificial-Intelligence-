#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import copy
import math

from numpy import pi

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def string_to_board(board,N):
    boardList = []
    for i in range(0,len(board),N):
        boardList.append([ char for char in board[i:i+N]])
    # for row in boardList:
    #     print(*row)
    return boardList

def pichu_count(board, pichu, row, col):
    top_right = 0
    top_left = 0
    bottom_right = 0
    bottom_left =0
    
    if pichu == 'b':
        jump_flag = False
        count = 0
        for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)):
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                top_left += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                top_left +=2
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break

        jump_flag = False
        count = 0
        for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))):
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                top_right += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                top_right +=2
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break

        return top_left + top_right

            
    if pichu =='w':
        jump_flag = False
        count = 0
        for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)):
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                bottom_left += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                bottom_left +=2
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break
            
        jump_flag = False
        count = 0
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))):
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                bottom_right += 1
                break
            elif (board[i][j] == '.' and jump_flag == True):
                bottom_right +=2
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break
        
        return  bottom_left + bottom_right          
                

def pikachu_count(board, pikachu, row, col):
    top = 0
    bottom = 0
    left = 0
    right = 0

    jump_flag = False
    count = 0

    if pikachu == 'B':
        jump_flag = False
        count = 0
        
        for i in range(row-1,-1,-1):
            k= i
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and (top ==2 or count ==3)):
                break

            if (jump_flag == True and top ==0 and count ==2):
                break

            if (board[i][col] == '.' and jump_flag == False):
                top +=1
                count +=1
            elif (board[i][col] == '.' and jump_flag == True):
                top += 2
                count +=1
            elif (board[i][col] in 'wW'):
                if jump_flag == False: 
                    jump_flag == True
                count += 1
            elif (board[i][col] in 'B@$'):
                break
       

    if pikachu == 'W':
        jump_flag = False
        count = 0
        for i in range(row+1,len(board)):
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and (bottom ==2 or count ==3)):
                break
            if (jump_flag == True and (top ==2 or count ==3)):
                break
            

            if (board[i][col] == '.' and jump_flag == False):
                bottom +=1
                count +=1
            elif (board[i][col] == '.' and jump_flag == True):
                bottom += 2
                count +=1
            elif (board[i][col] in 'bB'):
                if jump_flag == False: 
                    jump_flag == True
                count += 1
            elif (board[i][col] in 'W@$'):
                break
    

    jump_flag = False
    count = 0
    for i in range(col-1,-1,-1):
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and (left ==2 or count ==3)):
            break
        if (jump_flag == True and (top ==2 or count ==3)):
                break

        if (board[row][i] == '.' and jump_flag == False):
            left +=1
            count +=1
        elif (board[row][i] == '.' and jump_flag == True):
            left += 2
            count +=1
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag == True
            count += 1
        elif (pikachu =='W' and board[i][col] in 'W@$') or (pikachu =='B' and board[i][col] in 'B@$'):
                break

    jump_flag = False
    count = 0
    for i in range(col+1,len(board[0])):
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and (right ==2 or count ==3)):
            break
        if (jump_flag == True and (top ==2 or count ==3)):
                break

        if (board[row][i] == '.' and jump_flag == False):
            right +=1
            count +=1
        elif (board[row][i] == '.' and jump_flag == True):
            right += 2
            count +=1
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag == True
            count += 1
        elif (pikachu =='W' and board[i][col] in 'W@$') or (pikachu =='B' and board[i][col] in 'B@$'):
                break
    
    if pikachu == 'B':
        return top + left + right
    elif pikachu == 'W':
        return bottom +left + right

def raichu_count(board, raichu, row, col):
    top = bottom = left = right = top_left = top_right = bottom_left = bottom_right = 0

    jump_flag = False
    jump_count = 0
    for i in range(row-1,-1,-1):
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                top += 1
            elif (jump_flag == True and jump_count == 0):
                top += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                top += 1
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i in range(row+1,len(board)):
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                bottom += 1
            elif (jump_flag == True and jump_count == 0):
                bottom += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                bottom += 1
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    for i in range(col-1,-1,-1):
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                left += 1
            elif (jump_flag == True and jump_count == 0):
                left += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                left += 1
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

        
    jump_flag = False
    jump_count = 0
    for i in range(col+1,len(board[0])):
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                right += 1
            elif (jump_flag == True and jump_count == 0):
                right += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                right += 1
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                top_left += 1
            elif (jump_flag == True and jump_count == 0):
                top_left += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                top_left += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                top_right += 1
            elif (jump_flag == True and jump_count == 0):
                top_right += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                top_right += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                bottom_left += 1
            elif (jump_flag == True and jump_count == 0):
                bottom_left += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                bottom_left += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                bottom_right += 1
            elif (jump_flag == True and jump_count == 0):
                bottom_right += 2
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                bottom_right += 1
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    return top + bottom + left + right + top_left + top_right + bottom_left + bottom_right

def heuristic1(board):
    nw = sum(row.count('w') for row in board)
    nb = sum(row.count('b') for row in board)
    nW = sum(row.count('W') for row in board)
    nB = sum(row.count('B') for row in board)
    nWR = sum(row.count('@') for row in board)
    nBR = sum(row.count('$') for row in board)
    return (2*(nw - nb) + 3*(nW - nB) + 8*(nWR - nBR))


def heuristic2(board):
   
    print("inside h2:")
    print(board)

    wp=0
    wP=0
    bp=0
    bP=0    
    N = len(board)
   
    for i in range(N):
        for j in range(N):

            if board[i][j]=='w':
                wp += math.floor(N/2) - math.ceil((N-i-1)/2) +1
            elif board[i][j]=='b':
                bp += math.floor(N/2) - math.ceil(i/2) +1
            elif board[i][j]=='W':
                wP += math.ceil(N/3) - math.ceil((N-i-1)/3) +1
            elif board[i][j]=='B':
                bP += math.ceil(N/3) - math.ceil(i/3) +1
   
    return (wp+wP-bp-bP)

def heuristic3(board):
    black_count = 0
    white_count = 0

    
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'w':
                white_count += pichu_count(board,board[row][col], row, col)
            elif board[row][col] == 'b':
                black_count += pichu_count(board,board[row][col], row, col)
            elif board[row][col] == 'W':
                white_count += pikachu_count(board,board[row][col], row, col) 
            elif board[row][col] == 'B':
                black_count += pikachu_count(board,board[row][col], row, col)
            elif board[row][col] == '@':
                white_count += raichu_count(board,board[row][col], row, col)
            elif board[row][col] == '$':
                black_count += raichu_count(board,board[row][col], row, col)

    return black_count, white_count
                       

def pichu_succ(board, pichu, row, col):
    newboard = copy.deepcopy(board)
    # pichu_succ_list = []
    
    if pichu == 'b':
        jump_flag = False
        count = 0
        k,m = 1000, 1000
        for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)): #top-left diagonal
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break
        

        jump_flag = False
        count = 0
        k,m = 1000, 1000
        for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))): #top-right diagonal
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                if (k == 0 and newboard[k][m]=='b'):
                    newboard[k][m] = '$'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'w'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'WbB@$'):
                break

        # return pichu_succ_list

            
    if pichu =='w':
        jump_flag = False
        count = 0
        k = 0
        m = 0
        for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)): #bottom-left diagonal
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break
        
            
        jump_flag = False
        count = 0
        k = 0
        m = 0
        for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))): #bottom-right
            k = i
            m = j
            if count == 2:
                break
            if(board[i][j] == '.' and jump_flag == False):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                break
            elif (board[i][j] == '.' and jump_flag == True):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                if (k == len(board)-1 and newboard[k][m]=='w'):
                    newboard[k][m] = '@'
                yield newboard
                # pichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                count +=1
            elif (board[i][j] == 'b'):
                jump_flag = True
                count +=1
            elif (board[i][j] in 'BwW@$'):
                break

        # return  pichu_succ_list        
                

def pikachu_succ(board, pikachu, row, col):
    top = 0
    bottom = 0
    left = 0
    right = 0

    # pikachu_succ_list = []
    newboard = copy.deepcopy(board)

    jump_flag = False
    count = 0

    if pikachu == 'B':
        jump_flag = False
        count = 0
        k = 10000
        for i in range(row-1,-1,-1):
            k=i
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and (top ==2 or count ==3)):
                break

            if (jump_flag == True and top ==0 and count ==2):
                break

            if (board[i][col] == '.' and jump_flag == False):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                if (k==0 and newboard[k][col] == 'B'):
                    newboard[k][col] = '$'
                yield newboard
                # pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                top += 1
                count +=1
            elif (board[i][col] == '.' and jump_flag == True):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                if (k==0 and newboard[k][col] == 'B'):
                    newboard[k][col] = '$'
                yield newboard
                # pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                top += 2
                count +=1
            elif (board[i][col] in 'wW'):
                if jump_flag == False: 
                    jump_flag == True
                count += 1
            elif (board[i][col] in 'B@$'):
                break
        
        

    if pikachu == 'W':
        jump_flag = False
        count = 0
        k=0
        for i in range(row+1,len(board)):
            k=i
            if (jump_flag == False and count==2):
                break
            if (jump_flag == True and (bottom ==2 or count ==3)):
                break
            if (jump_flag == True and (top ==2 or count ==3)):
                break
            

            if (board[i][col] == '.' and jump_flag == False):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                if (k==len(board)-1 and newboard[k][col] == 'W'):
                    newboard[k][col] = '@'
                yield newboard
                # pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                bottom +=1
                count +=1
            elif (board[i][col] == '.' and jump_flag == True):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                if (k==len(board)-1 and newboard[k][col] == 'W'):
                    newboard[k][col] = '@'
                yield newboard
                # pikachu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                bottom += 2
                count +=1
            elif (board[i][col] in 'bB'):
                if jump_flag == False: 
                    jump_flag == True
                count += 1
            elif (board[i][col] in 'W@$'):
                break
        
    

    jump_flag = False
    count = 0
    for i in range(col-1,-1,-1):
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and (left ==2 or count ==3)):
            break
        if (jump_flag == True and (top ==2 or count ==3)):
                break

        if (board[row][i] == '.' and jump_flag == False):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[row][i+1] = '.'
            yield newboard
            # pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            left +=1
            count +=1
        elif (board[row][i] == '.' and jump_flag == True):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[row][i+1] = '.'
            yield newboard
            # pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            left += 2
            count +=1
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag == True
            count += 1
        elif (pikachu =='W' and board[i][col] in 'W@$') or (pikachu =='B' and board[i][col] in 'B@$'):
                break

    jump_flag = False
    count = 0
    for i in range(col+1,len(board[0])):
        if (jump_flag == False and count==2):
                break
        if (jump_flag == True and (right ==2 or count ==3)):
            break
        if (jump_flag == True and (top ==2 or count ==3)):
                break

        if (board[row][i] == '.' and jump_flag == False):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[row][i-1] = '.'
            yield newboard
            # pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            right +=1
            count +=1
        elif (board[row][i] == '.' and jump_flag == True):
            newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
            newboard[row][i-1] = '.'
            yield newboard
            # pikachu_succ_list.append(newboard)
            newboard = copy.deepcopy(board)
            right += 2
            count +=1
        elif (pikachu =='W' and board[row][i] in 'bB') or (pikachu =='B' and board[row][i] in 'wW') :
            if jump_flag == False: 
                jump_flag == True
            count += 1
        elif (pikachu =='W' and board[i][col] in 'W@$') or (pikachu =='B' and board[i][col] in 'B@$'):
                break
    
    # return pikachu_succ_list
            

def raichu_succ(board, raichu, row, col):
    
    # raichu_succ_list = []
    newboard = copy.deepcopy(board)

    jump_flag = False
    jump_count = 0
    for i in range(row-1,-1,-1):
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i+1][col] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i in range(row+1,len(board)):
        if (board[i][col] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][col], newboard[row][col] = newboard[row][col], newboard[i][col]
                newboard[i-1][col] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][col] in 'bB$') or (raichu == '$' and board[i][col] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    for i in range(col-1,-1,-1):
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

        
    jump_flag = False
    jump_count = 0
    for i in range(col+1,len(board[0])):
        if (board[row][i] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
            elif (jump_flag == True and jump_count == 0):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[row][i], newboard[row][col] = newboard[row][col], newboard[row][i]
                newboard[row][i-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board) 
        elif (raichu == '@' and board[row][i] in 'bB$') or (raichu == '$' and board[row][i] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break
    
    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row-1, -1, -1),range(col-1, -1, -1)):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row-1, -1, -1),range(col+1,len(board[0]))):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i+1][j-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row+1,len(board)),range(col-1, -1, -1)):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j+1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    jump_flag = False
    jump_count = 0
    for i,j in zip(range(row+1,len(board)),range(col+1,len(board[0]))):
        if (board[i][j] == '.'):
            if (jump_flag == False and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
            elif (jump_flag == True and jump_count == 0):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
                jump_count = 1
            elif (jump_flag == True and jump_count == 1):
                newboard[i][j], newboard[row][col] = newboard[row][col], newboard[i][j] 
                newboard[i-1][j-1] = '.'
                yield newboard
                # raichu_succ_list.append(newboard)
                newboard = copy.deepcopy(board)
        elif (raichu == '@' and board[i][j] in 'bB$') or (raichu == '$' and board[i][j] in 'wW@'):
            if (jump_flag == False):
                jump_flag == True
                continue
            elif (jump_flag == True):
                break
        elif ((raichu == '@' and board[i][col] in '@wW') or (raichu == '$' and board[i][col] in '$bB')):
            break

    # return raichu_succ_list


def succ(board, player):
    
    
    if player == 'w':
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 'w' :
                    yield pichu_succ(board,board[row][col], row, col)
                elif board[row][col] == 'W':
                    yield pikachu_succ(board,board[row][col], row, col)
                elif board[row][col] == '@':
                    yield raichu_succ(board,board[row][col], row, col)

    elif player == 'b':
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 'b' :
                    yield pichu_succ(board,board[row][col], row, col)
                elif board[row][col] == 'B':
                    yield pikachu_succ(board,board[row][col], row, col)
                elif board[row][col] == '$':
                    yield raichu_succ(board,board[row][col], row, col)

    # return all_successor
            


def es(board):
    
    
    h3_black, h3_white = heuristic3(board)
    return heuristic1(board) + heuristic2(board) - h3_black + h3_white
    # return heuristic1(board) + heuristic2(board) 


def minimaxpruning(board,player,height):

        hcount = 0
        evalues = []
        alpha = -(10^5)
        beta = 10^5
        if player =='w':
            # print("=========================== w successor ====================")
            for i in succ(board, 'w'):
                hcount=0
                evalues.append(min_val(i,alpha,beta,hcount, height))
                # for row in i:
                #     print(*row)
                # print(evalues[-1])
            return succ(board, player)[evalues.index(max(evalues))]
        elif player =='b':
            # print("=========================== b successor ====================")
            for i in succ(board, 'b'):
                hcount=0
                evalues.append(max_val(i,alpha,beta,hcount, height))
                # for row in i:
                #     print(*row)
                # print(evalues[-1])
            return succ(board, player)[evalues.index(min(evalues))]


def min_val(suc,alpha,beta,hcount, height):
        if hcount==height:
            return es(suc)
        else:
            # for row in suc:
            #     print(*row)
            # print("")
            # for i in succ(suc, 'b'):
            #     beta = min(beta,max_val(i,alpha,beta,hcount+1, height))
            #     if alpha>=beta:
            #         return beta
            # return beta

            current_succ = 0
            while True:
                current_succ = succ(suc, 'b')
                if current_succ != None:
                    beta = min(beta,max_val(current_succ,alpha,beta,hcount+1, height))
                    if alpha >= beta:
                        break
                else:
                    break
            return beta


def max_val(suc,alpha,beta,hcount, height):
        if hcount==height:
            return es(suc)
        else:
            # for row in suc:
            #     print(*row)
            # print("")
            # for i in succ(suc, 'w'):
            #     alpha = max(alpha,min_val(i,alpha,beta,hcount+1, height))
            #     if alpha>=beta:
            #         return alpha
            # return alpha
            current_succ = 0
            while True:
                current_succ = succ(suc, 'b')
                if current_succ != None:
                    alpha = max(alpha,min_val(current_succ,alpha,beta,hcount+1, height))
                    if alpha >= beta:
                        break
                else:
                    break
            return alpha


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #

    # while timelimit:
    #     time.sleep(1)
    #     yield minimaxpruning(board,player)
    #     timelimit -= 1

    height = 3
    while True:
        print("solution for height: ", height)
        yield(minimaxpruning(board,player,height))
        height += 1

     


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    newboard = string_to_board(board,N)

    for board in find_best_move(newboard, N, player, timelimit):
        for row in board:
            print(*row)
        print("")
    #  print(board) # actual output

    # string_to_board(board, N)


    # demoSucc = string_to_board(board,N)

    # list_of_succ = succ(demoSucc, player)
    # for board in list_of_succ:
    #     for row in board:
    #         print(*row)
    #     print("")