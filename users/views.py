from django.shortcuts import render
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User,  NEW, CODE_VERIFIED
from .serializers import UserSerializers, UserChangeInformationSerializers, ChangeUserPhotoSerializers, LoginSerializers
from rest_framework import generics, permissions
from django.utils.datetime_safe import datetime
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from . models import User, UserConfirmation, VIA_EMAIL, VIA_PHONE
from shared.utils import check_email_or_phone, send_email, send_phone


# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class VerifyApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')


        self.check_verify(user, code)

        return  Response(
            data = {
                "success":True,
                "auth_status": user.auth_status,
                "access":user.token()['access'],
                "refresh":user.token()['refresh_token']
            }
        )
    @staticmethod
    def check_verify(user, code):
        verifies = user.verifycode.filter(expiration__gte=datetime.now(),code=code, is_confirmed=False)

        if not verifies.exists():
            data = {
                "message": "tasdiqlash codi xato yoki vaxti tugagan"
            }
            raise  ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()

        return True

class GetNewVerifyCode(APIView):
    permissions_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verify()


        if user.auth_type == VIA_EMAIL:
             code = user.create_verify_code(VIA_EMAIL)
             send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
             code = user.create_verify_code(VIA_PHONE)
             send_phone(user.phone_number, code)

    @staticmethod
    def check_verify(user):
        verifies = user.verifycode.filter(expiration__gte=datetime.now(), is_confirmed=False)

        if verifies.exists():
            data = {
                "message": "Sizni kodinzgiz bilan hali tasdiqlash mumkin"
            }
            raise ValidationError(data)

class UserChangeInformation(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserChangeInformationSerializers
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(UserChangeInformation, self).update(request, *args, **kwargs)

        data = {
            "message": "User Muvaffaqiyatli yangilandi",

            "auth_status": self.request.user.auth_status,
        }

        return Response(data)

class ChangeUserPhoto(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated,]

    def put(self, request, *args, **kwargs):
        serializers = ChangeUserPhotoSerializers(data=request.data)

        if serializers.is_valid():
            user = request.user
            serializers.update(user, serializers.validated_data)

            return Response(
                {
                    "message": "Rasm o'rnatildi"
                }
            )
        return Response(
                serializers.errors, status=400
        )

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializers