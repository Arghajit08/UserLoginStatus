import email
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MainUser
import jwt
from .serializers import UserSerializers
import datetime
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login, authenticate
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from drf_yasg import openapi

class UserProfile(APIView):
    token_param_config = openapi.Parameter('token', openapi.IN_QUERY, description="Bearer Token", type=openapi.TYPE_STRING)
    phoneno_param_config=openapi.Parameter('phoneno',openapi.IN_QUERY,description="Phone Number",type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config,phoneno_param_config])
    def get(self,request):
        serializer_class = UserSerializers

        token = request.GET.get('token')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')
        if payload['phoneno'] == 9863103113:
            if request.GET['phoneno']!='1':
                user=MainUser.objects.filter(phoneno=request.GET['phoneno']).first()
                user.user_locked=False
                user.save()
                return Response({'message':'User Unlocked'})
            else:
                user = MainUser.objects.all()
                serializer = UserSerializers(user,many=True)
                return Response(serializer.data)
        else:
            return Response('You are not authorized to view this page')
    
    # token_param_config = openapi.Parameter('token', openapi.IN_QUERY, description="Bearer Token", type=openapi.TYPE_STRING)
    phoneno_param_config=openapi.Parameter('phoneno',openapi.IN_QUERY,description="Phone Number",type=openapi.TYPE_STRING)
    password_param_config=openapi.Parameter('password',openapi.IN_QUERY,description="Password",type=openapi.TYPE_STRING)
    email_param_config=openapi.Parameter('email',openapi.IN_QUERY,description="Email",type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[phoneno_param_config,password_param_config,email_param_config])
    def post(self, request):
        phoneno = request.GET['phoneno']
        password = request.GET['password']

        user = MainUser.objects.filter(phoneno=phoneno).first()
        if user is None:
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        user = MainUser.objects.filter(phoneno=phoneno).first()

        payload = {
            'id': user.id,
            'password': user.password,
            'phoneno': user.phoneno,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        time = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        
        response.data = {
            'jwt': token,
            'time': time
        }
        user.save()

        return response

class UserLogin(APIView):
    
    token_param_config = openapi.Parameter('token', openapi.IN_QUERY, description="Bearer Token", type=openapi.TYPE_STRING)
    password_param_config=openapi.Parameter('password',openapi.IN_QUERY,description="Password",type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config,password_param_config])
    def post(self,request):
        token = request.GET.get('token')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()

        user = MainUser.objects.filter(phoneno=payload['phoneno']).first()
        if user.user_locked:
            raise AuthenticationFailed('User locked!')
        else:
            print(user.password)
            print(request.GET['password'])
            if user.password == request.GET['password']:
                user.user_loggedin = True
                user.user_failedlogin = 0
                user.save()
                response.data = {
                    'message': 'Logged in successfully'
                }
            else:
                user.user_failedlogin += 1
                user.save()
                response.data = {
                    'message': 'Logged in failed'
                }
                if user.user_failedlogin == 3:
                    user.user_locked = True
                    user.save()
                    response.data = {
                    'message': 'User Locked in'
                    }
        return response

class UserLogout(APIView):

    token_param_config = openapi.Parameter('token', openapi.IN_QUERY, description="Bearer Token", type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()

        user = MainUser.objects.filter(phoneno=payload['phoneno']).first()
        if user.user_locked:
            raise AuthenticationFailed('User locked!')
        else:
            if user.user_loggedin == True:
                user.user_loggedin = False
                user.user_failedlogin = 0
                user.user_locked = False
                user.user_loggedout = True
                user.save()
                response.data = {
                    'message': 'Logged out successfully'
                }
            else:
                response.data = {
                    'message': 'Logged out failed'
                }

        return response


# Create your views here
