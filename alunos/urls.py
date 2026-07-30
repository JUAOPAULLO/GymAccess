from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),

    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('editar/<int:id>/', views.editar_aluno, name='editar_aluno'),
    path('excluir/<int:id>/', views.excluir_aluno, name='excluir_aluno'),
    path('pacotes/', views.lista_pacotes, name='lista_pacotes'),
    path('pacotes/cadastrar/',views.cadastrar_pacote,name='cadastrar_pacote'),
    path('pacotes/editar/<int:id>/',views.editar_pacote,name='editar_pacote'),
    path('pacotes/excluir/<int:id>/',views.excluir_pacote,name='excluir_pacote'),
    path('qrcode/gerar/<int:pacote_id>/',views.gerar_qrcode,name='gerar_qrcode'),
    path('qrcode/validar/<uuid:token>/',views.validar_qrcode,name='validar_qrcode'),
    path('registros/',views.lista_registros,name='lista_registros'),
]