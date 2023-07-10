from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from django.http import FileResponse
from datetime import datetime, timedelta
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO

def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
    
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        valores = Valores(
            valor=valor, 
            categoria_id=categoria, 
            descricao=descricao, 
            data=data, 
            conta_id=conta, 
            tipo=tipo
        )

        valores.save()

        conta = Conta.objects.get(id=conta)
        
        if tipo == 'E':
            conta.valor += int(valor)
            mensagem_sucesso = 'Entrada cadastrada com sucesso!'
        elif tipo == 'S':
            conta.valor -= int(valor)
            mensagem_sucesso = 'Saída cadastrada com sucesso!'

        conta.save()

        messages.add_message(request, constants.SUCCESS, mensagem_sucesso)
        return redirect('/extrato/novo_valor')
    
def view_extrato(request, reset_filters=False):
    if reset_filters:
        return redirect('view_extrato')
    
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.filter(data__month=datetime.now().month)

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    periodo_get = request.GET.get('periodo')

    if conta_get:
        valores = valores.filter(conta_id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria_id=categoria_get)
    if periodo_get:
        valores = valores.filter(data__gte=datetime.now() - timedelta(days=7))

    return render(request, 'view_extrato.html', {'contas': contas, 'categorias': categorias, 'valores': valores})

def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores': valores})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    return FileResponse(path_output, filename='extrato.pdf')