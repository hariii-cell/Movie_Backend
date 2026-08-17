from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Media
from .serializers import MediaSerializer


def home(request):
    """Render the home/interface page"""
    return render(request, 'index.html')


def seed_demo_media(user):
    samples = [
        {'title': 'Inception', 'type': Media.TYPE_MOVIE, 'status': Media.STATUS_UNWATCHED, 'rating': 0},
        {'title': 'The Crown', 'type': Media.TYPE_TV, 'status': Media.STATUS_WATCHED, 'rating': 5},
        {'title': 'Arrival', 'type': Media.TYPE_MOVIE, 'status': Media.STATUS_WATCHED, 'rating': 4},
        {'title': 'Dark', 'type': Media.TYPE_TV, 'status': Media.STATUS_UNWATCHED, 'rating': 0},
    ]

    for entry in samples:
        Media.objects.get_or_create(
            owner=user,
            title=entry['title'],
            defaults={
                'type': entry['type'],
                'status': entry['status'],
                'rating': entry['rating'],
            },
        )


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    if request.user.is_authenticated:
        return Response({'username': request.user.username})
    return Response({'username': None})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = (request.data.get('username') or '').strip()
    password = (request.data.get('password') or '').strip()

    if not username or not password:
        return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'This username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    if not Media.objects.filter(owner=user).exists():
        seed_demo_media(user)
    return Response({'username': user.username}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = (request.data.get('username') or '').strip()
    password = (request.data.get('password') or '').strip()

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    if not Media.objects.filter(owner=user).exists():
        seed_demo_media(user)
    return Response({'username': user.username})


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_user(request):
    logout(request)
    return Response({'detail': 'Logged out successfully.'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def media_list(request):
    owner = request.user

    if request.method == 'GET':
        items = Media.objects.filter(owner=owner).order_by('status', 'title')
        serializer = MediaSerializer(items, many=True)
        return Response(serializer.data)

    serializer = MediaSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save(owner=owner)
        return Response(MediaSerializer(item).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def media_detail(request, pk):
    owner = request.user
    item = Media.objects.filter(owner=owner, pk=pk).first()

    if item is None:
        return Response({'detail': 'Media item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = MediaSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
