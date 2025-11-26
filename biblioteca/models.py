from django.db import models
from usuarios.models import Usuario


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, related_name="libros")
    genero = models.CharField(
        max_length=50,
        choices=[
            ("romance", "Romance"),
            ("terror", "Terror"),
            ("policial", "Policial"),
            ("ciencia_ficcion", "Ciencia Ficción"),
            ("fantasia", "Fantasía"),
            ("historia", "Historia"),
        ],
        default="romance"
    )
    fecha_publicacion = models.DateField(blank=True, null=True)
    portada = models.ImageField(upload_to="portadas/", blank=True, null=True)

    def __str__(self):
        return self.titulo


class Reseña(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="reseñas")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="reseñas")
    comentario = models.TextField()
    calificacion = models.PositiveSmallIntegerField(default=1)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.libro.titulo}"


class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial_libros')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.usuario.username} consultó {self.libro.titulo}"


class Lista(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='listas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    libros = models.ManyToManyField(Libro, related_name='listas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    reseña = models.ForeignKey(Reseña, on_delete=models.CASCADE, related_name="comentarios")
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.reseña.libro.titulo}"


class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="favoritos")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="favoritos")
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'libro')

    def __str__(self):
        return f"{self.usuario.username} → {self.libro.titulo}"
