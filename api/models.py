import qrcode
import datetime
from io import BytesIO
from django.core.files import File
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PasswordOTPReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)

class Gender(models.TextChoices):
    pria = 'pria', 'PRIA'
    wanita = 'wanita', 'WANITA'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

class Merk(models.Model):
    nama_merk = models.CharField(max_length=255)
    img_merk = models.ImageField(upload_to='merk/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_merk

class Seri(models.Model):
    judul_seri = models.CharField(max_length=255, blank=True)
    nama_seri = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.judul_seri = f"{self.merk.nama_merk} - {self.nama_seri}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_seri


class KodeKomponen(models.TextChoices):
    baterai = 'baterai', 'BATERAI'
    casing = 'casing', 'CASING'
    charger = 'charger', 'CHARGER'
    gpu = 'gpu', 'GPU',
    kamera = 'kamera', 'KAMERA'
    layar = 'layar', 'LAYAR'
    penyimpanan = 'penyimpanan', 'PENYIMPANAN'
    prosesor = 'prosesor', 'PROSESOR'
    ram = 'ram', 'RAM'

class JenisBahan(models.Model):
    nama_bahan = models.CharField(max_length=255)
    kode_komponen = models.CharField(max_length=15, choices=KodeKomponen.choices)
    status_eco_friendly = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nama_bahan} – {self.kode_komponen.upper()}"


class BateraiLaptop(models.Model):
    judul_baterai = models.CharField(max_length=255, blank=True)
    seri_baterai = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    kapasitas = models.IntegerField()
    voltage = models.DecimalField(max_digits=5, decimal_places=2)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_baterai = f"Baterai {self.merk.nama_merk} – {self.seri_baterai} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_baterai

class ResolusiChoices(models.TextChoices):
    hd = 'hd', 'HD'
    full_hd = 'full hd', 'FULL HD'
    res_2k = '2k', '2K'
    res_4k = '4k', '4K'

class RefreshRateChoices(models.TextChoices):
    h_60hz = '60hz', '60HZ'
    h_90hz = '90hz', '90HZ'
    h_120hz = '120hz', '120HZ'
    h_144hz = '144hz', '144HZ'

class Layar(models.Model):
    judul_layar = models.CharField(max_length=255, blank=True)
    seri_layar = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    panjang_layar = models.IntegerField()
    lebar_layar = models.IntegerField()
    resolusi = models.CharField(max_length=10, choices=ResolusiChoices.choices)
    refresh_rate = models.CharField(max_length=10, choices=RefreshRateChoices.choices)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_layar = f"Layar {self.merk.nama_merk} – {self.seri_layar} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_layar

class VentilasiChoices(models.TextChoices):
    fan = 'fan', 'FAN'
    airflow = 'airflow', 'AIRFLOW'

class Casing(models.Model):
    judul_casing = models.CharField(max_length=255, blank=True)
    seri_casing = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    ventilasi = models.CharField(max_length=20, choices=VentilasiChoices.choices)
    panjang = models.IntegerField()
    lebar = models.IntegerField()
    tinggi = models.IntegerField()
    warna = models.CharField(max_length=20)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_casing = f"Casing {self.merk.nama_merk} – {self.seri_casing} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_casing

class ArsitekturProsesorChoices(models.TextChoices):
    x86 = 'x86', 'X86'
    arm = 'arm', 'ARM'
    arm64 = 'arm64', 'ARM64'

class Prosesor(models.Model):
    judul_prosesor = models.CharField(max_length=255, blank=True)
    seri_prosesor = models.CharField(max_length=255)
    jumlah_core = models.IntegerField()
    kecepatan_clock = models.DecimalField(max_digits=5, decimal_places=2)
    arsitektur = models.CharField(max_length=8, choices=ArsitekturProsesorChoices.choices)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_prosesor = f"Prosesor {self.merk.nama_merk} – {self.seri_prosesor} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_prosesor

class TipeGPUChoices(models.TextChoices):
    integrated = 'integrated', 'INTEGRATED'
    discrete = 'discrete', 'DISCRETE'

class GPU(models.Model):
    judul_gpu = models.CharField(max_length=255, blank=True)
    tipe_gpu = models.CharField(max_length=25, choices=TipeGPUChoices.choices)
    model_gpu = models.CharField(max_length=255)
    memori_gpu = models.CharField(max_length=255)
    keperluan = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_gpu = f"GPU {self.merk.nama_merk} – {self.model_gpu} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_gpu

class JenisRamChoices(models.TextChoices):
    ddr3 = 'ddr3', 'DDR3'
    ddr4 = 'ddr4', 'DDR4'
    ddr5 = 'ddr5', 'DDR5'
    lpddr = 'lpddr', 'LPDDR'

class RAM(models.Model):
    judul_ram = models.CharField(max_length=255, blank=True)
    jenis_ram = models.CharField(max_length=10, choices=JenisRamChoices.choices)
    kapasitas_ram = models.IntegerField()
    kecepatan_ram = models.IntegerField()
    cas_latency = models.IntegerField()
    seri_ram = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_ram = f"RAM {self.merk.nama_merk} – {self.jenis_ram} {self.kapasitas_ram} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_ram

