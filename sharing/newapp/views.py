# views.py
import os
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, UploadedFile
from .serializers import UserProfileSerializer, UploadedFileSerializer
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import hashlib
import uuid
from django.core.mail import send_mail

@api_view(['POST'])
def ops_login(request):
    # Implementing Ops User login logic 
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate Ops User
    user = authenticate(request, username=username, password=password)

    if user is not None and user.is_staff:
        # Ops User is authenticated and is a staff member
        login(request, user)
        
        # Generate or retrieve token (for simplicity, you can use Django's built-in session ID)
        token = request.session.session_key

        # Update UserProfile to store the session key or generate a token for more security
        user_profile = UserProfile.objects.get(user=user)
        user_profile.token = token
        user_profile.save()

        # Return user information including the token
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid credentials or not authorized'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ops_upload(request):
    # Implement Ops User file upload logic here
    # Check if the user is an Ops User
    if not request.user.userprofile.ops_user:
        return Response({'error': 'Unauthorized'}, status=401)

    # Get the uploaded file and validate file type
    uploaded_file = request.FILES.get('file')
    allowed_file_types = ['pptx', 'docx', 'xlsx']
    
    if not uploaded_file:
        return Response({'error': 'No file uploaded'}, status=400)

    file_extension = os.path.splitext(uploaded_file.name)[1][1:]
    if file_extension not in allowed_file_types:
        return Response({'error': 'Invalid file type'}, status=400)

    # Save the file to the server
    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)

    # Save file information to the database
    uploaded_file_obj = UploadedFile(user=request.user, file=filename, file_type=file_extension)
    uploaded_file_obj.save()

    # Provide the download link to the Ops User
    serializer = UploadedFileSerializer(uploaded_file_obj)
    return Response(serializer.data, status=201)

@api_view(['POST'])
def client_signup(request):
    # Implementing Client User signup logic 
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Create user
    user = User.objects.create_user(username, email, password)
    user_profile = UserProfile.objects.create(user=user)

    # Generate verification code and URL
    verification_code = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    user_profile.verification_code = verification_code
    user_profile.save()

    verification_url = f"http://localhost:8000/verify-email/{verification_code}/"
    
    # Send verification email
    send_mail(
        'Verify Your Email',
        f'Click the following link to verify your email: {verification_url}',
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return Response({'message': 'Please check your email to verify your account.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_download(request, assignment_id):
    # Implementing Client User download logic 
    user = request.user
    uploaded_file = get_object_or_404(UploadedFile, id=assignment_id, user=user)

    # Check if the requesting user is the owner of the file
    if uploaded_file.user != user:
        return Response({'error': 'Unauthorized'}, status=403)

    # Generate a secure download link (in a real-world scenario, you might want to use a token-based system)
    download_link = f"/download-file/{assignment_id}/"

    # Update the UploadedFile model with the download link
    uploaded_file.download_link = download_link
    uploaded_file.save()

    return Response({'download_link': download_link, 'message': 'success'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_list_files(request):
    # Implementing Client User list files logic
    user = request.user

    # Get all files uploaded by the client user
    files = UploadedFile.objects.filter(user=user)

    # Serialize the files data
    serializer = UploadedFileSerializer(files, many=True)

    # Return the serialized data in the response
    return Response(serializer.data)