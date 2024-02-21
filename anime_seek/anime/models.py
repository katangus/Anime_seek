from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Otaku(models.Model): 
    """
    Características de um utilizador
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    path_image= models.CharField(max_length=30)
    
class Generos(models.Model):
    """
    Géneros do anime
    """ 
    genero = models.CharField(max_length=30,default=None) 

    def __str__(self):
        return self.genero
    
class Anime(models.Model):
    """
    Características do anime
    """
    anime = models.CharField(max_length=50)
    episodios= models.PositiveIntegerField() 
    generos = models.ForeignKey(Generos,on_delete=models.CASCADE,default=None)
    logo = models.CharField(max_length=500,default=None)

    def __str__(self):
        return self.anime

class List(models.Model): 
    """
    Lista de animes visto pelo utilizador, default ainda não viu
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)


class Review(models.Model):
    """
    Review feita pelo utilizador ao anime
    """
    anime = models.ForeignKey(Anime,on_delete=models.CASCADE) 
    user= models.ForeignKey(User, on_delete=models.CASCADE) 
    comentario = models.CharField(max_length=200)
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.comentario

    def foi_publicada_recentemente(self):
        return self.pub_data >= timezone.now() - datetime.timedelta(days=1)

class Friends(models.Model): 
    """
    Seguir um utilizador
    """
    following = models.ForeignKey(User,related_name ="following",default=None,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name ="user",on_delete=models.CASCADE,default=None)



