from django.contrib import admin

from .models import Universidad, Carrera, Orientacion, Formulario

# Register your models here.
class UniversidadAdmin(admin.ModelAdmin):
    filter_horizontal = ("carreras",)

# Register your models here.
class CarrerasAdmin(admin.ModelAdmin):
    filter_vertical = ("universidades",)
    filter_horizontal = ("relacionadas",)

class OrientiacionAdmin(admin.ModelAdmin):
	filter_horizontal = ("carreras",)

admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Carrera, CarrerasAdmin)
admin.site.register(Orientacion, OrientiacionAdmin)
admin.site.register(Formulario)
