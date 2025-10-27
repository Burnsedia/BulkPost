from django.db import models

# Create your models here.
class post(models.Model):
   # add post class properties here
   post_title =  models.CharField(max_length = 20)
   post_content = models.TextField()
   post_date = modoels.DateTimeField(default= timezone.now)

   def __str__(self):
       return '<Name:{}, ID:{}'.format(self.name,self.id)


