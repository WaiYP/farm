from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def about(request):
    return  render(request,'about.html')

def product(request):
    return  render(request,'our-product.html')

def news(request):
    return render(request,'news.html')

def shop(request):
    datalist=[1,2,3,4,5,6,7,8,9,10,11]
    context = {
        'datalist':datalist
    }
    return render(request,'shop.html',context)

def farmingpractice(request):
    return render(request,'farming-practice.html')

def newdetail(request):
    return render(request,'news-details.html')

def contact(request):
    return render(request,'contact.html')