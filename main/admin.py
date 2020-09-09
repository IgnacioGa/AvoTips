from django.contrib import admin

from .models import Universidad, Carrera, Orientacion, Formulario, Especifica

# Register your models here.
class UniversidadAdmin(admin.ModelAdmin):
    filter_horizontal = ('carreras', 'orientaciones',)

# Register your models here.
class CarrerasAdmin(admin.ModelAdmin):
    filter_horizontal = ('universidades', 'relacionadas', 'orientaciones',)    

class OrientiacionAdmin(admin.ModelAdmin):
	filter_horizontal = ("carreras",)

admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Carrera, CarrerasAdmin)
admin.site.register(Orientacion, OrientiacionAdmin)
admin.site.register(Especifica)

admin.site.register(Formulario)
