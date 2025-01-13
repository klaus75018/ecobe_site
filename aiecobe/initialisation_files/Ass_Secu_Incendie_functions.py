import json
import requests
import openai
from openai import OpenAI
from aiecobe.initialisation_files.Ass_Secu_Incendie_Instr import instructions

def NewAssIncendie():


    client = OpenAI()

    assistant = client.beta.assistants.create(
    name="Assistant expert en Securité Incendie",
    instructions=instructions,
    model="gpt-4o-mini",
    tools=[{"type": "file_search"},{
        "type":"function","function": {
            "name": "mise_a_jour_informations_projet",
            "description": "Permet de mettre à jour la base de donnée regroupant les informations sur le projet. Si tu utilises un sujet déjà existant, les  informations founies lors de l'appel de la fonction seront stockées à cet étage de la base de donnée.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sujet": {
                        "type": "string",
                        "description": "Le sujet sur lequel porte la ou les informations que tu veux fournir"
                        
                    },
                    "children": {
                        "type": "array",
                        "description": "Sous-sujet(s) dans un sujet",
                        "items": {
                            "$ref": "#"
                        }
                    },
                    "attributes": {
                        "type": "array",
                        "description": "Informations collectée concernant le sujet.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "titre": {
                                    "type": "string",
                                    "description": "titre de l'information collectée"
                                },
                                "detail": {
                                    "type": "string",
                                    "description": "détails de l'information collectée"
                                }
                            },
                            "required": ["titre", "detail"],
                            "additionalProperties": False
                            
                        },
                    },
                },
                "required": ["sujet", "children", "attributes"],
                "additionalProperties": False
            },
            "strict":True,
        }
    }]
    )
    print(assistant.id)