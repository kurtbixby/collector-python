from django.db import models

# Create your models here.

class Game(models.Model):
    id = models.AutoField(primary_key=True)

class Platform(models.Model):
    platform_name = models.TextField()

class Region(models.Model):
    region_code = models.TextField()

class Company(models.Model):
    company_name = models.TextField()

class Version(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    version_name = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    publisher = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    developer = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)

class Country(models.Model):
    country_code = models.TextField()
    country_name = models.TextField()
    
class Piece(models.Model):
    piece_type = models.TextField()

class Edition(models.Model):
    version = models.ForeignKey(Version, on_delete=models.PROTECT)
    edition_name = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    pieces = models.ManyToManyField(Piece)
