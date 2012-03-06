from django.db import models

class FeelingData(models.Model):
    CONDITIONS = (
        (1, 'sunny'),
        (2, 'rainy'),
        (3, 'snowy'),
        (4, 'cloudy')
    )
    # imageid
    feeling = models.ForeignKey('Feeling')
    sentence = models.TextField()
    postdatetime = models.DateTimeField(null=True)
    posturl = models.URLField(null=True)
    gender = models.NullBooleanField(null=True)
    born = models.SmallIntegerField(null=True)
    country = models.CharField(max_length=64, null=True)
    state = models.CharField(max_length=16, null=True)
    city = models.CharField(max_length=64, null=True)
    lat = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='latitude', null=True)
    lon = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='longitude', null=True)
    conditions = models.SmallIntegerField(choices=CONDITIONS, null=True)

class Feeling(models.Model):
    name = models.CharField(max_length=64, blank=False, primary_key=True)
    color = models.CharField(max_length=64, blank=False)
