from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime

def definir_contas(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})

    titulo = request.POST.get('titulo')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    valor = request.POST.get('valor')
    dia_pagamento = request.POST.get('dia_pagamento')

    conta = ContaPagar(
        titulo = titulo, 
        categoria_id = categoria, 
        descricao = descricao,
        valor = valor, 
        dia_pagamento = dia_pagamento
    )

    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/contas/definir_contas')

def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    meses = {
        '1': 'Janeiro', 
        '2': 'Fevereiro',
        '3': 'Março',
        '4': 'Abril',
        '5': 'Maio',
        '6': 'Junho',
        '7': 'Julho',
        '8': 'Agosto',
        '9': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro'   
    }

    mes_atual_nome = ''

    for key, value in meses.items():
        if int(key) == MES_ATUAL:
            mes_atual_nome = value

    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)

    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)

    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    total_contas_proximas_vencimento = len(contas_proximas_vencimento)
    total_contas_vencidas = len(contas_vencidas)
    total_restantes = len(restantes)
    total_contas_pagas = len(contas_pagas)

    return render(request, 'ver_contas.html', {'mes_atual': mes_atual_nome, 
                                               'contas_vencidas': contas_vencidas, 
                                               'contas_proximas_vencimento': contas_proximas_vencimento, 
                                               'restantes': restantes,
                                               'total_contas_proximas_vencimento': total_contas_proximas_vencimento,
                                               'total_contas_vencidas': total_contas_vencidas,
                                               'total_restantes': total_restantes,
                                               'total_contas_pagas': total_contas_pagas
                                               })  

def pagar_conta(request, id):
    conta = ContaPagar.objects.get(id=id)
    data_atual = datetime.now()

    conta_paga = ContaPaga(
        conta_id=conta.id, 
        data_pagamento=data_atual
    )

    conta_paga.save()

    return redirect('/contas/ver_contas')