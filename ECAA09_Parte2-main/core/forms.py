from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Problema

class CadastroUnificadoForm(UserCreationForm):
    # Campo extra para escolher o tipo de usuário via Radio Button
    TIPO_CHOICES = (
        ('CLIENTE', 'Sou Cliente'),
        ('OFICINA', 'Sou Oficina/Escritório'),
    )
    tipo_usuario = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        widget=forms.RadioSelect,
        label="Tipo de Conta"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Adiciona campos padrões do UserCreationForm + email (opcional)
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        tipo = self.cleaned_data['tipo_usuario']
        
        # Define as permissões baseadas na escolha
        if tipo == 'CLIENTE':
            user.is_cliente = True
            user.is_oficina = False
        else:
            user.is_oficina = True
            user.is_cliente = False
        
        if commit:
            user.save()
        return user

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        # Inclui o campo 'imagem' para o upload
        fields = ['titulo', 'modelo_carro', 'descricao', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Motor falhando'}),
            'modelo_carro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiat Uno 2010'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }