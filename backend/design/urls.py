from django.urls import path
from .view.DefineView import DefineViewList, DefineViewDetail#, CreateDefineView

app_name = 'design'

urlpatterns = [
    path('define', DefineViewList.as_view()),
    path('define/<int:pk>', DefineViewDetail.as_view()),
    # path('define/add', CreateDefineView.as_view()),
]