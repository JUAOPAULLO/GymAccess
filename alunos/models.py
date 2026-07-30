import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from io import BytesIO
import qrcode
from django.core.files.base import ContentFile


# Create your models here.

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    ativo = models.BooleanField(default=True)
    
    data_cadastro = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.nome
    
class PacoteAcesso(models.Model):

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE
    )

    total_acessos = models.IntegerField()

    acessos_restantes = models.IntegerField()

    ativo = models.BooleanField(default=True)

    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.acessos_restantes}/{self.total_acessos} acessos"

    
class QRCodeAcesso(models.Model):

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    imagem = models.ImageField(
        upload_to='qrcodes/',
        blank=True,
        null=True
    )

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE
    )

    pacote = models.ForeignKey(
        PacoteAcesso,
        on_delete=models.CASCADE
    )

    usado = models.BooleanField(
        default=False
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    valido_ate = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.aluno.nome} - {self.token}"

    def gerar_qrcode(self):

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(str(self.token))
        qr.make(fit=True)

        imagem = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        buffer = BytesIO()

        imagem.save(buffer, format="PNG")

        nome_arquivo = f"qr_{self.token}.png"

        self.imagem.save(
            nome_arquivo,
            ContentFile(buffer.getvalue()),
            save=False
        )

    def save(self, *args, **kwargs):

        novo = self.pk is None

        if novo and not self.valido_ate:
            self.valido_ate = timezone.now() + timedelta(seconds=30)

        super().save(*args, **kwargs)

        if novo and not self.imagem:

            self.gerar_qrcode()

            super().save(update_fields=["imagem"])

            
class RegistroAcesso(models.Model):

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE
    )

    pacote = models.ForeignKey(
        PacoteAcesso,
        on_delete=models.CASCADE
    )

    data_hora = models.DateTimeField(
        auto_now_add=True
    )

    autorizado = models.BooleanField(
        default=True
    )

    def __str__(self):

        status = "Liberado" if self.autorizado else "Negado"

        return f"{self.aluno.nome} - {status} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"