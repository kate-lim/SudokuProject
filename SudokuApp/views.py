from django.shortcuts import render

def sudoku_home(request):
    return render(request, 'SudokuHome.html')
