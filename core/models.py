from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django import forms

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
    BRAND_CHOICES = [
        ('Intel', 'Intel'),
        ('AMD', 'AMD'),
    ]
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, null=True)
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
    BRAND_CHOICES = [
        ('ASUS', 'ASUS'),
        ('MSI', 'MSI'),
        ('Gigabyte', 'Gigabyte'),
        ('ASRock', 'ASRock'),
        ('Biostar', 'Biostar'),
        ('EVGA', 'EVGA'),
        ('NZXT', 'NZXT'),
        ('Colorful', 'Colorful'),
        ('Supermicro', 'Supermicro'),
    ]
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, null=True)
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
    BRAND_CHOICES = [
        ('Corsair', 'Corsair'),
        ('G.Skill', 'G.Skill'),
        ('Kingston', 'Kingston'),
        ('Crucial', 'Crucial'),
        ('ADATA', 'ADATA'),
        ('TeamGroup', 'TeamGroup'),
        ('Patriot', 'Patriot'),
        ('Samsung', 'Samsung'),
        ('HyperX', 'HyperX'),
        ('PNY', 'PNY'),
        ('Transcend', 'Transcend'),
    ]
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, null=True)
    RAM_TYPE_CHOICES = Motherboard.RAM_SLOTS_CHOICES

    ram_type = models.CharField(max_length=10, choices=RAM_TYPE_CHOICES)
    capacity = models.PositiveIntegerField(help_text="Capacity in GB")
    speed = models.PositiveIntegerField(help_text="Speed in MHz")


    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAMs'

class GPU(BaseComponent):
    BRAND_CHOICES = [
        ('NVIDIA', 'NVIDIA'),
        ('AMD', 'AMD'),
        ('Intel', 'Intel'),
        ('ASUS', 'ASUS'),
        ('MSI', 'MSI'),
        ('Gigabyte', 'Gigabyte'),
        ('ZOTAC', 'ZOTAC'),
        ('EVGA', 'EVGA'),
        ('Sapphire', 'Sapphire'),
        ('PowerColor', 'PowerColor'),
        ('GALAX', 'GALAX'),
        ('PNY', 'PNY'),
        ('XFX', 'XFX'),
        ('Inno3D', 'Inno3D'),
        ('Palit', 'Palit'),
        ('Colorful', 'Colorful'),
    ]
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, null=True)
    
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
    BRAND_CHOICES = [
        ('Corsair', 'Corsair'),
        ('EVGA', 'EVGA'),
        ('Seasonic', 'Seasonic'),
        ('Cooler Master', 'Cooler Master'),
        ('Antec', 'Antec'),
        ('Thermaltake', 'Thermaltake'),
        ('SilverStone', 'SilverStone'),
        ('NZXT', 'NZXT'),
        ('be quiet!', 'be quiet!'),
        ('ASUS', 'ASUS'),
        ('Gigabyte', 'Gigabyte'),
        ('MSI', 'MSI'),
        ('FSP', 'FSP'),
    ]
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, null=True)
    
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

    power_rating = models.PositiveIntegerField(help_text="Power rating in Watts")
    efficiency_rating = models.CharField(max_length=20, choices=EFFICIENCY_CHOICES)
    modularity = models.CharField(max_length=20, choices=MODULAR_CHOICES)
    cables_included = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'PSU'
        verbose_name_plural = 'PSUs'


class SSDStorage(BaseComponent):
    BRAND_CHOICES = [
        ('Samsung', 'Samsung'),
        ('Western Digital', 'Western Digital'),
        ('Crucial', 'Crucial'),
        ('Kingston', 'Kingston'),
        ('ADATA', 'ADATA'),
        ('Seagate', 'Seagate'),
        ('Corsair', 'Corsair'),
        ('SanDisk', 'SanDisk'),
        ('Transcend', 'Transcend'),
        ('PNY', 'PNY'),
        ('Intel', 'Intel'),
        ('SK hynix', 'SK hynix'),
        ('TeamGroup', 'TeamGroup'),
    ]
    brand = models.CharField(max_length=30, choices=BRAND_CHOICES, null=True)
    
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
    BRAND_CHOICES = [
        ('Western Digital', 'Western Digital'),
        ('Seagate', 'Seagate'),
        ('Toshiba', 'Toshiba'),
        ('Hitachi', 'Hitachi'),
        ('Samsung', 'Samsung'),
        ('HGST', 'HGST'),
        ('Fujitsu', 'Fujitsu'),
        ('Maxtor', 'Maxtor'),
    ]
    brand = models.CharField(max_length=30, choices=BRAND_CHOICES, null=True)
    capacity = models.PositiveIntegerField(help_text="Capacity in GB")
    rpm = models.PositiveIntegerField(help_text="Revolutions Per Minute (RPM)")
    
    class Meta:
        verbose_name = 'HDD Storage'
        verbose_name_plural = 'HDD Storages'

