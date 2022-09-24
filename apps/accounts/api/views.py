from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.hashers import make_password
from twilio.rest import Client

User = get_user_model()


class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        email = data['email']
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']
        password2 = data['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                return Response({'error': "Email already exists."})
            if len(password) < 8:
                return Response({'error': "Password must be at least 8 characters"})

            User.objects.create(
                email=email,
                password=make_password(password),
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            return Response({'success': "User created successfully"})
        return Response({'error': "Passwords do not match."})
