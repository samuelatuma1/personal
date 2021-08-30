from django.shortcuts import render, get_object_or_404

from django import template, forms

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Categories, Product, Star, UserProfile, Desk
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
 
import random
import datetime
from datetime import timedelta
@login_required
def payment(request):
    if request.method == 'POST':
        userEditForm = UserEdit(instance=request.user, data=request.POST)
        profileEditForm = ProfileEdit(instance=request.user.profile, data=request.POST)
        
        if userEditForm.is_valid() and profileEditForm.is_valid():
            userEditForm.save()
            profileEditForm.save()
            
            deliveryMethod = request.POST['deliveryMethod']
            cartItemDetails = eval(request.POST['cartItemDetails'])
            paymentMethod = request.POST['paymentMethod']
            transaction_id = str(request.user) + str(random.randrange(100000000000, 999999999999))
            deliveryAddress = request.POST['address']
            phone = request.POST['phone']
            deliveryDate = datetime.datetime.now() + timedelta(days=2)
            
            purchase = Desk(name=request.user, deliveryMethod=deliveryMethod,
                          cartItemDetails=cartItemDetails, transaction_id=transaction_id,
            	          deliveryDate=deliveryDate, phone=phone, deliveryAddress=deliveryAddress, paymentMethod=paymentMethod)
            purchase.save()
            recent_purchase = Desk.objects.filter(name=request.user).order_by('-deliveryDate').first()
            products_purchased = eval(recent_purchase.cartItemDetails)
            index = 0
            total_cost = 0
            product_purchase = []
            for product in products_purchased:
                productid = int(product['productid'])
                product = Product.objects.filter(pk=productid).first()
                color = products_purchased[index]['color']
                if color == 'empty':
                    color = ''
                else:
                    color = color
                
                size = products_purchased[index]['size']
                if size == 'empty':
                    size = ''
                else:
                    size = size
                
                
                
                about_prod = {
					'name': product.name,
					'price': product.price,
					'qty': products_purchased[index]['qty'],
					'color': color,
					'size': size
				}
                total_cost += (int(products_purchased[index]['qty']) * int(product.price))
                product_purchase.append(about_prod)
                index += 1
                          
            return render(request, 'order_summary.html', {'recent_purchase' : recent_purchase,
                                                      'product_purchases': product_purchase, 'total_cost': total_cost})

        
from django.core.mail import send_mail        
@login_required  
def order_placed(request):
    recent_purchase = Desk.objects.filter(name=request.user).order_by('-deliveryDate').first()
    recent_purchase.order_placed = True
    recent_purchase.save()
    
    #total cost, reduce quantity available to reflect purchase
    products_purchased = eval(recent_purchase.cartItemDetails)
    total_cost = 0
    index = 0
    for product in products_purchased:
        productid = int(product['productid'])
        product = Product.objects.filter(pk=productid).first()
        product.qty -= int(products_purchased[index]['qty'])
        product.save()
        total_cost += (int(products_purchased[index]['qty']) * int(product.price))
        index += 1

    # Delete all unplaced orders
    
    Desk.objects.filter(name=request.user).filter(order_placed=False).order_by('-deliveryDate').all().delete()
    send_mail(f"Your B'nora Order {recent_purchase.transaction_id} has been confirmed",
           f"Dear {recent_purchase.name.username}, \n Thank you for shopping on B'nora.\
           Your order {recent_purchase.transaction_id} has successfully been confirmed\n. \
        	it will be packaged and shipped to you as soon as possible.\
            Thank you for shopping with B'nora {[(Product.objects.get(pk=product['productid']).name, Product.objects.get(pk=product['productid']).price, product['qty']+' unit',  ' size: '+ product['size'], ' color: '+ product['color']) for product in eval(recent_purchase.cartItemDetails)]},'Total Cost: '+ {total_cost}",
           'atumasaake@gmail.com', [f'{recent_purchase.name.email}'])
    
    #send mail to admin
    title = f"{recent_purchase.name.username}'s order is pending approval "
    
    message = f"{[(Product.objects.get(pk=product['productid']).name, Product.objects.get(pk=product['productid']).price, product['qty']+' unit','color: ' + product['size'], ' color: '+ product['color']) for product in eval(recent_purchase.cartItemDetails)]}, Total: ${total_cost}"
    
    send_mail(title, message, 'atumasaake@gmail.com', ['atumasaake@gmail.com'])
    return render(request, 'order_placed.html', {'recent_purchase' : recent_purchase,})

@login_required
def track_orders(request):
    order_placed = Desk.objects.filter(name=request.user).filter(order_stage='Order placed').order_by('-deliveryDate').all()  
    processing = Desk.objects.filter(name=request.user).filter(order_stage='Processing').order_by('-deliveryDate').all()
    delivered =  Desk.objects.filter(name=request.user).filter(order_stage='Delivered').order_by('-deliveryDate').all()
    
    return render(request, 'track_orders.html', {'order_placed': order_placed, 'processing': processing, 'delivered': delivered})

	