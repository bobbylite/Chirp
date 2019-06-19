from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
import requests

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    print("UserViewSet!")

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({'geoData': self.webRequest()})
        return context

    def __init__(self):
        print("initialized")
    
    def webRequest(self):
        response = requests.get('https://freegeoip.app/json/')
        geodata = response.json() 
        return {
            'ip': geodata['ip'],
            'country': geodata['country_name']
        }

    template_name = 'home/home.html'

class WebRequest(APIView):
    def post(self, url, dataObject):
        response = requests.post(url, dataObject)
        return self.process_request(response)

    def get(self, url):
        response = requests.get(url)
        return self.process_json(response)

    def process_json(self, response):
        return response.json()

    def process_request(self, response):
        return response.text()


def renderHomePage(request):
    response = requests.get('http://freegeoip.net/json/')
    geodata = response.json()
    return render(request, 'home/home.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name']
    })