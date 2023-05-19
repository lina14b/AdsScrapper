# from django.db import models
# # from djongo import models as djongo_models
# import uuid


# class Immo(models.Model):
    
#     url = models.CharField(max_length=100)
#     code = models.IntegerField()
#     price = models.IntegerField()
#     surfaceTotale = models.IntegerField()
#     surface_habitable = models.IntegerField()
#     adresse = models.TextField()
#     country = models.CharField(max_length=30)
#     state = models.CharField(max_length=30)
#     zone = models.CharField(max_length=30)
#     ville = models.CharField(max_length=30)
#     etage = models.IntegerField()
#     place_voiture= models.IntegerField()
#     nombre_de_chambre = models.IntegerField()
#     nombre_de_piece = models.IntegerField()
#     nombre_de_salle_de_bain = models.IntegerField()
#     dateinstered = models.CharField(max_length=30)
#     datemodified = models.CharField(max_length=30)
#     anneeconstruction = models.IntegerField()
#     TotalDescp = models.TextField()

# class Characteristic(djongo_models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100)
#     def __str__(self):
#         return self.name

# class Property(djongo_models.Model):
#     characteristicslist = djongo_models.ArrayField(
#         model_container=Characteristic
#     )

# class Imageurl(djongo_models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     urlimg = models.CharField(max_length=100)
#     def __str__(self):
#         return self.urlimg

# class Imageurlslist(djongo_models.Model):
#     imagesurlslist = djongo_models.ArrayField(model_container=Imageurl)