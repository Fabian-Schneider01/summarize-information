from django.shortcuts import render

# Create your views here.
def index(request):
    print("works")
    return render(request, 'core/index.html', {})