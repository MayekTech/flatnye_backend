from django.shortcuts import render
from django.utils import timezone
from rest_framework import renderers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from .serializers import *
from .models import *


# Gestion des utulisateurs ou comptes(AGences et Administrateurs) start
class UserViewSet(viewsets.ModelViewSet):
    """
    me donne acces aux url 'list' et 'detail' en meme temps
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

#   # Methodes suplementaire start
#     def destroy(self, request, pk=None):
#         objet = User.objects.get(pk=pk)
#         try:
#             objet.deleted = True
#             objet.deleted_at = timezone.now()
#             objet.save()
#             return Response({'status': 'Suppression faite'})
#         except:
#             return Response({'status': 'Erreur lors de la suppression'})

#     @action(detail=True, permission_classes=[permissions.IsAuthenticated])
#     def restore(self, request, pk=None):
#         objet = User.objects.get(pk=pk)
#         try:
#             objet.deleted = False
#             objet.deleted_at = None
#             objet.save()
#             return Response({'status': 'Les données ont été restaurées avec succes'})
#         except:
#             return Response({'status': 'Erreur lors de la suppression'})

#     @action(detail=False, permission_classes=[permissions.IsAuthenticated])
#     def get_deleted_list(self, request):
#         objet = User.objects.filter(deleted=True).order_by('-deleted_at')
#         serializer = self.get_serializer(objet, many=True)
#         return Response(serializer.data)
#     # Methodes suplementaire end



class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.filter(deleted=False)
    serializer_class = CompteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Methodes suplementaire de compte start
    def destroy(self, request, pk=None):
        objet = Compte.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Compte.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Compte.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)

    # Methodes suplementaire de compte end

# Gestion des utulisateurs ou comptes(AGences et Administrateurs) end

# Post des biens et ses descritions(Images, Videos, Viste) start

class BienSet(viewsets.ModelViewSet):
    # queryset = Zone.objects.all()
    queryset = Bien.objects.filter(deleted=False)
    serializer_class = BienSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Methodes suplementaire de bien start

    def destroy(self, request, pk=None):
        objet = Bien.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Bien.objects.get(pk=pk) 
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Bien.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)
    
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def reserver(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.reserver()
            objet.save()
            return Response({'status': 'Le bien a été reservé avec succes'})
        except:
            return Response({'status': 'Erreur lors de la reservation'})
    
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def louer(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.louer()
            objet.save()
            return Response({'status': 'Le bien a été loué avec succes'})
        except:
            return Response({'status': 'Erreur lors de la procedure de location'})
    
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def vendre(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.vendre()
            objet.save()
            return Response({'status': "L'achat a été bien effectué"})
        except:
            return Response({'status': "Erreur lors de l'achat"})

    # Methodes suplementaire de bien end


class MediaSet(viewsets.ModelViewSet):
    queryset = Media.objects.filter(deleted=False)
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Methodes suplementaire de media start
    def destroy(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Media.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)
    
    # Methodes suplementaire de media end


class VisiteSet(viewsets.ModelViewSet):
    queryset = Visite.objects.filter(deleted=False)
    serializer_class = VisiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Methodes suplementaire de viste start
    def destroy(self, request, pk=None):
        objet = Visite.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Visite.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Visite.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)
    # Methodes suplementaire de viste end


class NotationSet(viewsets.ModelViewSet):
    queryset = Notation.objects.filter(deleted=False)
    serializer_class = NotationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Methodes suplementaire de viste start
    def destroy(self, request, pk=None):
        objet = Notation.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Notation.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Notation.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)
    # Methodes suplementaire de viste end


class CommentSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.filter(deleted=False)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Methodes suplementaire de viste start
    def destroy(self, request, pk=None):
        objet = Commentaire.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Commentaire.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Commentaire.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)
    # Methodes suplementaire de viste end

# Post des biens et ses descritions(Images, Videos, Viste) end

# Poster des Articles (avec Images, Videos, Gifs) start

class ArticleSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(deleted=False)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Methodes suplementaire de viste start
    def destroy(self, request, pk=None):
        objet = Article.objects.get(pk=pk)
        try:
            # objet.deleted = True
            # objet.deleted_at = timezone.now()
            objet.suppress()
            objet.save()
            return Response({'status': 'Suppression faite'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def restore(self, request, pk=None):
        objet = Article.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.restore()
            objet.save()
            return Response({'status': 'Les données ont été restaurées avec succes'})
        except:
            return Response({'status': 'Erreur lors de la suppression'})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_deleted_list(self, request):
        objet = Article.objects.filter(deleted=True).order_by('-deleted_at')
        serializer = self.get_serializer(objet, many=True)
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def publier(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.publier()
            objet.save()
            return Response({'status': "L'article a ete publié avec succes"})
        except:
            return Response({'status': "Une Erreur est survenue lors de la publication"})
    
    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def annuler(self, request, pk=None):
        objet = Media.objects.get(pk=pk)
        try:
            # objet.deleted = False
            # objet.deleted_at = None
            objet.annuler()
            objet.save()
            return Response({'status': "Vous avez annuler la publication de cet article"})
        except:
            return Response({'status': "Erreur lors de l'annulation"})
    # Methodes suplementaire de viste end


# Post des Articles (avec Images, Videos, Gifs) end
