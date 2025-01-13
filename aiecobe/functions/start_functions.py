import json

from openai import OpenAI
from aiecobe.functions.tool1_functions import *

def initialize(username, etude_name, project_name, buildings_qty):
    create_json(username, project_name, buildings_qty)
    vs_id = create_new_vs(etude_name)
    myfile = f"aiecobe/json_files/{username}_{project_name}.json"
    file_id = create_file_and_fill_vs(myfile,vs_id)
    thread_id = create_new_thread(vs_id)
    create_new_project_and_first_study(username, project_name, etude_name, thread_id, myfile, file_id, vs_id)
    maj_json(myfile, thread_id)
    AddNewJsonDB(project_name, thread_id, username, myfile)
    return thread_id

    


def maj_json(my_path, thread_id):
    import json
    with open(my_path, "r") as jjss:
        my_dic = json.load(jjss)
        my_dic["attributes"].append({"titre":"thread_id", "detail":thread_id})
        jjss.close()
    with open(my_path, "w") as newjson:
        json.dump(my_dic,newjson,indent=4)


def create_json(username, project_name, buildings_qty):
    with open(f"aiecobe/json_files/{username}_{project_name}.json", "w") as my_json:
        main = {"sujet":"Informations générales du projet", "children":[], "attributes":[]}
        batiments=[]
        for i in range(0,buildings_qty) :
            main["children"].append({"sujet":f"Informations bâtiment {i+1}", "children":[], "attributes":[]})
        main["attributes"].append({"titre":"project_name","detail":project_name})
        main["attributes"].append({"titre":"username","detail":username})
        json.dump(main, my_json, indent=4)
    


def create_new_project_and_first_study(username, project_name, etude_name, thread_id, json_file, json_id, vs_id):
    user = User.objects.get(username=username)
    user.save()
    myproject = user.project_set.create(name=project_name)
    myproject.save()
    myproject.json_db=json_file
    myproject.json_db_id=json_id
    myproject.save()
    myetude = myproject.etude_set.create(name = etude_name, thread_id=thread_id, vs_id =vs_id)
    myetude.save()

    
def create_new_thread(vs_id):
    from openai import OpenAI
    client = OpenAI()
    thread = client.beta.threads.create(tool_resources={"file_search": {"vector_store_ids": [vs_id]}})
    return thread.id

def create_new_vs(etude_name):
    from openai import OpenAI
    client = OpenAI()
    vector_store = client.beta.vector_stores.create(name=f"Données bâtiment pour analyse règlementation{etude_name}")
    return vector_store.id

def create_file_and_fill_vs(file_path,vs_id):
    from openai import OpenAI
    client = OpenAI()
    file_paths = [file_path]
    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vs_id, files=file_streams
    )


#    file = open(file_path, 'rb')
#    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#            vector_store_id=vs_id, files=[file]
#            )
#    file.close()
    

    file_list = []
    vector_store_files = client.beta.vector_stores.files.list(
                            vector_store_id=vs_id
                            )
    for vsfile in vector_store_files.data:
        file_list.append(vsfile.id)

    return file_list[0]
     