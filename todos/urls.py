from django.urls import path
from . import views

urlpatterns =[
    path('',views.list_todo_items),
    path('owner/',views.owner, name= 'owner'),
    path('signup/', views.sign_up, name="signup"),
    path('signup/', views.sign_up, name="signup"),
    path('login/', views.user_login, name="login"),
    path('profile/', views.user_profile, name = "profile"),
    path('logout/', views.user_logout, name = "logout"),

    path('insert_todo/',views.insert_todo_item,name='insert_todo_item'),
    path('delete_todo/<int:todo_id>/',views.delete_todo_item,name='delete_todo_item'),
]