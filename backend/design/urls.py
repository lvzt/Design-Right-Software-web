from django.urls import path
from .view.DefineView import DefineViewList, DefineViewDetail#, CreateDefineView
from .view.DefineOwnerView import DefineOwnerView, AddOrEditOwnerView, DelOwnerView

app_name = 'design'

urlpatterns = [
    path('define', DefineViewList.as_view()),
    path('define/<int:pk>', DefineViewDetail.as_view()),
    path('define_owner', DefineOwnerView.as_view()),
    path('define_owner/add_or_edit', AddOrEditOwnerView.as_view()),
    path('define_owner/delete', DelOwnerView.as_view())
    # path('define/add', CreateDefineView.as_view()),
]