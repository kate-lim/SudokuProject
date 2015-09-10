from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'Home/', views.sudoku_home, name="home"),
]
