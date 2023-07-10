from extrato.models import Valores
from django.db.models import Sum
from datetime import datetime

def calcula_equilibrio_financeiro():
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False) 

    total_gastos_essenciais = gastos_essenciais.aggregate(Sum('valor'))['valor__sum']
    total_gastos_nao_essenciais = gastos_nao_essenciais.aggregate(Sum('valor'))['valor__sum']

    gastos_totais = total_gastos_essenciais + total_gastos_nao_essenciais
    
    percentual_gastos_essenciais = (total_gastos_essenciais/gastos_totais) * 100 if gastos_totais != 0 else 0
    percentual_gastos_nao_essenciais = (total_gastos_nao_essenciais/gastos_totais) * 100 if gastos_totais != 0 else 0

    return percentual_gastos_essenciais, percentual_gastos_nao_essenciais