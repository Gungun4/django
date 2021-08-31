from django.shortcuts import render, HttpResponseRedirect, HttpResponse
# Create your views here.

def index_view(request):
    return render(request, 'music/index.html')