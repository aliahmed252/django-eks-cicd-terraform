from rest_framework import serializers
from .models import Meal,Rating
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password']
        extra_kwargs={'password':{'write_only':True,'required':True}}# to hide the password on the postman must to be hide for the secure
        #(username still appear in the postman)
      

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model=Meal
        fields=['id','title','description','no_of_ratings','avg_rating']
        
class RatingSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields=['id','stars','user','meal']