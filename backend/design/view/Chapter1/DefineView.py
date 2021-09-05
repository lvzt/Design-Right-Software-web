# from django.views.generic import ListView, CreateView
from rest_framework import generics
from .model.Chaper1.define_models import SelectProject
from .serializers.Chapter1.design_serializer import DesignSerializer

# class DefineViewList(ListView):
class DefineViewList(generics.ListCreateAPIView):
    model = SelectProject
    queryset = SelectProject.objects.all() 
    serializer_class = DesignSerializer

class DefineViewDetail(generics.RetrieveUpdateDestroyAPIView):
    model = SelectProject
    queryset = SelectProject.objects.all() 
    serializer_class = DesignSerializer
    # def get_queryset(self):
    #     return SelectProject.objects.all()

# class CreateDefineView(generics.ListCreateAPIView):
#     model = SelectProject
#     serializer_class = DesignSerializer

#     def get_queryset(self):
#         return SelectProject.objects.all()