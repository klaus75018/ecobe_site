from django.test import TestCase
from aiecobe.functions.tool1_functions import *
from aiecobe.models import *
import openai
import json
import time
import logging
from datetime import datetime





# gets API Key from environment variable OPENAI_API_KEY
def NewAssistantVectorStore(assistant_id):
    client = openai.OpenAI()

    assistant_id = assistant_id

    vector_store = client.beta.vector_stores.create(name="Texte Securité Incendie")

    print(f"vector store is {vector_store.id}")

    # Ready the files for upload to OpenAI
    file_paths = ["aiecobe\initialisation_files\compléments_code_du_travail.docx","aiecobe\initialisation_files\ParcStationnementERP.pdf","aiecobe\initialisation_files\Arrêté du 31 janvier 1986.docx","aiecobe\initialisation_files\Arrêté_du_25_juin_1980.docx","aiecobe\initialisation_files\extrait_Code_du_Travail.pdf", "aiecobe\initialisation_files\compléments_code_du_travail.docx"]
    file_streams = [open(path, "rb") for path in file_paths]

    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
    )

    # You can print the status and the file counts of the batch to see the result of this operation.
    print(f"file batch is {file_batch.status}")
    print(file_batch.file_counts)

    assistant = client.beta.assistants.update(
    assistant_id=assistant_id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    print(f"assistant id is updated :  {assistant.id}")



