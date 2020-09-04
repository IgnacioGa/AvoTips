from django.db import models

# Create your models here.
class Universidad(models.Model):
	nombre = models.CharField(max_length=64)
	abreviacion = models.CharField(max_length=4, default="")
	color = models.CharField(max_length=64)
	descripcion = models.TextField()
	carreras = models.ManyToManyField('Carrera', related_name="universidadesSelf", blank=True, null=True)
	video = models.CharField(max_length=255, blank=True, null=True)
	noticia = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return f"Universidad = {self.nombre}"

class Carrera(models.Model):
	titulo = models.CharField(max_length=64)
	descripcion = models.TextField()
	universidades = models.ManyToManyField(Universidad, related_name="carrerasSelf")
	video = models.CharField(max_length=255, blank=True, null=True)
	relacionadas =  models.ManyToManyField('self', related_name="relacionadas", blank=True, null=True)
	noticia = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return f"Carrera = {self.titulo}"

class Orientacion (models.Model):
	orientacion = models.CharField(max_length=64)
	carreras = models.ManyToManyField(Carrera, related_name="orientacion")
	informacion = models.TextField() 

	def __str__(self):
		return f"{self.orientacion} tiene estas carreras = {self.carreras}"

class Formulario (models.Model):	
	PRIMER_AÑO = 1
	SEGUNDO_AÑO = 2   
	TERCER_AÑO = 3
	CUARTO_AÑO = 4
	QUINTO_AÑO = 5
	TERMINADA = 6
	TIEMPO_CARRERA = (
        (PRIMER_AÑO, 'Primer año'),
        (SEGUNDO_AÑO, 'Segundo año'),
        (TERCER_AÑO, 'Tercer año'),
        (CUARTO_AÑO, 'Cuarto año'),
        (QUINTO_AÑO, 'Quinto año o más'),
        (TERMINADA, 'Termine la carrera'),
    )

	VALORACIONES = (
    (1, 'Una estrella'),
    (2, 'Dos estrella'),
    (3, 'Tres estrella'),
    (4, 'Cuatro estrella'),
    (5, 'Cinco estrella'),
)

	email = models.EmailField(max_length=254)
	carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name="opinionesCar")
	universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name="opinionesUni")
	tituloReseña = models.CharField(max_length=70, verbose_name="Titulo de la reseña")
	reseña = models.TextField()
	mostrarReseña = models.BooleanField()
	recomendacion = models.PositiveSmallIntegerField(choices= VALORACIONES, default=1)
	profesores = models.PositiveSmallIntegerField(choices= VALORACIONES, default=1)
	exigencia = models.PositiveSmallIntegerField(choices= VALORACIONES, default=1)
	cargaHoraria = models.PositiveSmallIntegerField(choices= VALORACIONES, default=1)
	progIntercambio = models.PositiveSmallIntegerField(choices= VALORACIONES, default=1)
	tiempoCarrera = models.PositiveSmallIntegerField(choices= TIEMPO_CARRERA, default=PRIMER_AÑO, blank=True, null=True)
	nombre = models.CharField(max_length=70, blank=True, null=True)
	permitirContacto = models.BooleanField()
	contacto = models.CharField(max_length=70, blank=True, null=True)

	def __str__(self):
		return f"Comentario de {self.email} sobre {self.carrera} de {self.universidad}"
