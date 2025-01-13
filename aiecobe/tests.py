from django.test import TestCase
from aiecobe.functions.tool1_functions import *
import json
from aiecobe.models import *
import openai

import time
import logging
from datetime import datetime
from openai import OpenAI




# gets API Key from environment variable OPENAI_API_KEY
client = openai.OpenAI()

assistant_id = "asst_ySyb2MWFvv6oaz7yVr0pfmzc"
thread_id = "thread_oksXjeJvJoxGV5o7tVKnurxk"



def newMessage(myMessage, client, thread_id, assistant_id):
    

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=myMessage,
    )
    print(message)
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="please adress the user as KLaus. If new informations concerning the building(s) of the project are given, use the given function to store them in our database.",
    )
    print(run)
    return run.id


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == "completed":
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
            elif run.status == "requires_action":
                print(run.status)
                requiered_actions = run.required_action.submit_tool_outputs.model_dump()
                print(requiered_actions)
                tool_output = []
                for action in requiered_actions["tool_calls"]:
                    function_name = action["function"]["name"]
                    arguments = json.loads(action["function"]["arguments"])

                    if function_name == "mise_a_jour_informations_projet":
                        print("coucou")
                        output = mise_a_jour_informations_projet(arguments["sujet"], arguments["children"], arguments["attributes"])
                        print("coucou2")
                        tool_output.append({
                            "tool_call_id" : action["id"],
                             "output" : output
                        })
                        print("coucou3")
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id = thread_id,
                    run_id = run_id,
                    tool_outputs = tool_output
                )

            else:
               print("atre chose")
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

while True:
    print("donner une entrée")
    a = str(input())
    if a != "Fin!":
       try:
           run_id = newMessage(a, client=client, thread_id=thread_id, assistant_id=assistant_id)
           print(run_id)
           wait_for_run_completion(client=client, thread_id=thread_id, run_id=run_id)
       except Exception as e:
           print("il y a eu une erreur...")
           print(e)
    else:
        print("c'est fini")
        break
        
