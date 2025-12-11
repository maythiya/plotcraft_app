from django.urls import path
from django.contrib.auth import views as auth_views
from .views import landing, home, register, profile
from myapp import views


urlpatterns = [

    path('', landing, name='landing'),   # root → landing
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('profile/', profile, name='profile'),
    path('quickguide/', auth_views.TemplateView.as_view(template_name='Quickguide.html'), name='quickguide'),

    path('search/', views.global_search, name='global_search'),


]