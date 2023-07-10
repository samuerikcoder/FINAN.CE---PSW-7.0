from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from extrato.models import Valores
from datetime import datetime
from .utils import calcula_equilibrio_financeiro
from contas.models import ContaPagar, ContaPaga

def home(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)

    qtd_contas_vencidas = len(contas_vencidas)
    qtd_contas_proximas_vencimento = len(contas_proximas_vencimento)

    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = sum(entrada.valor for entrada in entradas)
    total_saidas = sum(saida.valor for saida in saidas)
    total_livre = total_entradas - total_saidas

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    contas = Conta.objects.all()
    total_contas = sum(conta.valor for conta in contas)

    return render(request, 'home.html', {'contas': contas, 
                                         'total_contas': total_contas,
                                         'total_entradas': total_entradas,
                                         'total_saidas': total_saidas,
                                         'total_livre': total_livre,
                                         'percentual_gastos_essenciais': int(percentual_gastos_essenciais),
                                         'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais),
                                         'qtd_contas_proximas_vencimento': qtd_contas_proximas_vencimento,
                                         'qtd_contas_vencidas': qtd_contas_vencidas
                                         })

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    total_contas = sum(conta.valor for conta in contas)
    
    banco_options =  (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('BR', 'Bradesco'),
        ('ST', 'Santander'),
        ('IN', 'Inter'),
        ('IT', 'Iti'),
        ('IU', 'Itau'),
        ('C6', 'C6Bank')
    )
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas':total_contas, 'categorias': categorias, 'banco_options': banco_options})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0 or len(tipo.strip()) == 0 or len(valor.strip()) == 0 or icone is None:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    try:
        valor = float(valor)
    except ValueError:
        messages.add_message(request, constants.ERROR, 'O campo valor deve ser do tipo numérico')
        return redirect('/perfil/gerenciar/')

    if tipo not in ['pf', 'pj']:
        messages.add_message(request, constants.ERROR, 'Tipo inválido!')
        return redirect('/perfil/gerenciar/')

    if banco not in ['NU', 'CE', 'BR']:
        messages.add_message(request, constants.ERROR, 'Banco inválido!')
        return redirect('/perfil/gerenciar/')
    
    if len(apelido) > 50:
        messages.add_message(request, constants.ERROR, 'O campo apelido não deve ultrapassar 50 caracteres!')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido = apelido, 
        banco = banco, 
        tipo = tipo,
        valor = valor, 
        icone = icone
    )

    conta.save() 

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if nome == '' or len(nome) < 0 or type(essencial) != bool:
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria = nome, 
        essencial = essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')

def dashboard(request):
    from extrato.models import Valores
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})