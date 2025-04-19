from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Student, Candidate
from .serializers import StudentSerializer, CandidateSerializer
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterStudentView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new student or teacher",
        request_body=StudentSerializer,
        responses={
            201: openapi.Response("User registered successfully"),
            400: openapi.Response("Validation error"),
        },
    )
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginStudentView(APIView):
    @swagger_auto_schema(
        operation_description="Login a student and get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description="PRN of the student"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of the student"),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Response(
                "Login successful",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token"),
                        "access": openapi.Schema(type=openapi.TYPE_STRING, description="Access token"),
                    },
                ),
            ),
            401: openapi.Response("Invalid credentials"),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CandidateListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of candidates from the same class as the logged-in user",
        security=[{"Bearer": []}],  # Add this line for Bearer token
        responses={
            200: openapi.Response(
                description="List of candidates",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(type=openapi.TYPE_STRING, description="Candidate's name"),
                            "prn": openapi.Schema(type=openapi.TYPE_STRING, description="Candidate's PRN"),
                            "class_name": openapi.Schema(type=openapi.TYPE_STRING, description="Candidate's class"),
                            "votes": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of votes"),
                        },
                    ),
                ),
            ),
            401: openapi.Response(description="Unauthorized"),
        },
    )
    def get(self, request):
        user_class = request.user.class_name
        candidates = Candidate.objects.filter(class_name=user_class)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VolunteerCandidateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Volunteer as a candidate",
        security=[{"Bearer": []}],
        responses={
            201: openapi.Response("You have successfully volunteered as a candidate."),
            400: openapi.Response("Validation error or already registered as a candidate."),
        },
    )
    def post(self, request):
        user = request.user
        if Candidate.objects.filter(prn=user.username).exists():
            return Response({"error": "You are already registered as a candidate."}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "name": user.name,  
            "prn": user.username,
            "class_name": user.class_name,
        }
        serializer = CandidateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "You have successfully volunteered as a candidate."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username, 
            "name": user.name, 
            "class_name": user.class_name,
            "is_teacher": user.is_teacher
        }, status=status.HTTP_200_OK)
    

def index(request):
    return render(request, 'index.html')

# Static Index views
def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def test(request):
    return render(request, 'test.html')

def vote(request):
    return render(request, 'vote.html')

