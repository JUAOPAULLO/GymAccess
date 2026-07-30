from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone

from .models import (
    Aluno,
    PacoteAcesso,
    QRCodeAcesso,
    RegistroAcesso,
)


def home(request):

    total_alunos = Aluno.objects.count()

    pacotes_ativos = PacoteAcesso.objects.filter(
        ativo=True
    ).count()

    total_registros = RegistroAcesso.objects.count()

    ultimos_registros = (
    RegistroAcesso.objects
    .select_related("aluno")
    .order_by("-data_hora")[:5]
)

    qrcodes_ativos = QRCodeAcesso.objects.filter(
        usado=False
    ).count()

    contexto = {
        "total_alunos": total_alunos,
        "pacotes_ativos": pacotes_ativos,
        "total_registros": total_registros,
        "qrcodes_ativos": qrcodes_ativos,
        'ultimos_registros':ultimos_registros,
    }

    return render(
        request,
        "alunos/home.html",
        contexto
    )


def lista_alunos(request):

    alunos = Aluno.objects.all().order_by("nome")

    paginator = Paginator(alunos, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "alunos/lista_alunos.html",
        {
            "page_obj": page_obj,
        }
    )


def cadastrar_aluno(request):

    if request.method == 'POST':

        nome = request.POST['nome']
        cpf = request.POST['cpf']
        telefone = request.POST['telefone']
        email = request.POST['email']

        Aluno.objects.create(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            email=email
        )

        messages.success(
            request,
            'Aluno cadastrado com sucesso!'
        )

        return redirect('lista_alunos')

    return render(
        request,
        'alunos/cadastrar_aluno.html'
    )


def editar_aluno(request, id):

    aluno = get_object_or_404(
        Aluno,
        id=id
    )

    if request.method == 'POST':

        aluno.nome = request.POST['nome']
        aluno.cpf = request.POST['cpf']
        aluno.telefone = request.POST['telefone']
        aluno.email = request.POST['email']

        aluno.save()

        messages.success(
            request,
            'Aluno atualizado com sucesso!'
        )

        return redirect('lista_alunos')

    return render(
        request,
        'alunos/editar_aluno.html',
        {
            'aluno': aluno
        }
    )


def excluir_aluno(request, id):

    aluno = get_object_or_404(
        Aluno,
        id=id
    )

    if request.method == 'POST':

        aluno.delete()

        messages.success(
            request,
            'Aluno excluído com sucesso!'
        )

        return redirect('lista_alunos')

    return render(
        request,
        'alunos/excluir_aluno.html',
        {
            'aluno': aluno
        }
    )


def lista_pacotes(request):

    pacotes = PacoteAcesso.objects.select_related(
        "aluno"
    ).order_by("aluno__nome")

    paginator = Paginator(pacotes, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "alunos/lista_pacotes.html",
        {
            "page_obj": page_obj,
        }
    )


def cadastrar_pacote(request):

    alunos = Aluno.objects.all()

    if request.method == 'POST':

        aluno = get_object_or_404(
            Aluno,
            id=request.POST['aluno']
        )

        total = int(
            request.POST['total_acessos']
        )

        PacoteAcesso.objects.create(
            aluno=aluno,
            total_acessos=total,
            acessos_restantes=total,
            ativo=True
        )

        messages.success(
            request,
            'Pacote cadastrado com sucesso!'
        )

        return redirect('lista_pacotes')

    return render(
        request,
        'alunos/cadastrar_pacote.html',
        {
            'alunos': alunos
        }
    )


def editar_pacote(request, id):

    pacote = get_object_or_404(
        PacoteAcesso,
        id=id
    )

    alunos = Aluno.objects.all()

    if request.method == 'POST':

        pacote.aluno = get_object_or_404(
            Aluno,
            id=request.POST['aluno']
        )

        pacote.total_acessos = int(
            request.POST['total_acessos']
        )

        pacote.acessos_restantes = int(
            request.POST['acessos_restantes']
        )

        pacote.ativo = request.POST.get('ativo') == 'on'

        pacote.save()

        messages.success(
            request,
            'Pacote atualizado com sucesso!'
        )

        return redirect('lista_pacotes')

    return render(
        request,
        'alunos/editar_pacote.html',
        {
            'pacote': pacote,
            'alunos': alunos
        }

    )

def excluir_pacote(request, id):

    pacote = get_object_or_404(
        PacoteAcesso,
        id=id
    )

    if request.method == "POST":

        pacote.delete()

        messages.success(
            request,
            "Pacote excluído com sucesso!"
        )

        return redirect("lista_pacotes")

    return render(
        request,
        "alunos/excluir_pacote.html",
        {
            "pacote": pacote
        }
    )

def gerar_qrcode(request, pacote_id):

    pacote = get_object_or_404(
        PacoteAcesso,
        id=pacote_id
    )

    if not pacote.ativo:

        messages.error(
            request,
            "Este pacote está inativo."
        )

        return redirect("lista_pacotes")

    qrcode = QRCodeAcesso.objects.create(

        aluno=pacote.aluno,

        pacote=pacote

    )

    return render(
    request,
    "alunos/exibir_qrcode.html",
    {
        "qrcode": qrcode
    }

)

def validar_qrcode(request, token):

    qrcode = get_object_or_404(
        QRCodeAcesso,
        token=token
    )

    #verifica se o qrcode expirou
    if qrcode.valido_ate and timezone.now() > qrcode.valido_ate:

        return render(
            request,
            'alunos/validacao_qrcode.html',
            {
                'qrcode': qrcode,
                'mensagem': 'QR Code expirado.',
                'sucesso': False
            }
        )

    # Verifica se o QR Code já foi utilizado
    if qrcode.usado:

        return render(
            request,
            "alunos/validacao_qrcode.html",
            {
                "qrcode": qrcode,
                "mensagem": "QR Code já foi utilizado.",
                "sucesso": False
            }
        )

    pacote = qrcode.pacote

    # Verifica se o pacote está ativo
    if not pacote.ativo:

        return render(
            request,
            "alunos/validacao_qrcode.html",
            {
                "qrcode": qrcode,
                "mensagem": "Pacote inativo.",
                "sucesso": False
            }
        )

    # Marca o QR Code como utilizado
    qrcode.usado = True
    qrcode.save()

    # Diminui um acesso do pacote
    pacote.acessos_restantes -= 1

    # Se acabou os acessos, desativa o pacote
    if pacote.acessos_restantes <= 0:

        pacote.acessos_restantes = 0
        pacote.ativo = False

    pacote.save()

    RegistroAcesso.objects.create(
        aluno=qrcode.aluno,
        pacote=pacote,
        autorizado=True
    )

    return render(
        request,
        "alunos/validacao_qrcode.html",
        {
            "qrcode": qrcode,
            "mensagem": "Entrada liberada.",
            "sucesso": True
        }
    )

def lista_registros(request):
    registros = RegistroAcesso.objects.select_related(
        "aluno",
        "pacote"
    ).order_by("-data_hora")

    paginator = Paginator(registros, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "alunos/lista_registros.html",
        {
            "page_obj": page_obj,
        }
    )