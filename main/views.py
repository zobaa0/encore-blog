from django.shortcuts import render, redirect
from .models import Product, Article, Tag
from django.core.paginator import Paginator
from .forms import NewUserForm, UserForm, ProfileForm, VoteForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def homepage(request):
	if request.method == 'POST':
		product_id = request.POST.get('product_pk')
		product = Product.objects.get('product_id')
		request.user.profile.products.add(product)
		messages.success(request, (f'{product} added to wishlist.'))
		return redirect('main:homepage')
	product = Product.objects.all()[:4]
	new_posts = Article.objects.all()[:4]
	featured = Article.objects.filter(article_tags__tag_name='Featured')[:3]
	most_recent = new_posts.first()
	context = {
			'product': product,
			'most_recent': most_recent,
			'new_posts': new_posts,
			'featured': featured
	}
	return render(request, 'main/index.html', context)

def products(request):
	if request.method == 'POST':
		if "score_submit" in request.POST:
			vote_form = VoteForm(request.POST)
			if vote_form.is_valid():
				form = vote_form.save(commit=False)
				form.profile = request.user.profile
				profile_id = request.POST.get('product')
				form.product = Product.objects.get(id=product_id)
				form.save()
				form.calculate_averages()
				messages.success(request, (f'{form.product} product score submitted.'))
				return redirect('main:products')
		product_id = request.POST.get('product_pk')
		product = Product.objects.get(id=product_id)
		request.user.profile.products.add(product)
		messages.success(request, (f'{product} added to wishlist.'))
		return redirect('main:products')
	products = Product.objects.all()
	paginator = Paginator(products, 18)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	vote_form = VoteForm()
	context = {
		'page_obj': page_obj,
		'vote_form': vote_form
	}
	return render(request, 'main/products.html', context)

def register(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful.")
			return redirect('main:homepage')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	context = {'form': form}
	return render(request, 'main/register.html', context)

def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f'You are now logged in as {username}.')
				return redirect('main:homepage')
			else:
				messages.error(request, 'Invalid username or password.')
		else:
			messages.error(request, "Invalid username or password.")
	form = AuthenticationForm()
	context = {'form': form}
	return render(request, 'main/login.html', context)	

def logout_request(request):
		logout(request)
		messages.info(request, 'You have successfully logged out')
		return redirect('main:homepage')

def blog(request, tag_page):
	if tag_page == 'articles':
		tag = ''
		blog = Article.objects.all()
	else:
		tag = Tag.objects.get(tag_slug=tag_page)
		blog = Article.objects.filter(article_tags=tag)
	paginator = Paginator(blog, 25)
	page_number = request.GET.get('page')
	blog_obj = paginator.get_page(page_number)
	context = {
			'blog': blog_obj,
			'tag': tag
	}
	return render(request, 'main/blog.html', context)

def article(request, article_page):
	article = Article.objects.get(article_slug=article_page)
	context = {'article': article}
	return render(request, 'main/article.html', context)

def userpage(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid():
			user_form.save()
			messages.success(request,('Your profile was successfully updated!'))
		elif profile_form.is_valid():
			profile_form.save()
			messages.success(request,('Your wishlist was successfully updated!'))
		else:
			messages.error(request,('Unable to process request'))
		return redirect('main:userpage')
	user_form = UserForm(instance=request.user)
	profile_form = ProfileForm(instance=request.user.profile)
	context = {
			'user': request.user,
			'user_form': user_form,
			'profile_form': profile_form
	}
	return render(request, 'main/user.html', context)