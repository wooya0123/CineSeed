from django.shortcuts import render

# Create your views here.
def funding_list(request):
    pass

def funding_detail(request):
    funding_id = request.GET.get('필드명')