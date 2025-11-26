from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Especialidade, PerfilOficina, Problema

# 1. Configuração do Usuário Personalizado
# Usamos UserAdmin para manter a segurança de senhas e funcionalidades padrão
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Adiciona os campos booleanos ao formulário de edição do admin
    fieldsets = UserAdmin.fieldsets + (
        ('Tipo de Usuário', {'fields': ('is_cliente', 'is_oficina')}),
    )
    # Mostra colunas extras na lista de usuários
    list_display = ['username', 'email', 'first_name', 'is_cliente', 'is_oficina']
    list_filter = ['is_cliente', 'is_oficina', 'is_staff']

# 2. Configuração das Especialidades
@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# 3. Configuração do Perfil da Oficina
@admin.register(PerfilOficina)
class PerfilOficinaAdmin(admin.ModelAdmin):
    list_display = ('nome_oficina', 'usuario', 'endereco')
    search_fields = ('nome_oficina', 'endereco')
    # filter_horizontal cria uma interface melhor para selecionar várias especialidades
    filter_horizontal = ('especialidades',)

# 4. Configuração dos Problemas (Chamados)
@admin.register(Problema)
class ProblemaAdmin(admin.ModelAdmin):
    # Colunas visíveis na tabela
    list_display = ('titulo', 'modelo_carro', 'cliente', 'oficina_responsavel', 'status_colorido', 'data_criacao')
    # Filtros laterais
    list_filter = ('status', 'data_criacao', 'modelo_carro')
    # Barra de pesquisa
    search_fields = ('titulo', 'descricao', 'modelo_carro', 'cliente__username')
    # Permite clicar no status para editar direto na lista? (Opcional, descomente se quiser)
    # list_editable = ('status',)

    # Função auxiliar para mostrar a oficina (trata caso seja Null)
    def oficina_responsavel(self, obj):
        return obj.oficina.username if obj.oficina else "-"
    oficina_responsavel.short_description = 'Oficina Encarregada'

    # Função auxiliar para colorir o status (Visualização extra)
    @admin.display(description='Status')
    def status_colorido(self, obj):
        from django.utils.html import format_html
        colors = {
            'ABERTO': 'red',
            'ANDAMENTO': 'orange',
            'CONCLUIDO': 'green',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )