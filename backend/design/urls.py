from django.urls import path
from .view.DefineView import DefineViewList

app_name = 'design'

urlpatterns = [
    path('define', DefineViewList.as_view()),
]