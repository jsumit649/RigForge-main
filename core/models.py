from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()




'''
From here it is the models.py file for components
'''



class BaseComponent(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(help_text="Detailed description of the component So that youser can see what it is in the frontend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    

class CPU(BaseComponent):
    SOCKET_CHOICES = [
        ('AM4', 'AM4'),
        ('AM5', 'AM5'),
        ('LGA1200', 'LGA1200'),
        ('LGA1700', 'LGA1700'),
        ('LGA2011', 'LGA2011'),
    ]

    socket = models.CharField(max_length=20, choices=SOCKET_CHOICES)
    cores = models.PositiveIntegerField()
    threads = models.PositiveIntegerField()
    base_clock = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    boost_clock = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    tdp = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPUs'



class Motherboard(BaseComponent):
    SOCKET_CHOICES = CPU.SOCKET_CHOICES

    FORM_FACTOR_CHOICES = [
        ('ATX', 'ATX'),
        ('Micro-ATX', 'Micro-ATX'),
        ('Mini-ITX', 'Mini-ITX'),
    ]

    RAM_SLOTS_CHOICES = [
        ("DDR4", "DDR4"),
        ("DDR5", "DDR5"),
    ]

    socket = models.CharField(max_length=20, choices=SOCKET_CHOICES)
    form_factor = models.CharField(max_length=20, choices=FORM_FACTOR_CHOICES)
    ram_type = models.CharField(max_length=10, choices=RAM_SLOTS_CHOICES)
    ram_slots = models.PositiveIntegerField()
    max_ram = models.PositiveIntegerField(help_text="Maximum RAM in GB")

    class Meta:
        verbose_name = 'Motherboard'
        verbose_name_plural = 'Motherboards'

class RAM(BaseComponent):
    RAM_TYPE_CHOICES = Motherboard.RAM_SLOTS_CHOICES

    ram_type = models.CharField(max_length=10, choices=RAM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField(help_text="Capacity in GB")
    speed = models.PositiveIntegerField(help_text="Speed in MHz")

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAMs'

class GPU(BaseComponent):
    VRAM_CHOICES = [
        ('2GB', '2GB'),
        ('4GB', '4GB'),
        ('6GB', '6GB'),
        ('8GB', '8GB'),
        ('10GB', '10GB'),
        ('12GB', '12GB'),
        ('16GB', '16GB'),
        ('24GB', '24GB'),
    ]

    MEMORY_TYPE_CHOICES = [
        ('GDDR5', 'GDDR5'),
        ('GDDR5X', 'GDDR5X'),
        ('GDDR6', 'GDDR6'),
        ('GDDR6X', 'GDDR6X'),
    ]

    vram = models.CharField(max_length=5, choices=VRAM_CHOICES)
    memory_type = models.CharField(max_length=10, choices=MEMORY_TYPE_CHOICES)
    base_clock = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    boost_clock = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    tdp = models.PositiveIntegerField()


    class Meta:
        verbose_name = 'GPU'
        verbose_name_plural = 'GPUs'


class PSU(BaseComponent):
    POWER_CHOICES = [
        ('450W', '450W'),
        ('550W', '550W'),
        ('650W', '650W'),
        ('750W', '750W'),
        ('850W', '850W'),
        ('1000W', '1000W'),
    ]
    EFFICIENCY_CHOICES = [
        ("80+", "80 Plus"),
        ("80+ Bronze", "80 Plus Bronze"),
        ("80+ Silver", "80 Plus Silver"),
        ("80+ Gold", "80 Plus Gold"),
        ("80+ Platinum", "80 Plus Platinum"),
        ("80+ Titanium", "80 Plus Titanium"),
    ]

    MODULAR_CHOICES = [
        ("Non-Modular", "Non-Modular"),
        ("Semi-Modular", "Semi-Modular"),
        ("Fully-Modular", "Fully Modular"),
    ]

    power_rating = models.CharField(max_length=10, choices=POWER_CHOICES)
    efficiency_rating = models.CharField(max_length=20, choices=EFFICIENCY_CHOICES)
    modularity = models.CharField(max_length=20, choices=MODULAR_CHOICES)
    cables_included = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'PSU'
        verbose_name_plural = 'PSUs'


class SSDStorage(BaseComponent):
    
    PCIE_GENERATIONS = [
        ('Gen3', 'PCIe Gen 3'),
        ('Gen4', 'PCIe Gen 4'), 
        ('Gen5', 'PCIe Gen 5'),
    ]

    capacity = models.PositiveIntegerField(help_text="Capacity in GB")
    pcie_generation = models.CharField(max_length=10, choices=PCIE_GENERATIONS)
    read_speed = models.PositiveIntegerField(help_text="Read Speed in MB/s")
    write_speed = models.PositiveIntegerField(help_text="Write Speed in MB/s")
    
    class Meta:
        verbose_name = 'SSD Storage'
        verbose_name_plural = 'SSD Storages'
    
class HDDStorage(BaseComponent):
    capacity = models.PositiveIntegerField(help_text="Capacity in GB")
    rpm = models.PositiveIntegerField(help_text="Revolutions Per Minute (RPM)")
    
    class Meta:
        verbose_name = 'HDD Storage'
        verbose_name_plural = 'HDD Storages'

class Case(BaseComponent):
    FORM_FACTOR_CHOICES = Motherboard.FORM_FACTOR_CHOICES

    form_factor = models.CharField(max_length=20, choices=FORM_FACTOR_CHOICES)
    color = models.CharField(max_length=50, blank=True, null=True)
    cooling_support = models.BooleanField(default=True)
    fan_slots = models.PositiveIntegerField(help_text="Number of fan slots available")
    front_usb_ports = models.PositiveIntegerField(help_text="Number of front USB ports")

    class Meta:
        verbose_name = 'Case'
        verbose_name_plural = 'Cases'


class CPUCooler(BaseComponent):
    COOLER_TYPE_CHOICES = [
        ('Air', 'Air Cooler'),
        ('Liquid', 'Liquid Cooler'),
        ('AIO', 'All-in-One Liquid Cooler'),
    ]

    cooler_type = models.CharField(max_length=10, choices=COOLER_TYPE_CHOICES)
    socket_compatibility = models.CharField(max_length=20, choices=CPU.SOCKET_CHOICES)
    cooling_capacity = models.PositiveIntegerField(help_text="Cooling capacity in Watts")

    class Meta:
        verbose_name = 'CPU Cooler'
        verbose_name_plural = 'CPU Coolers'