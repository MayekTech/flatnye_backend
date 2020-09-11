from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.


class TimeModel(models.Model):
    class Meta:
        verbose_name = ("")
        verbose_name_plural = ("s")

    created_at = models.DateTimeField(
        "Date creation", auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(
        "Date de mise ajour", auto_now=True, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    deleted_at = models.DateTimeField(
        "Date de suppression", blank=True, null=True)

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
        return f"{self.id}"

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Compte(TimeModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(
        max_length=254, unique=True, blank=True, null=True)
    contact = models.CharField(
        max_length=10, unique=True, null=True, blank=True)
    localisation = models.CharField(max_length=254,  blank=True, null=True)
    TYPE_COMPTE = (
        ('Ge', 'Gerant'),
        ('Ag', 'Agence'),
    )
    type_compte = models.CharField(
        max_length=2, choices=TYPE_COMPTE, blank=True, null=True)

    image = models.ImageField(
        upload_to="User/Profile", blank=True, null=True, verbose_name="Image de profile")
    valide = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.nom

    def __unicode__(self):
        return self.nom

    def valider(self):
        val = 0
        try:
            self.valide = True
        except:
            val = -1
        finally:
            return val

# def create_compte(sender, **kwargs):
#     """
#     Pour creer automatiquement un compte dès la creation d'un `User`
#     """
#     if kwargs['created']:
#         user_compte = Compte.objects.create(user=kwargs['instance'])

# post_save.connect(create_compte, sender=User)


class Article(models.Model):
    titre = models.CharField("Titre de l'article", max_length=150, blank=True, null=True)
    texte = models.TextField("Contenu de l'article", blank=True, null=True)
    ETAT_ARTICLE = (
        ('Pub', 'Publié'),
        ('Brl', 'Brouillon'),
        ('Anl', 'Annulé'),
    )
    etat = models.CharField(max_length=3, choices=ETAT_ARTICLE, blank=True, null=True)

    def __str__(self):
        return self.titre

    def __unicode__(self):
        return self.titre


class Bien(TimeModel):
    agence = models.ForeignKey(
        Compte, on_delete=models.CASCADE, blank=True, null=True)
    titre = models.CharField(max_length=150, blank=True, null=True)
    localisation = models.CharField(
        "coordonées GPS", max_length=150, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)
    quartier = models.CharField(max_length=50, blank=True, null=True)

    dimensions = models.CharField(
        "Superficie, taille", max_length=100, blank=True, null=True)

    description = models.CharField(max_length=254, blank=True, null=True)
    prix = models.FloatField(blank=True, null=True)
    date_mise_en_ligne = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    TYPE_BIEN = (
        ('T', 'Terrain'),
        ('V', 'Villa'),
        ('M', 'Maison'),
        ('A', 'Appartement'),
        ('C', 'Chambre'),
    )
    type = models.CharField(
        max_length=1, choices=TYPE_BIEN, blank=True, null=True)

    CATEGORIE_BIEN = (
        ('L', 'Location'),
        ('V', 'Vente'),
    )
    categorie = models.CharField(
        max_length=1, choices=CATEGORIE_BIEN, blank=True, null=True)

    ETAT_BIEN = (
        ('V', 'Vendu'),
        ('R', 'Reservé'),
        ('L', 'Loué'),
    )
    etat = models.CharField(
        max_length=1, choices=ETAT_BIEN, blank=True, null=True)
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
    bien_note = models.ForeignKey(
        Bien, on_delete=models.CASCADE, blank=True, null=True)

    class Notation(models.IntegerChoices):
        MEDIOCRE = 1
        ACCEPTABLE = 2
        BIEN = 3
        TRES_BIEN = 4
        EXELLENT = 5
    nombre_etoile = models.IntegerField(
        choices=Notation.choices, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_etoile}"

    def __unicode__(self):
        return f"{self.nombre_etoile}"


class Commentaire(TimeModel):
    bien_comment = models.ForeignKey(Bien, on_delete=models.CASCADE, blank=True, null=True)
    article_comment = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True)
    contenu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    def __unicode__(self):
        return f"{self.id}"

class Media(TimeModel):
    bien_decrit = models.ForeignKey(
        Bien, on_delete=models.CASCADE, blank=True, null=True)
    article_media = models.ForeignKey(
        Article, on_delete=models.CASCADE, blank=True, null=True)
    titre = models.CharField(max_length=100, blank=True, null=True)
    TYPE_MEDIA = (
        ('V', 'Video'),
        ('P', 'Photo'),
    )
    type = models.CharField(
        max_length=1, choices=TYPE_MEDIA, blank=True, null=True)

    def upload_media(self, filename):
        path = 'File/Description/{}'.format(filename)
        return path

    fichier = models.FileField(upload_to=upload_media, blank=True, null=True)

    def __str__(self):
        return self.titre

    def __unicode__(self):
        return self.titre


class Visite(TimeModel):
    bien_viste = models.ForeignKey(
        Bien, on_delete=models.CASCADE, blank=True, null=True)
    titre = models.CharField(max_length=100, blank=True, null=True)

    def upload_fichier(self, filename):
        path = 'File/Visite/{}'.format(filename)
        return path

    fichier = models.FileField(upload_to=upload_fichier, blank=True, null=True)

    def __str__(self):
        return self.titre

    def __unicode__(self):
        return self.titre


class Panier(TimeModel):
    # owner = models.
    bien_panier = models.ManyToManyField(Bien, through="AjoutPanier")
    slug = models.SlugField(max_length=50)
    est_regle = models.BooleanField(blank=True, null=True, default=False)

    def regler(self):
        val = 0
        try:
            self.est_regle = True
        except:
            val = -1
        finally:
            return val

    def __str__(self):
        return self.slug

    def __unicode__(self):
        return self.slug


class AjoutPanier(TimeModel):
    bucket = models.ForeignKey(
        Panier, blank=True, null=True, on_delete=models.CASCADE)
    bien_ajout = models.ForeignKey(Bien, blank=True, null=True, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    TYPE_AJOUT = (
        ('A', 'Achat'),
        ('L', 'Location'),
    )
    type_ajout = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return self.date_ajout

    def __unicode__(self):
        return self.date_ajout


class Achat(TimeModel):
    date_achat = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    biens_panier = models.ForeignKey(
        Panier, on_delete=models.CASCADE, blank=True, null=True)
    biens = models.ForeignKey(
        Bien, on_delete=models.CASCADE, blank=True, null=True)
    montant = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Achat du {self.date_achat}"

    def __unicode__(self):
        return f"Achat du {self.date_achat}"


class Loaction(TimeModel):
    date_paiement = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    bien_loue = models.ForeignKey(
        Bien, on_delete=models.CASCADE, blank=True, null=True)
    montant = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Loué le {self.date_paiement}"

    def __unicode__(self):
        return f"Loué le {self.date_paiement}"
