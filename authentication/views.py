from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser

from rest_framework import generics
from .serializers import UserSerializer, LoginSerializer

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import authenticate
import jwt
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from rest_framework.authtoken.models import Token 


from rest_framework.decorators import api_view,permission_classes

from rest_framework.permissions import AllowAny

# Create your views here.


class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# for functional views
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    # data=JSONParser().parse(request)
    # serializer=LoginSerializer(data=request.data)
    username=request.data.get('username')
    password=request.data.get('password')
    if username is None or password is None:
        return Response({'error':'Please provide both username and password'},status=status.HTTP_400_BAD_REQUEST)

    user=authenticate(username=username,password=password)

    if not user :
        return Response({'error':'Invalid credentials'},status=status.HTTP_404_NOT_FOUND)

    # if serializer.is_valid():
    # serializer.save()
    token,_=Token.objects.get_or_create(user=user)
    return Response({'token':token.key},status=status.HTTP_200_OK)

    # return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# fro class based views
class LoginView(generics.CreateAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,_=Token.objects.get_or_create(user=user)
        return Response({'token':token.key},status=status.HTTP_200_OK)



class ApiRoot(APIView):

    def get(self,request):

        return Response({

            'register':reverse('register',request=request),
            'hello':reverse('hello',request=request),

            'login':reverse('login',request=request),


        })

