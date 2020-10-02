from django.urls import path
from django.conf.urls import url

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("carrera/<str:titulo>", views.carrera, name="carrera"),
    path("universidad/<str:nombre>", views.universidad, name="universidad"),
    path("orientacion/<str:orientacion>",
         views.orientacion, name="orientacion"),
    path("especifica/<str:especifica>", views.especifica, name="especifica"),
    path("saveReseña/<str:titulo>", views.saveReseña, name="saveReseña"),
    path("busqueda", views.busqueda, name="busqueda")
]
