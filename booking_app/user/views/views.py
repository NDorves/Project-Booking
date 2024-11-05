from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from booking_app.user.models.model import User
from booking_app.user.serializers.user_serializer import UserDetailSerializer, UserListSerializer, \
    RegisterUserSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserListGenericView(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        listings_title = self.request.query_params.get('listings_title')

        if listings_title:
            return User.objects.filter(listings__title=listings_title)

        return User.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        users = self.get_queryset()

        if not users.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.get_serializer(users, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class RegisterUserGenericView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

