import random
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from django.urls import reverse
from .models import *
from .serializers import *
from rest_framework.response import Response

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers
    http_method_names = ['post']

class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializers(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Password lama salah."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response({"detail": "Password berhasil diganti."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_exempt, name='dispatch')
# class PasswordResetRequestView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):  # <- Perhatikan tidak ada spasi ekstra di sini
#         email = request.data.get("email")
#         if not email:
#             return Response({"error": "Email wajib diisi"}, status=400)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({"error": "Email tidak ditemukan"}, status=404)

#         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#         token = PasswordResetTokenGenerator().make_token(user)

#         reset_link = f"reseecle://reset-password-confirm/{uidb64}/{token}/"

#         send_mail(
#             subject="Reset Password Anda",
#             message=f"Klik link ini untuk reset password Anda: {reset_link}",
#             from_email="serverreseecle@gmail.com",
#             recipient_list=[email],
#         )

#         return Response({"message": "Link reset password berhasil dikirim ke email."})

# class PasswordResetConfirmView(APIView):
#     def post(self, request, uidb64, token):
#         serializer = SetNewPasswordSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             return Response({"error": "Token tidak valid"}, status=status.HTTP_400_BAD_REQUEST)

#         token_generator = PasswordResetTokenGenerator()
#         if not token_generator.check_token(user, token):
#             return Response({"error": "Token tidak valid atau sudah expired"}, status=status.HTTP_400_BAD_REQUEST)

#         password = serializer.validated_data['password']
#         user.set_password(password)
#         user.save()

#         return Response({"message": "Password berhasil direset."})

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email wajib diisi"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email tidak ditemukan"}, status=404)

        otp = f"{random.randint(100000, 999999)}"

        # Simpan OTP di DB
        PasswordOTPReset.objects.create(user=user, otp=otp)

        send_mail(
            subject="Kode OTP Reset Password",
            message=f"Kode OTP Anda: {otp}\nBerlaku selama 5 menit.",
            from_email="serverreseecle@gmail.com",
            recipient_list=[email],
        )

        return Response({"message": "Kode OTP sudah dikirim ke email."})

class PasswordResetConfirmOTPView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        if not otp:
            return Response({"error": "OTP wajib diisi"}, status=400)

        try:
            otp_obj = PasswordOTPReset.objects.get(otp=otp, is_used=False)
        except PasswordOTPReset.DoesNotExist:
            return Response({"error": "OTP tidak valid atau sudah digunakan"}, status=400)

        if otp_obj.is_expired():
            return Response({"error": "OTP kadaluarsa"}, status=400)

        # Simpan status validasi berhasil (opsional)
        return Response({"message": "OTP valid", "email": otp_obj.user.email}, status=200)

class SetNewPasswordView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        password = request.data.get('password')

        if not otp or not password:
            return Response({"error": "OTP dan password wajib diisi"}, status=400)

        try:
            otp_obj = PasswordOTPReset.objects.get(otp=otp, is_used=False)
        except PasswordOTPReset.DoesNotExist:
            return Response({"error": "OTP tidak valid"}, status=400)

        if otp_obj.is_expired():
            return Response({"error": "OTP kadaluarsa"}, status=400)

        try:
            user = otp_obj.user
        except User.DoesNotExist:
            return Response({"error": "User tidak ditemukan"}, status=404)

        user.password = make_password(password)
        user.save()

        otp_obj.is_used = True
        otp_obj.save()

        return Response({"message": "Password berhasil diubah"}, status=200)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializers
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this profile.")
        serializer.save()

class MerkViewSet(viewsets.ModelViewSet):
    queryset = Merk.objects.all()
    serializer_class = MerkSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class SeriViewSet(viewsets.ModelViewSet):
    queryset = Seri.objects.all()
    serializer_class = SeriSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class JenisBahanViewSet(viewsets.ModelViewSet):
    queryset = JenisBahan.objects.all()
    serializer_class = JenisBahanSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class BateraiLaptopViewSet(viewsets.ModelViewSet):
    queryset = BateraiLaptop.objects.all()
    serializer_class = BateraiLaptopSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class LayarViewSet(viewsets.ModelViewSet):
    queryset = Layar.objects.all()
    serializer_class = LayarSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class CasingViewSet(viewsets.ModelViewSet):
    queryset = Casing.objects.all()
    serializer_class = CasingSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class ProsesorViewSet(viewsets.ModelViewSet):
    queryset = Prosesor.objects.all()
    serializer_class = ProsesorSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class RAMViewSet(viewsets.ModelViewSet):
    queryset = RAM.objects.all()
    serializer_class = RAMSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class PenyimpananViewSet(viewsets.ModelViewSet):
    queryset = Penyimpanan.objects.all()
    serializer_class = PenyimpananSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class KameraViewSet(viewsets.ModelViewSet):
    queryset = Kamera.objects.all()
    serializer_class = KameraSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class ChargerViewSet(viewsets.ModelViewSet):
    queryset = Charger.objects.all()
    serializer_class = ChargerSerializers
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializers
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'seri__merk': ['exact'],
    }
    http_method_names = ['get']

    @action(detail=False, methods=['get'], url_path='hijau_bulan_ini')
    def hijau_bulan_ini(self, request):
        bulan_ini = datetime.datetime.now().month
        tahun_ini = datetime.datetime.now().year
        queryset = Laptop.objects.filter(
            status_eco_friendly=True,
            created_at__month=bulan_ini,
            created_at__year=tahun_ini
        ).order_by('-created_at')[:1]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class KomentarViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Komentar.objects.all()
    http_method_names = ['get', 'post']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'laptop': ['exact']}


    def get_serializer_class(self):
        if self.action == 'create':
            return KomentarCreateSerializer
        return KomentarReadSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
