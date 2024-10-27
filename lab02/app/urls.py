from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="Home Page"),
    path('<int:pk>', views.get_laptop, name="Laptop"),
    path('delete/<int:pk>', views.delete_laptop, name="Delete Laptop"),
    path('add', views.add_laptop, name="Add Laptop"),
    path('edit/<int:pk>', views.update_laptop, name="Update Laptop")
]