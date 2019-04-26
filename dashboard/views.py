from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def about(request):
    return  render(request,'about.html')

def product(request):
    return  render(request,'our-product.html')

def news(request):
    return render(request,'news.html')