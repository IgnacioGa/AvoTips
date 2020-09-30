from django.urls import path
from django.conf.urls import url

from . import views

from . import ajax

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("carrera/<str:titulo>", views.carrera, name="carrera"),
    path("universidad/<str:nombre>", views.universidad, name="universidad"),
    path("orientacion/<str:orientacion>",
         views.orientacion, name="orientacion"),
    path("especifica/<str:especifica>", views.especifica, name="especifica"),
    path("get_universidades",
         ajax.get_universidades, name='get_universidades'),
    path("saveReseña/<str:titulo>", views.saveReseña, name="saveReseña"),
]
