from rest_framework import serializers
from ..model.define_models import SelectProject

class DesignSerializer(serializers.ModelSerializer):
    project_description = serializers.CharField()
    class Meta:
        model = SelectProject
        fields = '__all__'