class Case(BaseComponent):
    BRAND_CHOICES = [
        ('Corsair', 'Corsair'),
        ('NZXT', 'NZXT'),
        ('Cooler Master', 'Cooler Master'),
        ('Thermaltake', 'Thermaltake'),
        ('Phanteks', 'Phanteks'),
        ('Fractal Design', 'Fractal Design'),
        ('Lian Li', 'Lian Li'),
        ('Antec', 'Antec'),
        ('be quiet!', 'be quiet!'),
        ('SilverStone', 'SilverStone'),
        ('Deepcool', 'Deepcool'),
        ('MSI', 'MSI'),
        ('ASUS', 'ASUS'),
        ('Gigabyte', 'Gigabyte'),
    ]
    brand = models.CharField(max_length=30, choices=BRAND_CHOICES, null=True)
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
    BRAND_CHOICES = [
        ('Cooler Master', 'Cooler Master'),
        ('Noctua', 'Noctua'),
        ('Corsair', 'Corsair'),
        ('be quiet!', 'be quiet!'),
        ('NZXT', 'NZXT'),
        ('Deepcool', 'Deepcool'),
        ('Thermaltake', 'Thermaltake'),
        ('Arctic', 'Arctic'),
        ('Cryorig', 'Cryorig'),
        ('Scythe', 'Scythe'),
        ('Phanteks', 'Phanteks'),
        ('Fractal Design', 'Fractal Design'),
        ('SilverStone', 'SilverStone'),
        ('MSI', 'MSI'),
        ('ASUS', 'ASUS'),
    ]
    brand = models.CharField(max_length=30, choices=BRAND_CHOICES, null=True)
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

class PCBuild(models.Model):
    Name = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pc_builds')
    CPU = models.ForeignKey(CPU, on_delete=models.CASCADE)
    Motherboard = models.ForeignKey(Motherboard, on_delete=models.CASCADE)
    RAM = models.ForeignKey(RAM, on_delete=models.CASCADE)
    GPU = models.ForeignKey(GPU, on_delete=models.CASCADE, null=True, blank=True)
    PSU = models.ForeignKey(PSU, on_delete=models.CASCADE)
    SSD_Storage = models.ForeignKey(SSDStorage, on_delete=models.CASCADE)
    HDD_Storage = models.ForeignKey(HDDStorage, on_delete=models.CASCADE, null=True, blank=True)
    Case = models.ForeignKey(Case, on_delete=models.CASCADE)
    CPU_Cooler = models.ForeignKey(CPUCooler, on_delete=models.CASCADE)
    Total_Price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PC Build'
        verbose_name_plural = 'PC Builds'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.Total_Price = self.get_total_price()
        super().save(*args, **kwargs)
        if is_new and not self.Name:
            self.Name = f"{self.user.username}'s PC Build #{self.pk}"
            super().save(update_fields=['Name'])

            
    def __str__(self):
        return f"PC Build by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def get_total_price(self):

        total_price = 0
        components = [
            self.CPU,
            self.Motherboard,
            self.RAM,
            self.GPU,
            self.PSU,
            self.SSD_Storage,
            self.HDD_Storage,
            self.Case,
            self.CPU_Cooler
        ]
        for component in components:
            if component:
                total_price += component.price

        return total_price
    
    def check_compatibility(self):  
        issues = []

        if self.CPU and self.Motherboard:
            if self.CPU.socket != self.Motherboard.socket:
                issues.append("CPU and Motherboard socket compatibility issue.")
            
        if self.Motherboard and self.RAM:
            if self.Motherboard.ram_type != self.RAM.ram_type:
                issues.append("Motherboard and RAM type compatibility issue.")

        if self.CPU and self.CPU_Cooler:
            if self.CPU.socket != self.CPU_Cooler.socket_compatibility:
                issues.append("CPU and CPU Cooler socket compatibility issue.")

        if self.GPU and self.Case:
            if self.Case.form_factor not in ['ATX', 'Micro-ATX', 'Mini-ITX']:
                issues.append("Case form factor may not support the GPU size.")

        if self.PSU and self.GPU and self.CPU:
            if self.PSU.power_rating < 1.5 * (self.GPU.tdp + self.CPU.tdp):
                issues.append("PSU power rating may not be sufficient for the GPU.")
        
        return issues if issues else None

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CartItem: {self.content_object} in {self.cart}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.line1}, {self.city}"











