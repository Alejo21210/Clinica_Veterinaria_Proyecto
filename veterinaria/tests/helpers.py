from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from veterinaria.models import Cliente, Mascota, Veterinario, Cita, Servicio


def create_user(username='user', email=None, password='Pass1234!', **kwargs):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )


def create_staff(username='staff', email=None, password='Admin1234!'):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, is_staff=True
    )


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def auth_client(user):
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client


def create_cliente(user, telefono='0999999999', direccion='Direccion test'):
    return Cliente.objects.get_or_create(
        user=user,
        defaults={'telefono': telefono, 'direccion': direccion},
    )[0]


def create_mascota(nombre='Firulais', especie='perro', raza='Labrador',
                   cliente=None, is_active=True):
    if cliente is None:
        user = create_user('dueno')
        cliente = create_cliente(user)
    return Mascota.objects.create(
        nombre=nombre, especie=especie, raza=raza,
        cliente=cliente, is_active=is_active,
    )


def create_veterinario(nombre='Juan Gomez', especialidad='Cirugia',
                       telefono='0988888888', email='vet@test.com'):
    return Veterinario.objects.create(
        nombre=nombre, especialidad=especialidad,
        telefono=telefono, email=email,
    )


def create_cita(mascota=None, veterinario=None, fecha='2026-06-15',
                hora='10:00', estado='pendiente'):
    if mascota is None:
        mascota = create_mascota()
    if veterinario is None:
        veterinario = create_veterinario()
    return Cita.objects.create(
        mascota=mascota, veterinario=veterinario,
        fecha=fecha, hora=hora, motivo='Consulta general',
        estado=estado,
    )


def create_servicio(nombre='Consulta General', precio=25.00):
    return Servicio.objects.create(
        nombre=nombre, precio=precio,
        descripcion='Atencion veterinaria general',
    )
