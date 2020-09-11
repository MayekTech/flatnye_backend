from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated

from .models import *

# section utilisateur debut 
class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        # fields = '__all__'
        exclude = ['user', 'deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {
            'valide': {'write_only': True},
        }
   

class UserSerializer(serializers.ModelSerializer):
    profile = CompteSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'read_only': True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        for prof in profile_data:
            Compte.objects.create(user=user, **prof)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        profile.nom = profile_data.get('nom', profile.nom)
        profile.adresse = profile_data.get('adresse', profile.adresse)
        profile.email = profile_data.get('email', profile.email)
        profile.contact = profile_data.get('contact', profile.contact)
        profile.localisation = profile_data.get('localisation', profile.localisation)
        profile.type_compte = profile_data.get('type_compte', profile.type_compte)
        profile.image = profile_data.get('image', profile.image)
        profile.valide = profile_data.get('valide', profile.valide)
        profile.save()
        return instance
# section utilisateur end


# post des biens start
    # Gestion des Commentaires et Notations debut
class NotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notation
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']
    # Gestion des Commentaires et Notations fin

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']


class VisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visite
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']


class BienSerializer(serializers.ModelSerializer):
    media_set = MediaSerializer(required=False, many=True, allow_null=True)
    visite_set = VisiteSerializer(required=False, many=True, allow_null=True)
    comment_set = CommentSerializer(read_only=True, many=True)
    notation = NotationSerializer(read_only=True, many=True)


    class Meta:
        model = Bien
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

    def create(self, validated_data):
        media_data = validated_data.pop('media_set')
        visite_data = validated_data.pop('visite_set')

        # creer le bien en premier
        bien_encours = Bien.objects.create(**validated_data)

        # creer le media et le lier au bien en cours
        for media in media_data:
            Media.objects.create(bien_decrit=bien_encours, **media)
    
        # creer la visite et le lier au bien en cours
        for visite in visite_data:
            Media.objects.create(bien_visite=bien_encours, **visite)
        
        return bien_encours
    
    def update(self, instance, validated_data):
        media_data = validated_data.pop('media_set')
        visite_data = validated_data.pop('visite_set')
        media = instance.media_set
        visite = instance.visite_set

        # mise a jour du media
        media.titre = media_data.get('titre', media.titre)
        media.type = media_data.get('type', media.type)
        media.save()

        # mise a jour de la visite
        visite.titre = visite_data.get('titre', visite.titre)
        visite.fichier = visite_data.get('fichier', visite.fichier)
        visite.save()

        # retourner le bien en cours
        return instance
# post des biens end

#Post d'Article start
class ArticleSerializer(serializers.ModelSerializer):
    media_set = MediaSerializer(required=False, many=True, allow_null=True)
    comment_set = CommentSerializer(read_only=True, many=True)


    class Meta:
        model = Article
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

    def create(self, validated_data):
        media_data = validated_data.pop('media_set')

        # creer l'article en premier
        article_encours = Article.objects.create(**validated_data)

        # creer le media et le lier à l'article en cours
        for media in media_data:
            Media.objects.create(article_decrit=article_encours, **media)
    
        return article_encours
    
    def update(self, instance, validated_data):
        media_data = validated_data.pop('media_set')
        media = instance.media_set

        # mise a jour du media
        media.titre = media_data.get('titre', media.titre)
        media.type = media_data.get('type', media.type)
        media.save()

        # retourner l'article en cours
        return instance

#Post d'Article end

#Processus de location start
class LocationSerializer(serializers.ModelSerializer):
    # bien_loue = BienSerializer(required=False, many=False, allow_null=True)
    class Meta:
        model = Loaction
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']
#Processus de location end

#Processus d'achat start
class AddPanierSerializer(serializers.ModelSerializer):
    # bien_loue = BienSerializer(required=False, many=False, allow_null=True)
    class Meta:
        model = AjoutPanier
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

class PanierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panier
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

class AchatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achat
        exclude = ['deleted']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at']

#Processus d'achat end
