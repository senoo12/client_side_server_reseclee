from django.contrib.auth.models import Group, User
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class RegisterSerializers(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )


        user.set_password(validated_data['password'])
        user.save()

        return user

class ChangePasswordSerializers(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetRequestSerializers(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializers(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=128)
    token = serializers.CharField()
    uidb64 = serializers.CharField()

class ProfileSerializers(serializers.HyperlinkedModelSerializer):
    full_name = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'bio', 'profile_picture']
        read_only_fields = ['user']

    def to_representation(self, instance):
        # saat GET
        ret = super().to_representation(instance)
        ret['full_name'] = f"{instance.user.first_name} {instance.user.last_name}".strip()
        return ret

    def update(self, instance, validated_data):
        full_name = validated_data.pop('full_name', None)

        # Update nama user jika full_name disediakan
        if full_name:
            parts = full_name.strip().split(" ", 1)
            instance.user.first_name = parts[0]
            instance.user.last_name = parts[1] if len(parts) > 1 else ""
            instance.user.save()

        # Update profil
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MerkSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Merk
        fields = ['id', 'url', 'nama_merk', 'img_merk', 'created_at', 'updated_at']

class SeriSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seri
        fields = ['id',  'url', 'judul_seri', 'nama_seri', 'merk', 'created_at', 'updated_at']

class JenisBahanSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JenisBahan
        fields = ['id', 'url', 'nama_bahan', 'kode_komponen', 'status_eco_friendly', 'created_at', 'updated_at']

class BateraiLaptopSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BateraiLaptop
        fields = ['id', 'url', 'judul_baterai', 'seri_baterai', 'kapasitas', 'voltage', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class LayarSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Layar
        fields = ['id', 'url', 'judul_layar', 'seri_layar', 'panjang_layar', 'lebar_layar', 'resolusi', 'refresh_rate', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class CasingSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Casing
        fields = ['id', 'url', 'judul_casing', 'seri_casing', 'ventilasi', 'panjang', 'lebar', 'tinggi', 'warna', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class ProsesorSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prosesor
        fields = ['id', 'url', 'judul_prosesor', 'seri_prosesor', 'jumlah_core', 'kecepatan_clock', 'arsitektur', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class GPUSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GPU
        fields = ['id', 'url', 'judul_gpu', 'tipe_gpu', 'model_gpu', 'memori_gpu', 'keperluan', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class RAMSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RAM
        fields = ['id', 'url', 'judul_ram', 'jenis_ram', 'kapasitas_ram', 'kecepatan_ram', 'cas_latency', 'seri_ram', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class PenyimpananSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Penyimpanan
        fields = ['id', 'url', 'judul_penyimpanan', 'seri_penyimpan', 'kapasitas_penyimpanan', 'kecepatan_baca_tulis', 'form_factor', 'jenis_penyimpanan', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class KameraSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kamera
        fields = ['id', 'url', 'judul_kamera', 'resolusi', 'tipe_lensa', 'seri_kamera', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class ChargerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Charger
        fields = ['id', 'url', 'judul_charger', 'seri_charger', 'tipe_port', 'teknologi_charger', 'kompatibilitas_tegangan', 'merk', 'jenis_bahan', 'created_at', 'updated_at']

class LaptopSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Laptop
        fields = '__all__'

# class KomentarSerializers(serializers.HyperlinkedModelSerializer):
#     user = serializers.CharField(source='user.username', read_only=True)  # Ini ubahannya

#     class Meta:
#         model = Komentar
#         fields = ['id', 'url', 'isi_komentar', 'created_at', 'laptop', 'user', 'parent']

class KomentarReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # tampilkan username

    class Meta:
        model = Komentar
        fields = ['id', 'url', 'isi_komentar', 'created_at', 'laptop', 'user', 'parent']


class KomentarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komentar
        fields = ['laptop', 'isi_komentar', 'parent']  # tanpa `user`
