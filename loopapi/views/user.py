import sqlite3
import json
from datetime import datetime

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                email=serializer.validated_data["username"],
                is_staff=serializer.validate_data["is_staff"]
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def user_login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token = Token.objects.get(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


    def login_user(user):
        """Checks for the user in the database

        Args:
            user (dict): Contains the username and password of the user trying to login

        Returns:
            json string: If the user was found will return valid boolean of True and the user's id as the token
                        If the user was not found will return valid boolean False
        """
        with sqlite3.connect('./db.sqlite3') as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                select id, username
                from Users
                where username = ?
                and password = ?
            """, (user['username'], user['password']))

            user_from_db = db_cursor.fetchone()

            if user_from_db is not None:
                response = {
                    'valid': True,
                    'token': user_from_db['id']
                }
            else:
                response = {
                    'valid': False
                }

            return json.dumps(response)


# def create_user(user):
#     """Adds a user to the database when they register

#     Args:
#         user (dictionary): The dictionary passed to the register post request

#     Returns:
#         json string: Contains the token of the newly created user
#     """
#     with sqlite3.connect('./db.sqlite3') as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         db_cursor.execute("""
#         Insert into Users (first_name, last_name, username, email, password, is_staff) values (?, ?, ?, ?, ?, true)
#         """, (
#             user['first_name'],
#             user['last_name'],
#             user['username'],
#             user['email'],
#             user['password'],
#             user['is_staff'],
#         ))

#         id = db_cursor.lastrowid

#         return json.dumps({
#             'token': id,
#             'valid': True
#         })
        
        
    @action(detail=False, methods=["post"], url_path="register")
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                email=serializer.validated_data["username"],  # Ensure you intended to use username for email
                is_staff=serializer.validated_data["is_staff"]  # Use validated_data instead of validate_data
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
