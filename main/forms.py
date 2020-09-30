from django.forms import ModelForm
from django import forms
from .models import Formulario, Carrera, Universidad


class Encuesta(forms.ModelForm):

    class Meta:
        model = Formulario
        fields = ['carrera', 'universidad', 'email', 'nombre', 'recomendacion',
                  'profesores', 'exigencia', 'cargaHoraria', 'progIntercambio', 'tiempoCarrera', 'tituloReseña', 'reseña', 'permitirContacto', 'contacto', ]
