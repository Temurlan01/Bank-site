from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer

class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(status=201, data={"token": token.key}, )
        return Response(serializer.errors, status=400)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                return Response(status=400, data={'message': 'Пользователь не найден'}, )
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response(status=400, data={'message': 'Неверный пароль'}, )
        return Response(serializer.errors, status=400)