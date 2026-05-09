from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('index.html', views.index),
    path('Admin.html', views.Admin),
    path('Login.html', views.Login),
    path('Register.html', views.Register),

    path('Signup', views.Signup),
    path('UserLogin', views.UserLogin),
    path('AdminLogin', views.AdminLogin),

    path('AddFood.html', views.AddFood),
    path('AddFoodAction', views.AddFoodAction),

    path('ViewOrders', views.ViewOrders),
    path('Deliver', views.Deliver),

    path('BrowseProducts.html', views.BrowseProducts),
    path('SearchProductAction', views.SearchProductAction),

    path('BookOrder', views.BookOrder),
]