class JenisPenyimpanan(models.TextChoices):
    SSD = 'ssd', 'SSD'
    HDD = 'hdd', 'HDD'
    eMMC = 'emmc', 'eMMC'
    UFS = 'ufs', 'UFS'

class Penyimpanan(models.Model):
    judul_penyimpanan = models.CharField(max_length=255, blank=True)
    seri_penyimpan = models.CharField(max_length=255)
    kapasitas_penyimpanan = models.IntegerField()
    kecepatan_baca_tulis = models.DecimalField( max_digits=6, decimal_places=1)
    form_factor = models.DecimalField(max_digits=5, decimal_places=2)
    jenis_penyimpanan = models.CharField(max_length=6, choices=JenisPenyimpanan.choices)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_penyimpanan = f"{self.jenis_penyimpanan}  {self.merk.nama_merk} – {self.seri_penyimpan} {self.kapasitas_penyimpanan} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_penyimpanan

class TipeLensaChoices(models.TextChoices):
    wide = 'wide', 'WIDE'
    ultrawide = 'ultrawide', 'ULTRAWIDE'
    telephoto = 'telephoto', 'TELEPHOTO'
    makro = 'makro', 'MAKRO'

class Kamera(models.Model):
    judul_kamera = models.CharField(max_length=255, blank=True)
    resolusi = models.IntegerField()
    tipe_lensa = models.CharField(max_length=25, choices=TipeLensaChoices.choices)
    seri_kamera = models.CharField(max_length=255)
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_kamera = f"Layar {self.merk.nama_merk} – {self.seri_kamera} {self.tipe_lensa} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_kamera

class TipePortChoices(models.TextChoices):
    usb_a = 'usb-a', 'USB-A'
    usb_c = 'usb-c', 'USB-C'
    magsafe = 'magsafe', 'MAGSAFE'

class TeknologiChargingChoices(models.TextChoices):
    quick_charger = 'quick charger', 'QUICK CHARGER'
    power_delivery = 'power delivery', 'POWER DELIVERY'
    vooc = 'vooc', 'VOOC'

class Charger(models.Model):
    judul_charger = models.CharField(max_length=255, blank=True)
    seri_charger = models.CharField(max_length=255)
    tipe_port = models.CharField(max_length=10, choices=TipePortChoices.choices)
    teknologi_charger = models.CharField(max_length=40, choices=TeknologiChargingChoices.choices)
    kompatibilitas_tegangan = models.IntegerField()
    merk = models.ForeignKey(Merk, on_delete=models.CASCADE)
    jenis_bahan = models.ForeignKey(JenisBahan, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        eco_status = "Eco-Friendly" if self.jenis_bahan.status_eco_friendly else "Not Eco-Friendly"
        self.judul_charger = f"Layar {self.merk.nama_merk} – {self.seri_charger} – {eco_status}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_charger

class Laptop(models.Model):
    judul_laptop = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    seri = models.ForeignKey(Seri, on_delete=models.CASCADE)
    tahun_seri = models.IntegerField()
    upload_foto = models.ImageField(upload_to='laptop/%Y/%m/%d/')
    jenis_warna = models.CharField(max_length=100)
    baterai = models.ForeignKey(BateraiLaptop, on_delete=models.CASCADE)
    prosesor = models.ForeignKey(Prosesor, on_delete=models.CASCADE)
    casing = models.ForeignKey(Casing, on_delete=models.CASCADE)
    penyimpanan = models.ForeignKey(Penyimpanan, on_delete=models.CASCADE)
    kamera = models.ForeignKey(Kamera, on_delete=models.CASCADE)
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE)
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE)
    layar = models.ForeignKey(Layar, on_delete=models.CASCADE)
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE)
    status_eco_friendly = models.BooleanField(blank=True)
    qr_code_laptop = models.ImageField(upload_to='barcode_produk/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_qr_code(self):
        url = f"https://seno11.pythonanywhere.com/api/laptop/{self.id}/"

        qr_img = qrcode.make(url)

        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        filename = f"laptop_{self.id}_qr.png"

        self.qr_code_laptop.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        komponen = [
            self.baterai.jenis_bahan,
            self.prosesor.jenis_bahan,
            self.casing.jenis_bahan,
            self.penyimpanan.jenis_bahan,
            self.kamera.jenis_bahan,
            self.gpu.jenis_bahan,
            self.charger.jenis_bahan,
            self.layar.jenis_bahan,
            self.ram.jenis_bahan,
        ]

        jumlah_eco = sum(1 for bahan in komponen if bahan.status_eco_friendly)
        jumlah_non_eco = len(komponen) - jumlah_eco

        self.judul_laptop = (
            f"Laptop {self.seri.judul_seri} – {self.tahun_seri} - {self.jenis_warna}"
        )

        self.status_eco_friendly = jumlah_eco > jumlah_non_eco

        if not self.id:
            super().save(*args, **kwargs)

        self.generate_qr_code()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul_laptop

class Komentar(models.Model):
    laptop = models.ForeignKey('Laptop', on_delete=models.CASCADE, related_name='komentar')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isi_komentar = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='balasan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.isi_komentar[:30]}"

    class Meta:
        ordering = ['created_at']