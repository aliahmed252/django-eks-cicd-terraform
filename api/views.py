from django.shortcuts import render
from rest_framework import viewsets,status
from .models import Meal ,Rating
from .serializers import MealSerializer,RatingSerailizer,UserSerializer
from rest_framework.decorators import action

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserViewset(viewsets.ModelViewSet):# to make a new user from the url on postman
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    authentication_classes=(TokenAuthentication,)
    permission_classes=(AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token,created=Token.objects.get_or_create(user=serializer.instance)
        return Response({
            'token':token.key,
            },
                        status=status.HTTP_201_CREATED)
    # def list(self,request,*args,**kwargs):
    #     if not request.user.is_superuser:#specfiy who can get the data here the onlY one is superuser(admin) 
    #         #if i want all users can access to data i will change (user.is_superuser) to (user.is_staff)
    #         response={'message':'you cannot create rating like that'}
    #         return Response(response,status=status.HTTP_403_FORBIDDEN)
    #     queryset=self.get_queryset()
    #     serializer=self.get_serializer(queryset,many=True)
    #     return Response(serializer.data)
    
    #i hashed all the above lines becaues i give the in the next func to get onlY his data the last func not allowed the users to do that
    def retrieve(self, request, *args, **kwargs):#in status the user have the right to see only himself
        user = self.get_object()
        if request.user != user:
            return Response({"error": "You can't view other users' profiles"}, status=403)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Only admin can delete users"}, status=403)
        return super().destroy(request, *args, **kwargs)
       
class MealViewset(viewsets.ModelViewSet):
    queryset=Meal.objects.all()
    serializer_class=MealSerializer
    
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)#(IsAuthenticated) to access the API must has token mean register by (username and password)
    
    @action(detail=True,methods=['post'],url_path='rate_meal')
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            meal=Meal.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user
            print(user)
            # username=request.data['username']
            # user=User.objects.get(username=username)
            
            try:#check if the pk existed (mean that the pk is can update)
                #update
                rating=Rating.objects.get(user=user,meal=meal)#specific rate
                rating.stars=stars
                rating.save()
                serializer=RatingSerailizer(rating,many=False)
                json={
                    'message':'meal rate updated',
                    'result':serializer.data
                }
                return Response(json,status=status.HTTP_400_BAD_REQUEST)
            except:#except will work when the pk not found it wILL created the pk there is no rating
                #create
                rating=Rating.objects.create(stars=stars,meal=meal,user=user)
                serializer=RatingSerailizer(rating,many=False)
                json={
                    'message':'meal rate created',
                    'result':serializer.data
                }
                return Response(json,status=status.HTTP_200_OK)
                
        else:
            json={
                'message':'stars not provided'
            }   
            return Response(json,status=status.HTTP_400_BAD_REQUEST)
        
    
class Ratingviewset(viewsets.ModelViewSet):
    queryset=Rating.objects.all()
    serializer_class=RatingSerailizer
    
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)#(IsAuthenticated) to access the API must has token mean register by (username and password)
    
    def update(self, request, *args, **kwargs):#to prevent the registered user to update the rating
        response={
            "message":"invalid way to create or update"
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):#to prevent the registered user to create the rating
        response={
            "message":"invalid way to create or update"
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)
    