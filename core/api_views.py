from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CPU, GPU, Motherboard, RAM, PSU, SSDStorage, HDDStorage, Case, CPUCooler, Cart, CartItem
from .serializers import (
    CPUSerializer, GPUSerializer, MotherboardSerializer, RAMSerializer,
    PSUSerializer, SSDStorageSerializer, HDDStorageSerializer, CaseSerializer, CPUCoolerSerializer
)

@api_view(['GET'])
def cpu_list(request):
    cpus = CPU.objects.all()
    serializer = CPUSerializer(cpus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def gpu_list(request):
    gpus = GPU.objects.all()
    serializer = GPUSerializer(gpus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def motherboard_list(request):
    motherboards = Motherboard.objects.all()
    serializer = MotherboardSerializer(motherboards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ram_list(request):
    rams = RAM.objects.all()
    serializer = RAMSerializer(rams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def psu_list(request):
    psus = PSU.objects.all()
    serializer = PSUSerializer(psus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ssd_storage_list(request):
    ssds = SSDStorage.objects.all()
    serializer = SSDStorageSerializer(ssds, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def hdd_storage_list(request):
    hdds = HDDStorage.objects.all()
    serializer = HDDStorageSerializer(hdds, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def case_list(request):
    cases = Case.objects.all()
    serializer = CaseSerializer(cases, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def cpu_cooler_list(request):
    coolers = CPUCooler.objects.all()
    serializer = CPUCoolerSerializer(coolers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    component_type = request.data.get('component_type')
    object_id = request.data.get('object_id')
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get(model=component_type.lower())
    cart, created = Cart.objects.get_or_create(user=request.user)
    CartItem.objects.create(cart=cart, content_type=content_type, object_id=object_id)
    return Response({'status': 'added'})