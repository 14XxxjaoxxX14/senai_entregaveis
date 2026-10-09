from django.shortcuts import render
from .models import Tarefas

def index(request):
    tarefas = Tarefas.objects.all()
    return render(request, 'core/index.html', {'tarefas': tarefas})

