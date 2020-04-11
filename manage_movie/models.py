from django.db import models
import pytz

# Create your models here.

class ManageMovie(models.Model):
    id           = models.AutoField(primary_key=True)
    title        = models.CharField(max_length=150)
    genre        = models.TextField(max_length=500)
    director     = models.TextField()
    actor        = models.TextField()
    writer       = models.TextField()
    plot         = models.TextField()
    poster       = models.TextField()
    imdb_rating  = models.CharField(max_length=100)
    imdb_id      = models.CharField(max_length=100)
    realease_date= models.CharField(max_length=200)
    imdbrating   = models.FloatField(default=0)
    added_date   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='movie'


