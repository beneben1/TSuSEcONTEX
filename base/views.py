from django.http import JsonResponse
from .models import Orders, Product
from .Serializer import CartItemSerializer, OrderSerializer, ProductSerializer
from .Serializer import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)})

        return Response({'error': 'Invalid credentials'}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.data['message'] = 'Login successful.'
        else:
            response.data['message'] = 'Invalid login credentials.'
        return response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    # Perform validation on the input data
    if not username or not password or not email:
        return Response({'error': 'Please provide all the required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username or email already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email address already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = User.objects.create_user(
        username=username, password=password, email=email)

    # You can perform additional actions here, such as sending a welcome email

    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getNotes(request):
    return ("protected")


def index(req):
    return JsonResponse('hello', safe=False)


def myProducts(req):
    all_products = ProductSerializer(Product.objects.all(), many=True).data
    return JsonResponse(all_products, safe=False)


class ProductViewSet(APIView):
    def get(self, request):
        my_model = Product.objects.all()
        serializer = ProductSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        my_model = Product.objects.get(pk=pk)
        serializer = ProductSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        my_model = Product.objects.get(pk=pk)
        my_model.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------Oreders handel-------------------------


class OrderViewSet(APIView):
    def get(self, request):
        my_model = Orders.objects.all()
        serializer = OrderSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        my_model = Orders.objects.get(pk=pk)
        serializer = OrderSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        my_model = Orders.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------------get images handel -----------------------------------
# return all images to client (without serialize)


@api_view(['GET'])
def getImages(request):
    res = []  # create an empty list
    for img in Product.objects.all():  # run on every row in the table...
        res.append({

            "image": str(img.image)
        })  # append row by to row to res list
    return Response(res)  # return array as json response


# upload image method (with serialize)
class APIViews(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        api_serializer = ProductSerializer(data=request.data)

        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', api_serializer.errors)
            return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# <--------------------------------------------------- Cart Entry Points ------------------------------------------->
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart_items = request.data
        print(cart_items)
        serializer = CartItemSerializer(data=request.data,  context={'user': request.user},many=True)
        if serializer.is_valid():
            cart_items = serializer.save()
        #     # Process the cart items as needed
        #     # ...
            return Response("Cart items received and processed successfully.")
        else:
            return Response(serializer.errors, status=400)
    def get(self, request):
        user= request.user
        my_model = user.orders_set.all()
        serializer = OrderSerializer(my_model, many=True)
        return Response(serializer.data)    
