from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .serializers import TaskSerializer, UserSerializer,UserResponseSerializer
from .models import Task, User

class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_tasks = Task.objects.filter(is_deleted=False,user=request.user).order_by('-created_at')
            serializer = TaskSerializer(user_tasks, many=True)
            return Response({
                "status": 200,
                "message": "Your tasks",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 500,
                "message": "An error occurred while fetching tasks.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            data = request.data.copy()
            data['user'] = user.id
            serializer = TaskSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 201,
                    "message": "Task created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                "status": 400,
                "message": "Task creation failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": 500,
                "message": "An error occurred while creating the task.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, task_id):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            task = get_object_or_404(Task, id=task_id)
            serializer = TaskSerializer(instance=task, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "Task updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "status": 400,
                "message": "Task update failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": 500,
                "message": "An error occurred while updating the task.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, task_id):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            task = get_object_or_404(Task, id=task_id)
            task.is_deleted = True
            task.save()
            
            serializer = TaskSerializer(task)
            return Response({
                "status": 200,
                "message": "Task deleted successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": 500,
                "message": "An error occurred while deleting the task.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OtherUserTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            other_user_tasks = Task.objects.filter(is_deleted=False).exclude(user=request.user)
            serializer = TaskSerializer(other_user_tasks, many=True)
            response_data = serializer.data
            for task in response_data:
                task['user'] = UserResponseSerializer(User.objects.get(id=task['user'])).data
            
            return Response({
                "status": 200,
                "message": "Other user tasks",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 500,
                "message": f"An error occurred while fetching tasks for other users.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignupLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')

        try:
            user = User.objects.get(email=email)
            # User exists, proceed with login
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status": 200,
                    "message": "Logged in successfully",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": 401,
                    "message": "Invalid credentials"
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        except User.DoesNotExist:
            # User does not exist, proceed with signup
            if not name:
                return Response({
                    "status": 400,
                    "message": "Name is required for signup"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "status": 201,
                        "message": "Signed up and logged in successfully",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token)
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        "status": 400,
                        "message": "Signup failed",
                        "errors": serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    "status": 500,
                    "message": "An error occurred during signup.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
