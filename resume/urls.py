from django.urls import path

from . import views

urlpatterns =[
    path('', views.homepage, name='Home'),
    path('post/<slug:slug>/', views.postpage, name='Post'),
    path('number/', views.posts, name='List'),
    path('profile/', views.profile, name='Personal'),

    path('newpost/', views.createpost, name='New'),
    path('updatepost/<slug:slug>/', views.updatepost, name='Update'),
    path('delete/<slug:slug>/', views.deletepost, name='Delete'),

    path('send_email/', views.sendemail, name='Message'),
]