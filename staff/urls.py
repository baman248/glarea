from django.urls import path

from . import views
app_name = 'store'

urlpatterns = [
    # path('register/',views.register, name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout')
]