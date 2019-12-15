from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Vote
import datetime


# Create your views here.
def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products': products})


@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and \
                request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST.get('url').startswith('http://') or request.POST.get('url').startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.date = datetime.datetime.now().date()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All Fields are required'})
    else:
        return render(request, 'products/create.html')


def detail(request, product_id):
    detail_product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': detail_product})


@login_required(login_url='/accounts/login')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        try:
            vote = Vote.objects.get(productID=product_id, userID=request.user)
        except Vote.DoesNotExist:
            vote = None

        if vote is None and product.hunter != request.user:
            # find product by id and increment
            vote = Vote(productID=product, userID=request.user)
            product.votes_total += 1
            vote.save()
            product.save()
        return redirect('/products/' + str(product.id))


