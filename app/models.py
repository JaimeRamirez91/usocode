from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
      # Perfil de usuario.

class Curso(models.Model):
      Ciclo = models.IntegerField()
      Nombre_Curso = models.CharField(max_length=60)
      Descripcion_Curso = models.CharField(max_length=120)
      Instructor = models.ForeignKey(User)
      # def __str__(self):
      #       retorna = []
      #       retorna.append(self.Ciclo)
      #       retorna.append(self.Nombre_Curso)
      #       # return 'Ciclo=%s, Nombre=%s' % (self.Ciclo, self.Nombre_Curso)
      #       return retorna

class Inscritos(models.Model):
      Curso = models.ForeignKey(Curso)
      Alumno = models.ForeignKey(User)
      Estado = models.IntegerField()

class Guia (models.Model):
      Numero_Guia = models.CharField(max_length=20)
      Tema_Guia = models.CharField(max_length=120)
      Descripcion_guia = models.CharField(max_length=120)
      Curso = models.ForeignKey(Curso)
      Guiahtml = models.TextField()

class Guia_User (models.Model):
      Estado = models.IntegerField()
      Nota = models.DecimalField(max_digits=2, decimal_places=2)
      Fecha_Mod = models.DateTimeField(auto_now=True)
      Guia = models.ForeignKey(Guia)
      Alumno = models.ForeignKey(User)

class Ejercicio (models.Model):
      Numero_ej = models.IntegerField()
      Tema_Eje = models.CharField(max_length=120)
      Descripcion_Ej = models.CharField(max_length=400)
      Guia = models.ForeignKey(Guia)

class Ejer_User (models.Model):
      Estado = models.IntegerField()
      Codigo = models.TextField()
      Guia = models.ForeignKey(Guia)
      Alumno = models.ForeignKey(User)
      Numero_ej=models.IntegerField()
