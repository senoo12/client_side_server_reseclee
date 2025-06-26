from django.contrib import admin
from django.utils.html import format_html
from api.models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'gender', 'bio', 'profile_picture']

admin.site.register(Profile, ProfileUserAdmin)

class SeriAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_seri', 'nama_seri', 'merk']
    readonly_fields = ['judul_seri']

admin.site.register(Seri, SeriAdmin)

class MerkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'nama_merk', 'img_merk']

admin.site.register(Merk, MerkAdmin)

class JenisBahanAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'nama_bahan', 'kode_komponen', 'status_eco_friendly']

admin.site.register(JenisBahan, JenisBahanAdmin)

class BateraiLaptopAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_baterai', 'seri_baterai', 'merk', 'kapasitas', 'voltage', 'jenis_bahan']
    readonly_fields = ['judul_baterai']

admin.site.register(BateraiLaptop, BateraiLaptopAdmin)

class LayarAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_layar', 'seri_layar', 'merk', 'panjang_layar', 'lebar_layar', 'resolusi', 'refresh_rate', 'jenis_bahan']
    readonly_fields = ['judul_layar']

admin.site.register(Layar, LayarAdmin)

class CasingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_casing', 'seri_casing', 'merk', 'ventilasi', 'panjang', 'lebar', 'tinggi', 'warna', 'jenis_bahan']
    readonly_fields = ['judul_casing']

admin.site.register(Casing, CasingAdmin)

class ProsesorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_prosesor', 'seri_prosesor', 'jumlah_core', 'kecepatan_clock', 'arsitektur', 'merk', 'jenis_bahan']
    readonly_fields = ['judul_prosesor']

admin.site.register(Prosesor, ProsesorAdmin)

class GPUAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_gpu', 'tipe_gpu', 'model_gpu', 'memori_gpu', 'keperluan', 'merk', 'jenis_bahan']
    readonly_fields = ['judul_gpu']

admin.site.register(GPU, GPUAdmin)

class RAMAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_ram', 'jenis_ram', 'kapasitas_ram', 'kecepatan_ram', 'cas_latency', 'seri_ram', 'merk', 'jenis_bahan']
    readonly_fields = ['judul_ram']

admin.site.register(RAM, RAMAdmin)

class PenyimpananAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_penyimpanan', 'seri_penyimpan', 'kapasitas_penyimpanan', 'kecepatan_baca_tulis', 'form_factor', 'jenis_penyimpanan', 'merk', 'jenis_bahan']
    readonly_fields = ['judul_penyimpanan']

admin.site.register(Penyimpanan, PenyimpananAdmin)

class KameraAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_kamera', 'resolusi', 'tipe_lensa', 'seri_kamera', 'merk', 'jenis_bahan']
    readonly_fields = ['judul_kamera']

admin.site.register(Kamera, KameraAdmin)

class ChargerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_charger', 'seri_charger', 'tipe_port', 'teknologi_charger', 'kompatibilitas_tegangan', 'merk', 'jenis_bahan']
    readonly_fields = ['judul_charger']

admin.site.register(Charger, ChargerAdmin)

class LaptopAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'judul_laptop', 'jenis_warna', 'tahun_seri', 'status_eco_friendly', 'qr_preview']
    readonly_fields = ['judul_laptop', 'status_eco_friendly', 'qr_code_laptop', 'qr_preview']

    def qr_preview(self, obj):
        if obj.qr_code_laptop:
            return format_html('<img src="{}" width="150" height="150" />', obj.qr_code_laptop.url)
        return "Belum ada QR Code"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)   # Simpan dulu agar dapat ID
        obj.generate_qr_code()                           # Generate QR setelah disimpan
        obj.save(update_fields=['qr_code_laptop'])

admin.site.register(Laptop, LaptopAdmin)

class KomentarAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['laptop', 'user', 'isi_komentar', 'parent']
    readonly_fields = ['laptop', 'user', 'isi_komentar', 'parent']

admin.site.register(Komentar, KomentarAdmin)