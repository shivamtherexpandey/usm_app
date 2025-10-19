from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from usm_user.serializers import AuthenticationRequestSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from usm_user.models import SubscriptionPlan, Subscription
from rest_framework.permissions import IsAuthenticated
from usm_user.serializers import UserDetailsSerializer
from rest_framework.generics import RetrieveAPIView

# Create your views here.
class SignupView(APIView):
    serializer_class = AuthenticationRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        # Set User model
        User = get_user_model()

        if User.objects.filter(email=validated_data['username'], is_active=True).exists():
            return Response({'error': 'An active user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Select Free Subscription Plan and create Subscription for User
        complementary_free_subscription = SubscriptionPlan.objects.get(id=1, is_active=True)
        subscription = Subscription.objects.create(plan=complementary_free_subscription, is_active=True)

        # Create User
        user_object = User(email=validated_data['username'], subscription=subscription)
        user_object.set_password(validated_data['password'])
        user_object.save()
        
        # Create JWT Token for the user
        access_token = AccessToken.for_user(user_object)

        response_content = {
            'access_token': str(access_token),
            'user_email': user_object.email,
            'msg': 'User created successfully'
        }
        return Response(response_content, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    serializer_class = AuthenticationRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        try:
            User = get_user_model()
            user_object = User.objects.get(email=validated_data['username'], is_active=True)
        except User.DoesNotExist:
            return Response({'error': 'No active user found with this email'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user_object.check_password(validated_data['password']):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Create JWT Token for the user
        access_token = AccessToken.for_user(user_object)

        response_content = {
            'access_token': str(access_token),
            'user_email': user_object.email,
            'msg': 'Login successful'
        }
        return Response(response_content, status=status.HTTP_200_OK)
    
class ProfileView(RetrieveAPIView):

    queryset = get_user_model().objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(id=self.request.user.id)