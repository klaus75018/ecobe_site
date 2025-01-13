from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
import openai
from django.contrib.auth.models import User
from .models import *
from .functions.tool1_functions import *


client = openai.OpenAI()

assistant_id = "asst_ZtaEiMKQNYt1IHjZvSixFOIO"
thread = client.beta.threads.create()
thread_id = thread.id
vs_id = "vs_YUuSw6fikktYVFeoDjTcIVOc"

def projects_overview(request):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    else:
        if request.method == 'POST':
            pass
        else:
            projects = User.objects.get(username=request.user.username).project_set.all()
            return render(request, 'console.html', {"projects":projects})


def incendie(request):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    else:
        if request.method == 'POST':
            user_message = request.POST["user_message"]

            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_message,
            )
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id, assistant_id=assistant_id
            )
            ai_messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))
            message_content = ai_messages[0].content[0].text


            messages.success(request,(f"REPONSE : \n\n {message_content.value}\n\n{thread_id}"))
            return redirect('incendie') 
        else:

            
            return render(request, 'conversations/incendie.html', {})
