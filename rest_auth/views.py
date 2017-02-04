from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail

from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status

from .models import PasswordRecovery
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST'],)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):

    class TempSerializer(serializers.Serializer):

        @staticmethod
        def is_user(password):
            if(authenticate(username=request.user.username, password=password) is None):
                raise serializers.ValidationError('Invalid credentials')

        old_password = serializers.CharField(validators=[is_user.__func__])
        new_password = serializers.CharField(min_length=8)

    serializer = TempSerializer(data=request.data)

    if(serializer.is_valid()):
        data = serializer.validated_data
        request.user.set_password(data['new_password'])
        request.user.save()
        return Response()
    return Response(data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password(request):

    class TempSerializer(serializers.Serializer):
        username = serializers.CharField()

    serializer = TempSerializer(data=request.data)
    if(serializer.is_valid()):
        data = serializer.validated_data
        try:
            user = get_user_model().objects.get(username=data['username'])
            ps = PasswordRecovery(user=user)
            token = ps.generate_token()
            send_mail('Password Recovery for {}'.format(user.username),
                      'Hi!\nYour Password Recovery Token is: {}'.format(token),
                      recipient_list=[user.email],
                      from_email='someone@something.com',
                      fail_silently=True)
        except ObjectDoesNotExist as e:
            pass
        return Response()
    return Response(data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password_done(request):

    class TempSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(min_length=8)
        token = serializers.CharField()

    serializer = TempSerializer(data=request.data)
    if(serializer.is_valid()):
        data = serializer.validated_data
        try:
            user = get_user_model().objects.get(username=data['username'])
            pr = user.passwordrecovery
            if((user.passwordrecovery.match(data['token']))):
                user.set_password(data['password'])
                user.save()
                return Response()
        except ObjectDoesNotExist:
            pass
        serializer.errors['token'] = 'Your token is expired or invalid.'
    return Response(data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
