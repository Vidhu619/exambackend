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
from .models import  Choice

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
def QuestionsList(request):
    if request.method == 'GET':
        # Handle GET request to retrieve questions
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        questions_text = request.POST.get('questions', '')
        category_id = request.POST.get('category', '')
        mark_type = request.POST.get('mark_type', '')
        question_status = request.POST.get('question_status', '')
        time_limit = request.POST.get('time_limit', '')

        # Extract choices from the request
        choices_data = request.POST.getlist('choices, []')

        # Create a dictionary with the extracted data
        data = {
            'questions': questions_text,
            'category': category_id,
            'mark_type': mark_type,
            'question_status': question_status,
            'time_limit': time_limit,
            'choices': [{'choice_text': choice_text} for choice_text in choices_data],
        }

        serializer = QuestionsSerializer(data=data)

        if serializer.is_valid():
            new_question = serializer.save()

            # Create Choice objects and associate them with the question
            for choice_text in choices_data:
                choice = Choice.objects.create(choice_text=choice_text, question=new_question)
                choice.save()

            # Serialize the question along with its choices
            serialized_data = QuestionsSerializer(new_question).data

            return JsonResponse(serialized_data, status=201)

        return JsonResponse(serializer.errors, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
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
    questions=request.date.get('question')
    choice=request.data.get('choice')
    
