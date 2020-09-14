from django.shortcuts import render
from django.db.models import Avg, Count

from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Carrera, Universidad, Orientacion, Formulario, Especifica

from django import db

# Create your views here.
def show_queries():
    for query in db.connection.queries:
        print (query["sql"])
    db.reset_queries()

def index(request):
    carrera = Carrera.objects.filter().values("titulo")
    universidad = Universidad.objects.filter().values("nombre")
    orientiacion = Orientacion.objects.filter().values("orientacion")
    especifica = Especifica.objects.filter()
    return render(request, "main/index.html", {
        "carreras": carrera,
        "universidades": universidad,
        "orientaciones": orientiacion,
        "especificas" : especifica
        })

def carrera(request,titulo):
	#Datos de la carrera y su respectiva review
	stats = {}
	carrera = Carrera.objects.get(titulo=titulo)
	relacionadas = carrera.relacionadas.all()
	resenasCAR = Formulario.objects.filter(carrera=carrera.id)
	stats = resenasCAR.aggregate(Count('recomendacion'), Avg('recomendacion'), Avg('profesores'), Avg('exigencia'), Avg('cargaHoraria'), Avg('progIntercambio'))

	#Universidades donde esta la carrera y sus respectivas reviews
	unis = []
	SelectedUniversidades = carrera.universidadesSelf.all()
	for x in SelectedUniversidades:
		reseña = Formulario.objects.filter(universidad=x)
		datos = reseña.aggregate(Count('recomendacion'), Avg('recomendacion'), Avg('profesores'), Avg('exigencia'), Avg('cargaHoraria'), Avg('progIntercambio'))
		dicc = {
			"universidad": x,
			"stats": datos
		}
		unis.append(dicc)

	#Paginator de universidades de a 3
	my_model = SelectedUniversidades.values()
	number_of_item = 2
	paginatorr = Paginator(my_model, number_of_item)
	first_page = paginatorr.page(1).object_list
	page_range = paginatorr.page_range

	context = {
    'paginatorr':paginatorr,
    'first_page':first_page,
    'page_range':page_range
    }
	if request.method == 'POST':
		page_n = request.POST.get('page_n', None) #getting page number
		results = list(paginatorr.page(page_n).object_list.values('id', 'nombre'))
		return JsonResponse({"results":results})

	return render(request, "main/career.html", {
		"carrera": carrera,
		"promedios": stats,
		"universidades": unis,
		"context": context,
		"relacionadas": relacionadas
		})


def universidad(request,nombre):
    pass

def orientacion(request,orientacion):
    pass

def especifica(request,especifica):
    pass
