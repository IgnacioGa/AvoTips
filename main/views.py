from django.shortcuts import render

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
    carrera = Carrera.objects.get(titulo=titulo)
    relacionadas = carrera.relacionadas.all()
    # Promedios de la carrera
    recomendaciones = 0
    profesores = 0
    exigencia = 0
    cargaHorario = 0
    intercambios = 0
    contador = 0
    resenasCAR = Formulario.objects.filter(carrera=carrera.id)

    for stats in resenasCAR:
        recomendaciones += stats.recomendacion
        profesores += stats.profesores
        exigencia += stats.exigencia
        cargaHorario += stats.cargaHoraria
        intercambios += stats.progIntercambio
        contador += 1

    promedioRec = recomendaciones / contador
    promedioPro = profesores / contador
    promedioExi = exigencia / contador
    promedioCHs = cargaHorario / contador
    promedioInt = intercambios / contador
    promedios = [promedioRec, promedioPro, promedioExi, promedioCHs, promedioInt]

    # Promedios de las universidades donde esta la carrera
    recomen = 0
    contador2 = 0
    calculo = 0
    resenaUNI = []
    SelectedUniversidades = carrera.universidades.all()
    for x in SelectedUniversidades:
        resena = Formulario.objects.filter(universidad=x)
        for y in resena:
            recomen += y.recomendacion
            contador2 += 1
        calculo = recomen / contador2
        resenaUNI.append(calculo)
        recomen = 0
        contador2 = 0
        calculo = 0


    return render(request, "main/career.html", {
        "carrera": carrera,
        "universidades": SelectedUniversidades,
        "promedios": promedios,
        "promedioUni": resenaUNI,
        "relacionadas": relacionadas,
        })

def universidad(reques,nombre):
    pass

def orientacion(reques,orientacion):
    pass

def especifica(reques,especifica):
    pass
