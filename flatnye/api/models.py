from django.db import models
import uuid 
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.

class TimeModel(models.Model):
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")
    
    created_at = models.DateTimeField("Date creation", auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField("Date de mise ajour", auto_now=True, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    deleted_at = models.DateTimeField("Date de suppression", blank=True, null=True)

    def suppress(self):
        val = 0
        try:
            self.deleted = True
            self.deleted_at = timezone.now
        except:
            val = -1
        finally:
            return val

    def restore(self):
        val = 0
        try:
            self.deleted = False
            self.deleted_at = None
        except:
            val = -1
        finally:
            return val

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Compte(TimeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    addresse = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)
    contact = models.CharField(max_length=10, unique=True, null=True, blank=True)
    localisation = models.CharField(max_length=254,  blank=True, null=True)
    image = models.ImageField(upload_to="User/Profile", blank=True, null=True, verbose_name="Image de profile")

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return self.nom

# def create_compte(sender, **kwargs):
#     """
#     Pour creer automatiquement un compte dès la creation d'un `User`
#     """
#     if kwargs['created']:
#         user_compte = Compte.objects.create(user=kwargs['instance'])

# post_save.connect(create_compte, sender=User)

class Bien(TimeModel):
    agence = models.ForeignKey(Compte, on_delete=models.CASCADE, blank=True, null=True)
    titre = models.CharField(max_length=150, blank=True, null=True)
    localisation = models.CharField("coordonées GPS", max_length=150, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    quartier = models.CharField(max_length=50, blank=True, null=True)

    dimensions = models.CharField("Superficie, taille", max_length=100, blank=True, null=True)
    dimensions = models.SET()

    description = models.CharField(max_length=254, blank=True, null=True)
    prix = models.FloatField(blank=True, null=True)
    date_mise_en_ligne = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    TYPE_BIEN = (
        ('T', 'Terrain'),
        ('V', 'Villa'),
        ('M', 'Maison'),
        ('A', 'Appartement'),
        ('C', 'Chambre'),
    )
    type = models.CharField(max_length=1, choices=TYPE_BIEN, blank=True, null=True)

    CATEGORIE_BIEN = (
        ('L', 'Location'),
        ('V', 'Vente'),
    )
    categorie = models.CharField(max_length=1, choices=CATEGORIE_BIEN, blank=True, null=True)

    ETAT_BIEN = (
        ('V', 'Vendu'),
        ('R', 'Reservé'),
        ('L', 'Loué'),
    )
    etat = models.CharField(max_length=1, choices=ETAT_BIEN, blank=True, null=True)
    est_valide = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.titre

    def __unicode__(self):
        return self.titre
    
    def reserver(self):
        val = 0
        try:
            self.etat = 'R'
        except:
            val = -1
        finally:
            return val

    def vendre(self):
        val = 0
        try:
            self.etat = 'V'
        except:
            val = -1
        finally:
            return val

    def louer(self):
        val = 0
        try:
            self.etat = 'L'
        except:
            val = -1
        finally:
            return val

class Notation(TimeModel):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, blank=True, null=True)

    class Notation(models.IntegerChoices):
        MEDIOCRE = 1
        ACCEPTABLE = 2
        BIEN = 3
        TRES_BIEN = 4
        EXELLENT = 5
    nombre_etoile = models.IntegerField(choices=Notation.choices, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_etoile}"

    def __unicode__(self):
        return f"{self.nombre_etoile}"
        

class Commentaire(TimeModel):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, blank=True, null=True)
    contenu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    def __unicode__(self):
        return f"{self.id}"


class Media(TimeModel):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, blank=True, null=True)
    titre = models.CharField(max_length=100, blank=True, null=True)
    TYPE_MEDIA = (
        ('V', 'Video'),
        ('P', 'Photo'),
    )
    type = models.CharField(max_length=1, choices=TYPE_MEDIA, blank=True, null=True)
    
    def upload_media(self, filename):
        path = 'File/Description/{}'.format(filename)
        return path
    
    fichier = models.FileField(upload_to=upload_media, blank=True, null=True)


    def __str__(self):
        return self.titre

    def __unicode__(self):
        return self.titre

class Visite(TimeModel):
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE, blank=True, null=True)
    titre = models.CharField(max_length=100, blank=True, null=True)

    def upload_fichier(self, filename):
        path = 'File/Visite/{}'.format(filename)
        return path
    
    fichier = models.FileField(upload_to=upload_fichier, blank=True, null=True)

    def __str__(self):
        return self.titre

    def __unicode__(self):
        return self.titre

