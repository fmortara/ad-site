from django.db import models
from ckeditor.fields import RichTextField
from ads.models import Ads


# Create your models here.
# Ask Model
class Question(models.Model):
    
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20)
    from_email = models.EmailField(max_length=50)
    to_email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    message = RichTextField(help_text='O texto não pode conter endereços de email ou números de telefone')
    rel_message = models.BigIntegerField(null=True, blank=True)
    data_cria = models.DateTimeField(auto_now=True, verbose_name='Data de Criação')
    data_visu = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, default='Nova')
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return (self.name) + (str(self.data_cria))
                
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    data_resp = models.DateTimeField(auto_now=True)
    mensagem = RichTextField(help_text='O texto não pode conter endereços de email ou números de telefone')
    nome = models.CharField(max_length=20)
    status = models.CharField(max_length=10, default='Nova')
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Respostas"
    
    def __str__(self):
        return (self.nome) + (str(self.data_resp))
                 
