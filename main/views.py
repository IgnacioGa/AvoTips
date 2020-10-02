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
    espe = list()
    carrera = Carrera.objects.filter().values("titulo")
    universidad = Universidad.objects.filter().values("nombre")
    orientiacion = Orientacion.objects.filter().values("orientacion")
    especifica = Especifica.objects.all()
    for x in especifica:
        dato = x.serialize()
        espe.append(dato['item'])
    return render(request, "main/index.html", {
        "carreras": carrera,
        "universidades": universidad,
        "orientaciones": orientiacion,
        "especificas": espe
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


def busqueda(request):
    if 'term' in request.GET:
        cs = Carrera.objects.filter(
            titulo__icontains=request.GET.get('term'))
        us = Universidad.objects.filter(
            nombre__icontains=request.GET.get('term'))
        os = Orientacion.objects.filter(
            orientacion__icontains=request.GET.get('term'))
        searchs = list()
        for value in cs:
            urlC = 'carrera/' + value.titulo
            dicc = {
                'url': urlC,
                'label': value.titulo,
                'value': value.titulo
            }
            searchs.append(dicc)
            es = value.especifica.all()
            for x in es:
                dato = x.serialize()
                urlE = "especifica/" + dato['item']
                dicc = {
                    'url': urlE,
                    'label': dato['item'],
                    'value': dato['item']
                }
                searchs.append(dicc)

        for value in us:
            urlU = 'universidad/' + value.nombre
            dicc = {
                'url': urlU,
                'label': value.nombre,
                'value': value.nombre
            }
            searchs.append(dicc)
            es = value.carreraEspecifica.all()
            for x in es:
                dato = x.serialize()
                urlE = "especifica/" + dato['item']
                dicc = {
                    'url': urlE,
                    'label': dato['item'],
                    'value': dato['item']
                }
                searchs.append(dicc)

        for value in os:
            urlO = 'orientacion/' + value.orientacion
            dicc = {
                'url': urlO,
                'label': value.orientacion,
                'value': value.orientacion
            }
            searchs.append(dicc)
        print(searchs)
        return JsonResponse(searchs, safe=False)


def universidad(request, nombre):
    pass


def orientacion(request, orientacion):
    pass


def especifica(request, especifica):
    pass
