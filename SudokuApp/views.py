from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
import json
import socket


def sudoku_home(request):
    puzzle = [[0 for r in range(9)] for c in range(9)]
    return render(request, 'SudokuHome.html', {'puzzle':puzzle})

def get_numbers(request):
    response_dict = {}
    addr = socket.getaddrinfo('localhost', 8000)
    response_dict.update({'server_response': addr})
    original = request.POST.getlist('inputNumbers[]')

    puzzle = setup_numbers(original)
    solve(puzzle)
    success = True

    print(puzzle)

    returnPuzzle = [0 for r in range(81)]
    for row in range(9):
        for col in range(9):
            print(puzzle[row][col])
            if type(puzzle[row][col]) != type(1):
                puzzle[row][col] = ""
                success = False
                print('why')
            index = int( str(row) + str(col)) - row
            returnPuzzle[index] = puzzle[row][col]

    print(returnPuzzle)

    response_dict.update({'solved_puzzle': returnPuzzle})
    response_dict.update({'success': success})

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

def setup_numbers(original):
    puzzle = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for r in range(9)] for c in range(9)]

    for row in range(9):
        for col in range(9):
            if original[0] != "" and original[0] != '' and original[0] != 0:
                puzzle[row][col] = int(original.pop(0))
            else:
                original.pop(0)


    return puzzle

def solve(puzzle):
    # need to come up with a better way of applying the functions
    for x in range(10):
        eliminate( puzzle )
        eliminateSquare(puzzle )
        sameTwoRow(puzzle)
        sameTwoCol(puzzle)
        onlyOne(puzzle)
    return puzzle


def eliminate(puzzle):
    for r in range(9):
        for c in range(9):
            # check if the cell is not a single number
            if type(puzzle[r][c]) != type(1):
                # remove a number that appears in its row and col from the iist
                for k in range(9):
                    try:
                        puzzle[r][c].remove(puzzle[r][k])
                    except ValueError:
                        pass
                    try:
                        puzzle[r][c].remove(puzzle[k][c])
                    except ValueError:
                        pass
                # if the cell is a single number, make that an int from a list of 1 element
                if len(puzzle[r][c]) == 1:
                    puzzle[r][c] = puzzle[r][c].pop()
    return 

# helper function for eliminateSquare()
def square(puzzle, r, Rowcount, Colcount):
    for c in range(Colcount, Colcount+3):
        if type(puzzle[r][c]) != type(1):
            for k in range(Rowcount, Rowcount+3):
                for m in range(Colcount, Colcount+3):
                    try: puzzle[r][c].remove(puzzle[k][m])
                    except: pass
            if len(puzzle[r][c]) == 1:
                puzzle[r][c] = int(puzzle[r][c].pop())
    return

#for every empty cell, eliminate numbers that overlap within its square
def eliminateSquare(puzzle):
    for r in range(0, 3):
        square(puzzle, r, 0, 0)
        square(puzzle, r, 0, 3)
        square(puzzle, r, 0, 6)
    for r in range(3, 6):
        square(puzzle, r, 3, 0)
        square(puzzle, r, 3, 3)
        square(puzzle, r, 3, 6)
    for r in range(6, 9):
        square(puzzle, r, 6, 0)
        square(puzzle, r, 6, 3)
        square(puzzle, r, 6, 6)
    return

#sameTwoRow returns indecies of all length 2 cells in a row
def indexTwoRow(puzzle, r):
    index = []
    for c in range(len(puzzle)):
        if type(puzzle[r][c]) != type(1) and len(puzzle[r][c]) == 2:
            index.append(c)
    return index

def sameTwoRow(puzzle):
    for r in range(len(puzzle)):
        index = indexTwoRow(puzzle, r)
        #i is a list of indicies of length 2 cells
        for i in index:
            for j in index:
                #search if any two cells have the same numbers
                if i != j and puzzle[r][i] == puzzle[r][j]:
                    #i : index of the first of the two same cells
                    #j : index of the second of the two same cells
                    #iterate through the rest empty cells in the row
                    #c is a temp var to iterate through each column in the row
                    for c in range(9):
                        if type(puzzle[r][c]) != type(1) and c != i and c != j:
                            try: 
                                puzzle[r][c].remove(puzzle[r][i][0])
                            except ValueError: 
                                try: 
                                    puzzle[r][c].remove(puzzle[r][i][1])
                                except ValueError: 
                                    pass

                            if len(puzzle[r][c]) == 1:
                                puzzle[r][c] = int(puzzle[r][c].pop())
                        
    return

#sameTwoCol returns indecies of all length 2 cells in a column
def indexTwoCol(puzzle, c):
    index = []
    for r in range(len(puzzle)):
        if type(puzzle[r][c]) != type(1) and len(puzzle[r][c]) == 2:
            index.append(r)
    return index

def sameTwoCol(puzzle):
    for c in range(len(puzzle)):
        #index is a list of indicies of length 2 cells
        index = indexTwoCol(puzzle, c)
        
        #search if any two cells have the same numbers
        #i : index of the first of the two same cells
        #j : index of the second of the two same cells
        for i in index:
            for j in index:
                if i != j and puzzle[i][c] == puzzle[j][c]:
                    #iterate through the rest empty cells in the column
                    #r is a temp var to iterate through each row in the column
                    for r in range(9):
                        if type(puzzle[r][c]) != type(1) and r != i and r != j:
                            try: 
                                puzzle[r][c].remove(puzzle[i][c][0])
                            except ValueError: 
                                try: 
                                    puzzle[r][c].remove(puzzle[i][c][1])
                                except ValueError: 
                                    pass

                            if len(puzzle[r][c]) == 1:
                                puzzle[r][c] = int(puzzle[r][c].pop())
                        
    return

# helper function for onlyOne
def check(puzzle, n):
    count = 0
    for c in range(9):
        if type(puzzle[c]) != type(1):
            for j in range(len(puzzle[c])):
                if puzzle[c][j] == n:
                    col = c
                    index = j
                    count = count+1
    if count == 1:
        return (True, col, index)
    else:
        return (False, 0, 0)

# when there is only one possible number in a row or a column
# for example, 4 empty cells in a row and possible values are [3,5,8], [3,8,9], [5,8], [3,8]
# you know the value of the second cell is 9
def onlyOne(puzzle):
    for r in range(9):
        temp = [1,2,3,4,5,6,7,8,9]

        #get rid of fixed numbers from temp
        for c in range(9):
            if type(puzzle[r][c]) == type(1):
                temp.remove(puzzle[r][c])

        #get the information of the number that only appears once in the row/col
        for i in range(len(temp)):
            b,col,index = check(puzzle[r], temp[i])
            if b:
                puzzle[r][col] = int(puzzle[r][col].pop(index))
    return
