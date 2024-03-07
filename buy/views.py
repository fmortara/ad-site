# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.db.models import Count, Q
# Model Forms.
from .forms import AskForm, RespostaForm
from django.contrib.auth.forms import User
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.core.mail import send_mail

# importing messages
from django.contrib import messages

from django.views import generic

from ads.models import Ads

# ask question view

def ask(request, pk):
    ads_detail = get_object_or_404(Ads, pk=pk)
    
    # If it is a POST, process the form data
    if request.method == 'POST':

        # Get advretsers email
        advertisers_email = ads_detail.author.user.email

        # Create an object instance of a question
        ask_instance = Question.objects.create()

        # Create a form instance and do the binding
        form = AskForm(request.POST)

        if form.is_valid():

            # Process the data in form.cleaned_data

            # Get Ads ID
            ask_instance.ads = ads_detail
            # Get asking name
            ask_instance.name = form.cleaned_data['name']
            # Get asking email
            ask_instance.from_email = form.cleaned_data['email']
            # Get asking phone
            ask_instance.phone = form.cleaned_data['phone']
            # Get asking message
            ask_instance.message = form.cleaned_data['message']
            # Save the question
            ask_instance.to_email = advertisers_email
            ask_instance.save()

            # Send email notificaton to Admin
            mail_subject = "[SITE TESTE] - Pergunta"
            sender_email = ask_instance.from_email

            # Monta a mensagem
            mensagem = "Prezado admin. Você tem uma mensagem para avaliar."
            message = mensagem
            # print(message)
            to_email = settings.EMAIL_HOST_USER
            to_list = [to_email]
            from_email = ask_instance.from_email
        
            send_mail(
                mail_subject,
                message,
                from_email,
                to_list,
                fail_silently=False,
            )

        return HttpResponseRedirect(reverse('ask-complete'))
    # If this is a GET or other method, create the default form
    else:
        if request.user.is_authenticated:
            form = AskForm(initial={'name': request.user.username, 
                                    'email': request.user.email})
        else:
            form = AskForm()
    
        # Create an object instance of a question
        # ask_instance = Question.objects.create()
    context = {
        'form': form,
        'ads_detail' : ads_detail,
        }    
    return render(request, 'buy/ask.html', context)

def ask_complete(request):
    return render(request, 'buy/ask-complete.html')

class QuestionListView(generic.ListView):
    model = Question
    context_object_name = 'question_list'
    queryset = Question.objects.filter(status = 'Nova')

