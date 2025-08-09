from rest_framework import serializers
from .models import CPU, GPU, Motherboard, RAM, PSU, SSDStorage, HDDStorage, Case, CPUCooler

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'

class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = '__all__'

class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = '__all__'

class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = '__all__'

class PSUSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSU
        fields = '__all__'

class SSDStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSDStorage
        fields = '__all__'

class HDDStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HDDStorage
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'


class CPUCoolerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPUCooler
        fields = '__all__'

