from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator 
# import uuid
"""we use MinValueValidator to specfiy that the rate start
from 1 and use MaxValueValidator prevent the user from rating the male <5 the max rate is=5"""

class Meal(models.Model):
    # id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title=models.CharField(max_length=32)
    description=models.CharField(max_length=360)
    def no_of_ratings(self):#to get number of ratings
        ratings=Rating.objects.filter(meal=self)
        return len(ratings)
    
    def avg_rating(self):#to get the average of ratings
        sum=0
        ratings=Rating.objects.filter(meal=self)
        for x in ratings:
            sum += x.stars
        if len(ratings)>0:
            return sum/len(ratings)
        else:
            return 0
            
    def __str__(self):
        return self.title
        
class Rating(models.Model):
    meal=models.ForeignKey(Meal,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    stars=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    # def __str__(self):
    #     return self.meal
    
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user', 'meal'], name='unique_user_meal')]
        # constraints: means that (user, meal) must be unique in the table
        # it means the same user cannot choose the same meal twice

        indexes = [
        models.Index(fields=['user', 'meal'])
        ]
        # we use index to facilitate the process of searching when the table contains a lot of data
        # search would look like: FavoriteMeal.objects.filter(user=ali, meal=pizza)