from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task, CustomUser
from .serializers import TaskSerializer, RegistrationSerializer, LoginSerializer, GetataskSerializer, StatusSerializer
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


class SignupView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = RegistrationSerializer(data=data)
            if serializer.is_valid():
                if CustomUser.objects.filter(email=data['email']).exists():
                    context = {
                        'message': 'Email already exists'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                if CustomUser.objects.filter(username=data['username']).exists():
                    context = {
                        'message': 'User name already exists'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                if len(data['password']) < 7:
                    context = {
                        'message': 'Passwords must be greater or equal to 7'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

                if data['password'] != data['confirm_password']:
                    context = {
                        'message': 'Passwords do not match'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)


                user = CustomUser.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    username=data['username'].replace(" ", ""),
                    email=data['email'],
                    password=data['password'],  # Store the hashed password
                )
                user.set_password(data['password'])
                user.save()
                if user:
                    return Response({'message': 'User Registered Successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Failed to register user'}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            return Response({'message': f'{e} is required'}, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            user = CustomUser.objects.filter(username=username).first()

        if user is None:
            context = {
                'message': 'Please enter valid login details'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            context = {
                'message': 'Please enter valid login details'
            }

            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        token = get_tokens_for_user(user)
        response = Response(status=status.HTTP_200_OK)
        response.data = {
            'message': "Login Success",
            'token': token['access'],
            'refresh': token['refresh'],

        }
        return response


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsManager]


class TasklListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = GetataskSerializer


# @permission_classes([IsAuthenticated])
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = StatusSerializer


