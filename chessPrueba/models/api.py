from djoser.views import TokenCreateView
from djoser.conf import settings



class MyTokenCreateView(TokenCreateView):

    def _action(self, serializer):
        response = super()._action(serializer)
        tokenString = response.data['auth_token']
        tokenObject = settings.TOKEN_MODEL.objects.get(key=tokenString)

        response.data['user_id'] = tokenObject.user.id 
        response.data['rating'] = tokenObject.user.rating
        return response