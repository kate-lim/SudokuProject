from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.sudoku_home, name='home'),
	url(r'^SudokuSolved$', views.get_numbers)
]