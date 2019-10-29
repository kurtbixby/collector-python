from django.db import models

# Create your models here.

class Game(models.Model):
    game_name = models.TextField()
    aliases = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % (self.game_name)

class Platform(models.Model):
    platform_name = models.TextField()
    manufacturer = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['manufacturer', 'platform_name'], name='unique-manufacturer-platform')
        ]

    def __str__(self):
        return '%s' % (self.platform_name)

class Region(models.Model):
    region_code = models.TextField(unique=True)

    def __str__(self):
        return '%s' % (self.region_code)

class Company(models.Model):
    company_name = models.TextField()

    def __str__(self):
        return '%s' % (self.company_name)

class Version(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='versions')
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
    version_name = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    publisher = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name='versions_published')
    developer = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name='versions_developed')

    def __str__(self):
        return '%s' % (self.version_name)

class Country(models.Model):
    country_code = models.TextField(unique=True)
    country_name = models.TextField()

    def __str__(self):
        return '%s: %s' % (self.country_code, self.country_name)
    
class Piece(models.Model):
    piece_type = models.TextField(unique=True)

    def __str__(self):
        return '%s' % (self.piece_type)

class Edition(models.Model):
    version = models.ForeignKey(Version, on_delete=models.PROTECT, related_name='editions')
    edition_name = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    pieces = models.ManyToManyField(Piece)

    def __str__(self):
        return '%s' % (self.edition_name)