from django.db import models

# Create your models here.
class Universidad(models.Model):
	nombre = models.CharField(max_length=64)
	abreviacion = models.CharField(max_length=8, default="")
	color = models.CharField(max_length=64)
	descripcion = models.TextField()
	carreras = models.ManyToManyField('Carrera', related_name="universidadesSelf", blank=True)
	orientaciones = models.ManyToManyField('Orientacion', related_name="unisConOrientaciones", blank=True)
	video = models.CharField(max_length=255, blank=True, null=True)
	noticia = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		ordering = ['nombre']

	def __str__(self):
		return str(self.nombre)

class Carrera(models.Model):
	titulo = models.CharField(max_length=64)
	descripcion = models.TextField()
	video = models.CharField(max_length=255, blank=True, null=True)
	relacionadas =  models.ManyToManyField('self', related_name="relacionadas", blank=True)
	noticia = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		ordering = ['titulo']

	def __str__(self):
		return str(self.titulo)

class Especifica(models.Model):
	carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name="especifica")
	descripcion = models.TextField()
	universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE, related_name="carreraEspecifica")

	class Meta:
		ordering = ['carrera']

	def __str__(self):
		return str(self.carrera)

class Orientacion (models.Model):
	orientacion = models.CharField(max_length=64)
	descripcion = models.TextField(blank=True, null=True)
	carreras = models.ManyToManyField(Carrera, related_name="orientacion")

	class Meta:
		ordering = ['orientacion']

	def __str__(self):
		return str(self.orientacion)

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
