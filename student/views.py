import statistics
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import ( HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT )
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Questions
from .serializers import QuestionsSerializer
from .models import Category
from .serializers import CategorySerializer
import json
from django.http import JsonResponse


# http://127.0.0.1:8000/student/register
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def Register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password1 = request.data.get('password1')

    if password != password1:
        return Response({'error': 'Confirmation Password is Wrong'}, status=HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username= username, email=email, password=password)
    user.save() 

    return Response({'Success': 'User Creation Successfully'}, status=HTTP_201_CREATED)



# http://127.0.0.1:8000/student/login
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
   
    user = authenticate (username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token':token.key},status=HTTP_200_OK)


# http://127.0.0.1:8000/student/logout
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Logout(request):
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
    return Response('You have successfully logged out.',status=HTTP_200_OK)






@csrf_exempt
@api_view(['GET'])
def Question_list(request):
        # Handle GET request to retrieve questions
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)

 
@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view


@api_view(['POST'])
def Question_list(request):
    questions = request.data.get('question')
    choice = request.data.get('choice')
    category_name = request.data.get('category')
    mark_type = request.data.get('mark_type')
    questions_status = request.data.get('status')
    time_limit = request.data.get('time_limit')

    if questions is not None and choice is not None and category_name is not None:
        try:
            category = Category.objects.get(category_name=category_name)
        except:
            return Response("Category does not exist")
        new_question = Questions.objects.create(
            questions=questions,
            choices=choice,
            category=category,
            mark_type=mark_type,
            question_status=questions_status,
            time_limit=time_limit
        )
        
        return Response("Question saved successfully")
        

    return Response("Incomplete data provided")
 