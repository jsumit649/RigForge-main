from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, CPU, GPU, RAM, Motherboard, PSU, SSDStorage, HDDStorage, Case, CPUCooler

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'name')
    list_filter = ('is_staff', 'is_active')



@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cores', 'threads', 'base_clock', 'boost_clock', 'socket', 'created_at', 'updated_at')
    search_fields = ('name', 'socket')
    list_filter = ('socket', 'created_at', 'updated_at')

@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'vram', 'memory_type', 'created_at', 'updated_at')
    search_fields = ('name', 'memory_type')
    list_filter = ('memory_type', 'created_at', 'updated_at')

@admin.register(RAM)
class RAMAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'capacity', 'speed', 'ram_type', 'created_at', 'updated_at')
    search_fields = ('name', 'ram_type')
    list_filter = ('ram_type', 'created_at', 'updated_at')

@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'socket', 'form_factor', 'created_at', 'updated_at')
    search_fields = ('name', 'socket')
    list_filter = ('socket', 'form_factor', 'created_at', 'updated_at')

@admin.register(PSU)
class PSUAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'power_rating', 'efficiency_rating', 'created_at', 'updated_at')
    search_fields = ('name', 'efficiency_rating')
    list_filter = ('efficiency_rating', 'created_at', 'updated_at')

@admin.register(SSDStorage)
class SSDStorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'capacity', 'pcie_generation', 'created_at', 'updated_at')
    search_fields = ('name', 'pcie_generation')
    list_filter = ('pcie_generation', 'created_at', 'updated_at')

@admin.register(HDDStorage)
class HDDStorageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'capacity', 'rpm', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'form_factor', 'created_at', 'updated_at')
    search_fields = ('name', 'form_factor')
    list_filter = ('form_factor', 'created_at', 'updated_at')

@admin.register(CPUCooler)
class CPUCoolerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'cooler_type', 'socket_compatibility', 'created_at', 'updated_at')
    search_fields = ('name', 'cooler_type')
    list_filter = ('cooler_type', 'socket_compatibility', 'created_at', 'updated_at')