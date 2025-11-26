from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Certifique-se de importar o CadastroUnificadoForm aqui
from .forms import CadastroUnificadoForm, ProblemaForm
from .models import Problema, User

def home(request):
    if request.user.is_authenticated:
        if request.user.is_cliente:
            return redirect('dashboard_cliente')
        elif request.user.is_oficina:
            return redirect('dashboard_oficina')
    return render(request, 'core/home.html')

# ESTA É A FUNÇÃO QUE ESTAVA FALTANDO
def signup(request):
    if request.method == 'POST':
        form = CadastroUnificadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redireciona baseado no tipo escolhido no cadastro
            if user.is_cliente:
                return redirect('dashboard_cliente')
            else:
                return redirect('dashboard_oficina')
    else:
        form = CadastroUnificadoForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard_cliente(request):
    # Lista apenas problemas deste cliente
    problemas = Problema.objects.filter(cliente=request.user).order_by('-data_criacao')
    
    if request.method == 'POST':
        # request.FILES é obrigatório para upload de imagens
        form = ProblemaForm(request.POST, request.FILES)
        if form.is_valid():
            problema = form.save(commit=False)
            problema.cliente = request.user
            problema.save()
            return redirect('dashboard_cliente')
    else:
        form = ProblemaForm()
    return render(request, 'core/dashboard_cliente.html', {'problemas': problemas, 'form': form})

@login_required
def dashboard_oficina(request):
    # 1. Problemas disponíveis no mercado (Sem oficina definida e Status Aberto)
    problemas_disponiveis = Problema.objects.filter(status='ABERTO', oficina__isnull=True)
    
    # 2. Problemas que ESTA oficina já pegou
    meus_servicos = Problema.objects.filter(oficina=request.user)
    
    return render(request, 'core/dashboard_oficina.html', {
        'problemas_disponiveis': problemas_disponiveis,
        'meus_servicos': meus_servicos
    })

@login_required
def pegar_servico(request, pk):
    problema = get_object_or_404(Problema, pk=pk)
    # Só pode pegar se ninguém pegou ainda e se o usuário for oficina
    if not problema.oficina and request.user.is_oficina:
        problema.oficina = request.user
        problema.status = 'ANDAMENTO'
        problema.save()
    return redirect('dashboard_oficina')

@login_required
def concluir_servico(request, pk):
    problema = get_object_or_404(Problema, pk=pk)
    # Só pode concluir se a oficina for a dona do serviço
    if problema.oficina == request.user:
        problema.status = 'CONCLUIDO'
        problema.save()
    return redirect('dashboard_oficina')