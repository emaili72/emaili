from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status,viewsets
from rest_framework.permissions import IsAdminUser 
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import *



# Регистрация аккаунта 
class RegisterAPIView(APIView):
   @swagger_auto_schema(request_body=RegisterSerializer())
   def post(self, request):
      print('DATA', request.data)
      serializer = RegisterSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response('To complete registration, follow the link sent', status=201)
        
# активация кода
@api_view(['GET'])
def activate_view(request, activation_code):
   user = get_object_or_404(User, activation_code=activation_code)
   user.is_active = True # activate user
   user.activation_code = '' # delete the activated code
   user.save()
   return Response('Succesfuly activated the account', status=200)

class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [IsAdminUser,]
   
   def get_serializer_context(self):
      return {'request':self.request}

class LogoutView(APIView):
   permission_classes = [IsAuthenticated, ]

   def post(self, request):
      print(request.data)
      user = request.user
      Token.objects.filter(user=user).delete()
      return Response('Succesfully logged out', status=201)
   
   # Если это видишь то значит все работает