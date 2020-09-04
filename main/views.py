from django.shortcuts import render

from .models import Carrera, Universidad, Orientacion, Formulario

# Create your views here.
def index(request):
	carrera = Carrera.objects.filter().values("titulo")
	universidad = Universidad.objects.filter().values("nombre")
	orientiacion = Orientacion.objects.filter().values("orientacion")
	return render(request, "main/index.html", {
		"carreras": carrera,
		"universidades": universidad,
		"orientaciones": orientiacion
		})

def carrera(request,titulo):
	uni = Carrera.objects.filter(titulo=titulo).values("universidades")
	carrera = Carrera.objects.filter(titulo=titulo)
	reseñas = Formulario.objects.filter(carrera__titulo=titulo)
	for u in uni:
		universidades = Universidad.objects.filter(nombre=u)
	return render(request, "main/test.html", {
		"carreras": carrera,
		"reseñas": reseñas,
		"universidades": universidades
		})

def universidad(reques,nombre):
	pass

def orientacion(reques,orientacion):
	pass