from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.views import ObtainAuthToken


from main.serializers import TodoSerialiser
from .models import Todo, User
# from .serializers import UserSerializers





class TodoApiView(APIView):
    serializer_class = TodoSerialiser
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated] 


    def get(self, request):
        works = Todo.objects.all()

        description = request.GET.get("description", None)
        is_active = request.GET.get("is_active", None)

        if description:
            description = works.filter(description__contains=description)
        
        if is_active:
            is_active = works.filter(is_active__contains=is_active)
        
        work_serialized = TodoSerialiser(works, many=True)
        return Response(work_serialized.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        work_serialized = TodoSerialiser(data=request.data)

        if work_serialized.is_valid():
            work_serialized.save()
            return Response({"Ish":"Saqlandi"}, status=status.HTTP_201_CREATED)
        
        return Response(work_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        

class SingleTodoApiView(APIView):
    serializer_class = TodoSerialiser

    def get(self, request, pk=None):
        work = Todo.objects.get(id=pk)
        work_serialized = TodoSerialiser(work, many=False)

        return Response(work_serialized.data, status=status.HTTP_200_OK)

    
    def put(self, request, pk=None):
        work = Todo.objects.get(id=pk)
        work_serialized = TodoSerialiser(instance=work, data=request.data)
        if work_serialized.is_valid():
            work_serialized.save()
            return Response({"post":"O'zgartirildi"}, status=status.HTTP_202_ACCEPTED)

        return Response(work_serialized.errors, status = status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk=None):
        work = Todo.objects.get(id=pk)
        work_serialized = TodoSerialiser(instance=work, data=request.data, partial=True)
        if work_serialized.is_valid():
            work_serialized.save()
            return Response({"post":"O'zgartirildi"}, status=status.HTTP_202_ACCEPTED)
        return Response(work_serialized.errors, status = status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        news = Todo.objects.get(id=pk)
        news_serialized = TodoSerialiser(news, many=False)
        data = news_serialized.data
        news.delete()

        return Response(data, status=status.HTTP_204_NO_CONTENT)

User = get_user_model()

class UserApiView(ObtainAuthToken):
    # serializer_class = UserSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request':request})
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = User.objects.filter(username=username)

            if user.exists():
                user = user.first()
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        "token":token.key,
                        "username":username,
                        "password":password,
                        "fullname":user.fullname
                    })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
        

