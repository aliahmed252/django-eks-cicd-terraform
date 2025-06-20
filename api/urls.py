from django.urls import path,include

from rest_framework import routers
from .views import MealViewset,Ratingviewset,UserViewset


router=routers.DefaultRouter()
router.register('meals',MealViewset)
router.register('ratings',Ratingviewset)
router.register('user',UserViewset)#url to create a new user on postman
urlpatterns = [
    path('',include(router.urls)),
]
