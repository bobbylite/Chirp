from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
import requests


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    print("UserViewSet!")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class HomeView(TemplateView):
    var1 = "192.168.1.1"
    var2 = "USA"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({'geoData': self.webRequest()})
        return context

    def __init__(self):
        response = requests.get('https://freegeoip.app/json/')
        geodata = response.json()
        print(geodata)
    

    
    def webRequest(self):
        response = requests.get('https://freegeoip.app/json/')
        geodata = response.json()
        return {
            'ip': geodata['ip'],
            'country': geodata['country_name']
        }

    template_name = 'home/home.html'

class WebRequest(APIView):
    def post(self, request, *args, **kwargs):
        return self.process_request(request, request.data)

    def get(self, request, format=None):
        return self.process_request(request, request.query_params)

    def process_request(self, request, data):
        print(data)


def renderHomePage(request):
    response = requests.get('http://freegeoip.net/json/')
    geodata = response.json()
    return render(request, 'home/home.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name']
    })