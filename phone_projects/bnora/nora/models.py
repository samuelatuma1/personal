from django.db import models
from django.conf import settings

# Create your models here.
class Categories(models.Model):
	name = models.CharField(max_length=40)
	image = models.ImageField(upload_to='categories/', blank=True, null=True)
	
	def __str__(self):
		return self.name
		
class Product(models.Model):
	category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products')
	name = models.CharField(max_length=200)
	image = models.ImageField(upload_to='products/images', blank=True, null=True)
	
	price=models.IntegerField()
	qty = models.IntegerField(default=1)
	uploaded = models.DateTimeField(auto_now_add=True)
	
	desc = models.TextField()
	
	img1 = models.ImageField(upload_to='description/', blank=True)
	img2 = models.ImageField(upload_to='description/', blank=True)
	img3 = models.ImageField(upload_to='description/', blank=True)
	
	color1 = models.CharField(max_length=30, blank=True)
	color2 = models.CharField(max_length=30, blank=True)
	color3 = models.CharField(max_length=30, blank=True)
	
	size1 = models.CharField(max_length=30, blank=True)
	size2 = models.CharField(max_length=30, blank=True)
	size3 = models.CharField(max_length=30, blank=True)
	max_order = models.IntegerField(default=2)
	
	rated = models.IntegerField(default=5)
	ratees = models.IntegerField(default=1)
	
	def __str__(self):
		return f'{self.name} from {self.category} category'

class Star(models.Model):
	star = models.ImageField(upload_to='staronly/')
	
	
	
class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	name = models.CharField(max_length=60, blank=True, null=True)
	address = models.TextField(blank=True, null=True)
	phone = models.IntegerField(blank=True, null=True)
	
 
class Counter(request):
    