from django.contrib import admin
from .models import Aluno, PacoteAcesso, QRCodeAcesso, RegistroAcesso


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "cpf",
        "telefone",
        "ativo",
    )

    search_fields = (
        "nome",
        "cpf",
    )


@admin.register(PacoteAcesso)
class PacoteAcessoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "aluno",
        "total_acessos",
        "acessos_restantes",
        "ativo",
        "data_compra",
    )

    list_filter = (
        "ativo",
        "data_compra",
    )

    search_fields = (
        "aluno__nome",
    )

    @admin.display(description='codigo')
    def codigo(self, obj):
        return obj.id
    
    
@admin.register(QRCodeAcesso)
class QRCodeAcessoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'aluno',
        'pacote',
        'usado',
        'criado_em',

    )

    readonly_fields = (
        'token',
        'criado_em',

    )

@admin.register(RegistroAcesso)
class RegistroAcessoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "aluno",
        "pacote",
        "autorizado",
        "data_hora",
    )

    list_filter = (
        "autorizado",
        "data_hora",
    )

    search_fields = (
        "aluno__nome",
    )

    ordering = (
        "-data_hora",
    )