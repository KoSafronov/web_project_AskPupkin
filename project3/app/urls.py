from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('login/', views.logout, name='logout'),

    path('questions/<int:question_id>', views.question, name='question'),
    path('tags/<tag_name>', views.tag, name='tag'),
    path('404/', views.oops_404, name='oops'),

]
