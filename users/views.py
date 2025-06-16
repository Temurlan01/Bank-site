from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer


class UserRegisterAPIView(APIView):
    """Вью для регистрации"""
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(status=201, data={"token": token.key})



class UserLoginAPIView(APIView):
    """Вью для логина"""
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return Response(status=404, data={'message': 'Пользователь не найден'})

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response(status=400, data={'message': 'Неверный пароль'})
