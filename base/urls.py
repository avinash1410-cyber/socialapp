from django.http import HttpResponse
from django.urls import path
from . import views
def home(request):
    return HttpResponse("Home PAge")


urlpatterns = [
    path('',views.home),
    path('home2',views.home,name="home"),
    path('room/<int:pk>',views.room,name="room"),
    path('room-creat/',views.createRoom,name="create_room"),
    path('room-update/<int:pk>',views.update,name="update_room"),
    path('room-delete/<int:pk>',views.delete,name="delete_room"),
    path('login/',views.userlogin,name="login"),
    path('register/',views.Registeruser,name="register"),
    path('logout/',views.userlogout,name="logout"),
    path('delete_msg/<int:pk>',views.msg_delete,name="delete_msg"),
    path('Profile/<int:pk>',views.profile,name="profile"),
    path('update-user/',views.updaetUser,name="update-user"),
]