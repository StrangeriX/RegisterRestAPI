from django.shortcuts import render
from rest_framework import generics, status, permissions
from authentication.serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate


class AuthUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return Response({'user': serializer.data})


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        user = authenticate(username=username, password=password)
        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials. Try again"}, status=status.HTTP_401_UNAUTHORIZED)
