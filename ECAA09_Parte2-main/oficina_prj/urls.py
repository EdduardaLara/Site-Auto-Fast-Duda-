from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Cadastro: Mudei para 'signup' (sem _cliente) para usar a tela unificada
    path('cadastro/', views.signup, name='signup'),
    
    # Paineis
    path('painel/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('painel/oficina/', views.dashboard_oficina, name='dashboard_oficina'),
    
    # Ações de Serviço
    path('servico/<int:pk>/pegar/', views.pegar_servico, name='pegar_servico'),
    path('servico/<int:pk>/concluir/', views.concluir_servico, name='concluir_servico'),
]

# Configuração OBRIGATÓRIA para carregar as imagens enviadas pelos usuários
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)