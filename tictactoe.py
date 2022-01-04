#! /usr/bin/python3
from time import sleep
import random

#function to print board
def printboard(board):
     for i in range(len(board)) : 
         for j in range(len(board[i])) : 
            if(board[i][j]==-1):
               print("-",end=" " )
            else:
                print(board[i][j],end=" " )
         print()   

#function to check if board is full
def isfull(board):
    check=True
    for i in range(len(board)) : 
         for j in range(len(board[i])) : 
             if(board[i][j]==-1):
                 check=False
                 break
    return check

#function to check if player has won
def checkwinplayer(board,plchar):
    for i in range(len(board)) :
        if(board[i][0]==plchar and board[i][1]==plchar and board[i][2]==plchar):
             return True
    for j in range(len(board)) : 
        if(board[0][j]==plchar and board[1][j]==plchar and board[2][j]==plchar):
             return True
    if(board[0][0]==plchar and board[1][1]==plchar and board[2][2]==plchar):
        return True
    elif(board[2][0]==plchar and board[1][1]==plchar and board[0][2]==plchar):
        return True
    else: return False

#function to check if computer has won
def checkwincomputer(board,compchar):
    for i in range(len(board)) :
        if(board[i][0]==compchar and board[i][1]==compchar and board[i][2]==compchar):
             return True
    for j in range(len(board)) : 
        if(board[0][j]==compchar and board[1][j]==compchar and board[2][j]==compchar):
             return True
    if(board[0][0]==compchar and board[1][1]==compchar and board[2][2]==compchar):
        return True
    elif(board[2][0]==compchar and board[1][1]==compchar and board[0][2]==compchar):
        return True
    else: return False

#function to check if it is a tie
def checktie(board,plchar,compchar):
    return isfull(board) and checkwinplayer(board,plchar)==False and checkwincomputer(board,compchar)==False

#function to check optimum move based on minimax search
def minimaxheuristic(board,depth,maximizeplayer,selections,plchar,compchar):
    #check if winner 
    if(checkwincomputer(board,compchar)):
        return 1
    if(checkwinplayer(board,plchar)):
        return -1
    if(checktie(board,plchar,compchar)):
        return 0
    if(maximizeplayer):
        bestscore= -200
        #check the initial value of best play
        bestplay=0
        for locn in range(len(selections)):
            loc= selections[locn]
            j=loc%3
            i=int((loc-j)/3)
            del selections[locn]
            board[i][j]=compchar
            score= minimaxheuristic(board,depth+1,False,selections,plchar,compchar)
            if(score>bestscore):
                bestscore=score
                bestplay=loc
            selections.insert(locn,loc)
            board[i][j]=-1
        return bestscore
    else:
        bestscore= 200
        #check the initial value of best play
        bestplay=0
        for locn in range(len(selections)):
            loc= selections[locn]
            j=loc%3
            i=int((loc-j)/3)
            del selections[locn]
            board[i][j]=plchar
            score=minimaxheuristic(board,depth+1,True,selections,plchar,compchar)
            if(score<bestscore):
                bestscore=score
                bestplay=loc
            selections.insert(locn,loc)
            board[i][j]=-1
        return bestscore

#function to decide best move for computer on the basis of minimax
def computermove(board,selections,plchar,compchar):
    bestscore= -200
    #check the initial value of best play
    bestplay=0
    for locn in range(len(selections)):
        loc= selections[locn]
        j=loc%3
        i=int((loc-j)/3)
        del selections[locn]
        board[i][j]=compchar
        score= minimaxheuristic(board,0,False,selections,plchar,compchar)
        if(score>bestscore):
            bestscore=score
            bestplay=loc
        selections.insert(locn,loc)
        board[i][j]=-1
    return bestplay

print("Choose the character you want to play with i.e. X or O")
choice=input("Do you want to play with X ?(Y/N) ")
if(choice=="Y" or choice=="y"):
    print("You will play with X and computer will play with O ! ")
    plchar='X'
    compchar='O'
else:
    print("You will play with O and computer will play with X ! ")
    plchar='O'
    compchar='X'
firstplayerturn=True
r=random.randint(1,10)
if(r>=6):
    firstplayerturn=True
else:
    firstplayerturn=False
while(1):
    selections=[0,1,2,3,4,5,6,7,8]
    board=[[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
    if(firstplayerturn==False):
        playerturn=True
        firstplayerturn=True
        print("You are chosen to play first! ")
    else:
        print("The computer is chosen to play first! ")
        firstplayerturn=False
        playerturn=False
    while(isfull(board) == False):
        
        #player's turn
        if(playerturn):    
            print("Your Turn!! ")
            rstr=input("Enter the row of the cell where you want to place the %s : " %(plchar))
            cstr=input("Enter the column of the cell where you want to place the %s : " %(plchar))
            if(rstr.isnumeric()==False or cstr.isnumeric()==False):
                print("Please enter a numeric value .Please try again")
                continue
            r=int(rstr)
            c=int(cstr)
            if(r<1 or r>3 or c<1 or c>3):
                print("Please enter a value existing in the grid i.e. r=1,2,3 and c=1,2,3 .Please try again")
                continue
            if(board[r-1][c-1]!=-1):
                print("Oops! It appears the cell is already populated.Please try again")
                continue
            else: 
                board[r-1][c-1]=plchar
                selections.remove(3*(r-1)+c-1)
            print("Current status of board:")
            printboard(board)
            checkerpl=checkwinplayer(board,plchar)
            if(checkerpl==True):
                print("Congratulations!!! You won")
                break
            playerturn=False
        
        #computer's turn
        else:
            print("Computer's turn!")
            sleep(0.5)
            # here the selection by computer begins
            bestposn=computermove(board,selections,plchar,compchar)
            loc=int(bestposn)
            j=loc%3
            i=int((loc-j)/3) 
            #the location has been selected
            print("I place %s at row number %d and column number %d " %(compchar,i+1,j+1) )
            board[i][j]=compchar
            print("Current status of board:")
            printboard(board)
            #delete from selections
            selections.remove(loc)
            checkercomp=checkwincomputer(board,compchar)
            if(checkercomp==True):
                print("Sorry you lost! Better luck next time")
                break
            playerturn=True
    if(checktie(board,plchar,compchar)):
        print("It is a tie!!")
    toplay="N"
    toplay=input("Would you like to play another round?(Y/N): " )
    if(toplay=="Y" or toplay=="y"):
        continue
    else :
        break
    


    


