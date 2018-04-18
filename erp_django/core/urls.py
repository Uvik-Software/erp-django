from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('heroes', views.heroes),
    path('hero/<int:id>', views.hero),
    re_path('^.*', views.index, name='index'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
