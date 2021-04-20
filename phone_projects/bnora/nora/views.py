from django.shortcuts import render, get_object_or_404

from django import template, forms

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Categories, Product, Star, UserProfile
# Create your views
def index(request):
	
	categories = Categories.objects.all()
	context = { 'categories': categories }
	return render(request, 'index.html', context )
	
def product(request, name):
	products = Product.objects.filter(category__name=name).exclude(qty=0).all()
	context = { 'products' : products }
	return render(request, 'product.html', context)
	
def item(request, id):
	if request.method == 'POST':
		if request.POST['qty']:
			qty = request.POST['qty']
		return HttpResponse(qty)
	item = get_object_or_404(Product, id=id)
	
	star = Star.objects.filter(pk=1).first()
	rating = int(item.rated/item.ratees )
	max_order = []
	qty = []
	for i in range(1, item.max_order+1):
		max_order.append(i)
	for j in range(1, item.qty+1):
		qty.append(j)
	#return HttpResponse(max_order)
	context = {
	'item': item, 'star': star, 'rating': rating, 
	'qty': qty, 'max_order': max_order}
	
	return render(request, 'item.html', context)
	
def cart(request):
	if request.method == 'POST':
		items = []
		cartItems = eval(request.POST['cartItems'])
		for item in cartItems:
			productid = int(item['productid'])
			product = Product.objects.filter(pk=productid).first()
			
			qty_ordered = int(item['qty'])
			qty_available = int(product.qty)
			max_qty = int(product.max_order)
			available = True
			
			if qty_available > max_qty:
				qty_available = max_qty
			
			elif qty_available < max_qty:
				qty_available = qty_available
			
			if qty_ordered > qty_available:
				available = False
			
			available_for_sale = []
			for i in range(1, int(qty_available)+1):
				available_for_sale.append(i)
				
			cartItem = {
				'id': productid,
				'idAgain': productid,
				'name': product.name,
				'color': item['color'],
				'size': item['size'],
				'price': str(product.price),
				'image_url' : product.image.url,
				'orderQty': item['qty'],
				'qty_available': str(available_for_sale),
				'available': available,
				'is_available': item['is_available']
			}
			items.append(cartItem)
		return JsonResponse({'items':  items })
		
	return render(request, 'cart.html')

#user forms
class UserEdit(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'email']
		
class ProfileEdit(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['name', 'address', 'phone']
		
class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Retype password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['first_name', 'email', 'username']
		
	def verify_password(self):
		password1 = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		
		if password1 != password2:
			raise form.validationError("passwords don't match")
		elif len(password1) < 6:
			raise form.validationError('password must be at least six characters long')
			
		return self.cleaned_data['password2']
	
	
def register(request):
	registered = False
	user_form =  UserRegistrationForm()
	if request.method == 'POST':
		user_form =  UserRegistrationForm(request.POST)
		
		
		if user_form.is_valid():
			password = user_form.cleaned_data['password']
			
			save_user = user_form.save(commit=False)
			save_user.set_password(password)
			save_user.save()
			
			UserProfile.objects.create(user=save_user)
			registered= True
			
			return render(request, 'register.html', {
					'registered': registered, 'new_user': save_user
			})
		else:
			return render(request, 'register.html', {
					'registered': registered, 'user_form': user_form, 'error_msg':
						 'Passwords must be at least six characters long, and be the same'
			})
	else:
		return render(request, 'register.html', {
					'registered': registered, 'user_form': user_form
			})
	
	

@login_required
def address(request):
	
	userEditForm = UserEdit(instance=request.user)
	profileEditForm = ProfileEdit(instance=request.user.profile)
	
	
	
	return render(request, 'profile.html', {
		'userEdit' : userEditForm,
		'profileEdit' : profileEditForm
	})
 

def payment(request):
    if request.method == 'POST':
        userEditForm = UserEdit(instance=request.user, data=request.POST)
        profileEditForm = ProfileEdit(instance=request.user.profile, data=request.POST)
        
        if userEditForm.is_valid() and profileEditForm.is_valid():
            userEditForm.save()
            profileEditForm.save()
            deliveryMethod = request.POST['deliveryMethod']
            cartItemDetails = eval(request.POST['cartItemDetails'])

        return HttpResponse(f'{cartItemDetails[0]["color"]}')
	
		
        
    return HttpResponse('Hello world') 
	
	