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
