from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from veterinaria.views.health     import health_check, testing_cicd
from veterinaria.views.auth       import RegisterView, LogoutView
from veterinaria.views.user       import UserViewSet
from veterinaria.views.cliente    import ClienteViewSet
from veterinaria.views.mascota    import MascotaViewSet
from veterinaria.views.veterinario import VeterinarioViewSet
from veterinaria.views.cita       import CitaViewSet
from veterinaria.views.historial  import HistorialMedicoViewSet
from veterinaria.views.servicio   import ServicioViewSet
from veterinaria.views.factura    import FacturaViewSet
from veterinaria.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users',         UserViewSet,          basename='user')
router.register('clientes',      ClienteViewSet,       basename='cliente')
router.register('mascotas',      MascotaViewSet,       basename='mascota')
router.register('veterinarios',  VeterinarioViewSet,   basename='veterinario')
router.register('citas',         CitaViewSet,          basename='cita')
router.register('historial',     HistorialMedicoViewSet, basename='historial')
router.register('servicios',     ServicioViewSet,      basename='servicio')
router.register('facturas',      FacturaViewSet,       basename='factura')

urlpatterns = [
    path('health/',             health_check),
    path('testing-cicd/',       testing_cicd),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]