from django.views.generic import ListView
from ..model.define_models import SelectProjectModel

class DefineViewList(ListView):
    model = SelectProjectModel