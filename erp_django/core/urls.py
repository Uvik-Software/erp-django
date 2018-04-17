from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('heroes', views.heroes),
    path('hero/<int:id>', views.hero),

]