def message_admin(request):
    if request.method == 'GET':   # Checks for "Nova", changes to "Em processo" and loads the list
        status_temporario_q = Question.objects.filter(status = 'Nova').update(status='Em processo')
        questionList = Question.objects.filter(status = 'Em processo')
        status_temporario_a = Answer.objects.filter(status='Nova').update(status='Em processo')
        answerList = Answer.objects.filter(status='Em processo')
        context = {'question_list': questionList, 'answer_list': answerList}
        return render(request, 'buy/question_list.html', context)
    else:  # Action from the list - either 'aprova' to all items in page or 'reprova' to a single item
        if request.POST.get('reprova'):
            pk = request.POST.get('reprova')
            item = 'pergunta'
        elif request.POST.get('reprova_a'):
            pk = request.POST.get('reprova_a')
            item = 'resposta'
        aprova = request.POST.get('aprova')
        if aprova == '0':   # Usuário clicou em aprovar as restantes
            aprovar_q = Question.objects.filter(status = 'Em processo').update(status='Aprovada', approved=True)
            status_temporario_q = Question.objects.filter(status='Nova').update(status='Em processo')
            aprovar_a = Answer.objects.filter(status='Em processo').update(status='Aprovada', approved=True)
            status_temporario_a = Answer.objects.filter(status='Nova').update(status='Em processo')
            ##############################################################################
            # ROTINA PARA ENCAMINHAR AS MENSAGENS PARA SEUS DESTINATARIOS
            aprovadaList = Question.objects.filter(status='Aprovada')
            for item in aprovadaList:
                message0 = "Prezado/a: "
                message1 = str(item.ads.author.user.username)
                message2 = "Você tem uma mensagem de um interessado no item "
                message3 = str(item.ads.title)
                message4 = "Link para a pergunta - a ser implementado"
                message = message0 + message1 + "\n \n" + message2 + "\n " + message3 + "\n " + message4
                nome = item.name
                email_interessado = item.from_email
                email_anunciante = item.to_email
                to_list = [item.to_email,]
                mail_subject = "Nós e as Minas - Chegou mensagem para você"
                from_email = settings.EMAIL_HOST_USER

                send_mail(
                    mail_subject,
                    message,
                    from_email,
                    to_list,
                    fail_silently=False,
                )
            # Muda status para Aguardando Resposta
            status_temporario = Question.objects.filter(status='Aprovada').update(status='Aguardando Resposta')

            ##############################################################################
            status_temporario_q = Question.objects.filter(status='Nova').update(status='Em processo')
            questionList = Question.objects.filter(status='Em processo')
            status_temporario_a = Answer.objects.filter(status='Nova').update(status='Em processo')
            answerList = Answer.objects.filter(status='Em processo')
            context = {'question_list': questionList, 'answer_list': answerList}
            return render(request, 'buy/question_list.html', context)
        else:
            if item=='pergunta':
                question = get_object_or_404(Question, pk=pk)
                question.status = 'Reprovado'
                question.save()
            elif item=='resposta':
                answer = get_object_or_404(Answer, pk=pk)
                answer.status = 'Reprovado'
                answer.save()
            ###############################################################################
            # Send email notificaton to Admin
            mail_subject = "[SITE TESTE] - Sua mensagem não foi aprovada"
            sender_email = settings.EMAIL_HOST_USER

            # Monta a mensagem
            mensagem0 = "Prezada/o "
            if item=='pergunta':
                mensagem1 = str(question.name)
            elif item=='resposta':
                mensagem1 = str(answer.nome)


            mensagem2 = "Sua mensagem no site Nós e as Minas foi rejeitada por violar as regras\n" \
            "de comunicação entre anunciante e comprador. Por favor, refazer a mensagem \n" \
            "sem utilizar números de telefone, email ou outros modos de contato. \n" \
            "Se houver entendimento entre as partes, o Nós e as Minas entrega os dados de \n" \
            "contato automaticamente, sem qualquer custo.\n" \
            "A mensagem em referencia é:\n\n"
            if item=='pergunta':
                mensagem3 = str(question.message)
            elif item=='resposta':
                mensagem3 = str(answer.mensagem)
            link = "<a href='{% url 'ads-detail' question.ads.id %}'>"
            mensagem4 = "O anúncio é esse: " + link
            message = mensagem0 + "  " + mensagem1 + "\n\n" + mensagem2 + mensagem3 + "\n\n" + mensagem4
            if item=='pergunta':
                to_email = question.from_email
            elif item=='resposta':
                to_email = answer.question.to_email
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER

            send_mail(
                mail_subject,
                message,
                from_email,
                to_list,
                fail_silently=False,
            )
            ################################################################################

            status_temporario_q = Question.objects.filter(status='Nova').update(status='Em processo')
            questionList = Question.objects.filter(status='Em processo')
            status_temporario_a = Answer.objects.filter(status='Nova').update(status='Em processo')
            answerList = Answer.objects.filter(status='Em processo')
            context = {'question_list': questionList, 'answer_list': answerList}
            return render(request, 'buy/question_list.html', context)

##################################################################################################################
# View para listar todas as mensagens pendentes do usuário
# O template lista as mensagens e apresenta um textbox
# para o usuário responder, e um botão - RESPONDER
# A lista tem que ter o título do anúncio e o nome do usuário e a pergunta.
# Ver se no template dá para listar todas as mensagens do usuário.
# Clicando RESPONDER, a view grava a resposta no BD e manda um alerta para quem
# fez a pergunta, que vai ver o mesmo tipo de tela quando acessar
@login_required
def message_reply(request):
    if request.method == 'GET':   # Monta a lista de mensagens pendentes
        question_list = Question.objects.filter(status='Aguardando Resposta').filter(to_email=request.user.email)
        context = {'question_list': question_list}
        return render(request, 'buy/approved_list.html', context)

    elif request.POST.get('responde') is not None:  # Action from the list - click on "responde"

        question_id = int(request.POST['responde'])
        approved_question_instance = get_object_or_404(Question, id=question_id)

        # Create a form instance and do the binding
        form = RespostaForm(request.POST)
        context = {'form': form, 'approved_question_instance': approved_question_instance}
        return render(request, 'buy/approved_list.html', context)

    else:  # request.POST[responde] é None, mas request.POST[grava_resposta] é válido

        question_id = int(request.POST['grava_resposta'])

        form = RespostaForm(request.POST)
        if form.is_valid():

            # Creates an answer instance
            resposta = Answer.objects.create(question_id=question_id)

            # Process the data in form.cleaned_data
            # Get answer text
            resposta.nome = request.user.username
            resposta.mensagem = form.cleaned_data['message']
            resposta.data_resp = date.today()
            resposta.save()

            # Muda status da pergunta, de 'Aguardando Resposta' para 'Respondida'
            salvando = Question.objects.filter(id=question_id).update(status='Respondida')

#           Monta nova lista de perguntas sem resposta e volta para a tela
            question_list = Question.objects.filter(status='Aguardando Resposta').filter(to_email=request.user.email)
            context = {'question_list': question_list}
            return render(request, 'buy/approved_list.html', context)