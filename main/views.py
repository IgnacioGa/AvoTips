from django.shortcuts import render
from django.db.models import Avg, Count

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

from .models import Carrera, Universidad, Orientacion, Formulario, Especifica

from django import db
from .forms import Encuesta

from django.urls import reverse
from django.core import serializers
import json

from .forms import Encuesta

# Create your views here.


def average(objeto):
    stats = objeto.aggregate(Count('recomendacion'), Avg('recomendacion'), Avg(
        'cargaHoraria'), Avg('exigencia'), Avg('profesores'), Avg('progIntercambio'))
    return stats
    stats.clear()


def index(request):
    carrera = Carrera.objects.filter().values("titulo")
    universidad = Universidad.objects.filter().values("nombre")
    orientiacion = Orientacion.objects.filter().values("orientacion")
    especifica = Especifica.objects.filter()
    return render(request, "main/index.html", {
        "carreras": carrera,
        "universidades": universidad,
        "orientaciones": orientiacion,
        "especificas": especifica
    })


def carrera(request, titulo):
    # Datos de la carrera y su respectiva review
    carrera = Carrera.objects.get(titulo=titulo)
    form = Encuesta(initial={
                    'carrera': carrera})
    # form.fields['carrera'].disabled = True // Para que no se pueda editar
    relacionadas = carrera.relacionadas.all()
    resenasCAR = Formulario.objects.filter(carrera=carrera.id)
    stats = average(resenasCAR)
    comentarios = []
    for y in resenasCAR:
        title = y.tituloReseña
        comment = y.reseña
        usuario = y.nombre
        dicc = {
            'titulo': title,
            'comentario': comment,
            'usuario': usuario
        }
        comentarios.append(dicc)

    # Universidades donde esta la carrera y sus respectivas reviews
    unis = []
    SelectedUniversidades = carrera.universidadesSelf.all()
    for x in SelectedUniversidades:
        reseña = Formulario.objects.filter(universidad=x)
        uni = serializers.serialize(
            'json', Universidad.objects.filter(nombre=x), fields=('nombre'))
        datos = average(reseña)
        dicc = {
            "universidad": json.loads(uni),
            "stats": datos}
        unis.append(dicc)

    # Paginator de universidades de a 3
    number_of_item = 3
    paginatorr = Paginator(unis, number_of_item)
    first_page = paginatorr.page(1).object_list
    page_range = paginatorr.page_range

    context = {
        'paginatorr': paginatorr,
        'first_page': first_page,
        'page_range': page_range
    }
    if request.method == 'POST':
        page_n = request.POST.get('page_n', None)  # getting page number
        results = list(paginatorr.page(
            page_n).object_list)
        return JsonResponse({"results": results})
    else:
        return render(request, "main/test.html", {
            "carrera": carrera,
            "promedios": stats,
            "context": context,
            "relacionadas": relacionadas,
            "comentarios": comentarios,
            "form": form
        })


def saveReseña(request, titulo):
    if request.method == 'POST':
        encuesta = Encuesta(request.POST)
        if encuesta.is_valid():
            datos = encuesta.cleaned_data
            print(datos)
            new = Formulario(email=datos["email"], carrera=datos['carrera'], universidad=datos['universidad'], tituloReseña=datos['tituloReseña'], reseña=datos['reseña'], recomendacion=datos['recomendacion'], profesores=datos['profesores'],
                             exigencia=datos['exigencia'], cargaHoraria=datos['cargaHoraria'], progIntercambio=datos['progIntercambio'], tiempoCarrera=datos['tiempoCarrera'], nombre=datos['nombre'], permitirContacto=datos['permitirContacto'], contacto=datos['contacto'])
            new.save()
            return HttpResponseRedirect(reverse('main:carrera', args=(titulo,)))
        else:
            print(encuesta.errors)
            return HttpResponseRedirect(reverse('main:index'))


def universidad(request, nombre):
    pass


def orientacion(request, orientacion):
    pass


def especifica(request, especifica):
    pass
