"""from djoser.views import TokenCreateView
from djoser.conf import settings
from .models import ChessGame
from .serializers import ChessGameSerializer
from rest_framework import mixins, viewsets

class MyTokenCreateView(TokenCreateView):

    def _action(self, serializer):

        response = super()._action(serializer)
        tokenString = response.data['auth_token']
        tokenObject = settings.TOKEN_MODEL.objects.get(key=tokenString)

        response.data['user_id'] = tokenObject.user.id
        response.data['rating'] = tokenObject.user.rating

        return response
    
class ChessGameViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = ChessGame.objects.all()
    serializer_class = ChessGameSerializer

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass
"""