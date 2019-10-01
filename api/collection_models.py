# Django
from django.db import models

# Local Component
from game_models import Game, Version, Edition, Piece

# Create your models here.

class Collection(models.Model):
    id = models.AutoField(primary_key=True)

class Condition(models.Model):
    condition_description = models.TextField()

class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    version = models.ForeignKey(Version, on_delete=models.PROTECT, null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.PROTECT, null=True, blank=True)
    notes = models.TextField()
    condition = models.TextField()
    pieces = models.ManyToManyField(Piece)