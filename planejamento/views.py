from django.shortcuts import render
from perfil.models import Categoria
from datetime import datetime
from extrato.models import Valores
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'valor': f'Recebi o valor {novo_valor}'})

def ver_planejamento(request):
    categorias = Categoria.objects.all()
    valores = Valores.objects.all()

    valor_total = sum(valor.valor for valor in valores.filter(data__month=datetime.now().month) if valor.tipo == 'S')
    planejamento_total = sum(categoria.valor_planejamento for categoria in categorias)
    percentual_total_gastos = int((valor_total/planejamento_total) * 100) if planejamento_total != 0 else 0
    return render(request, 'ver_planejamento.html', {'categorias': categorias, 'valor_total': valor_total, 'planejamento_total': planejamento_total, 'percentual_total_gastos': percentual_total_gastos})