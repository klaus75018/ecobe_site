import json
import requests
import openai
from openai import OpenAI
from pydantic import BaseModel
from Ass_Secu_Incendie_Instr import instructions

client = OpenAI()

assistant = client.beta.assistants.create(
name="Assistant expert en Securité Incendie",
instructions=instructions,
model="gpt-4o-mini",
tools=[{"type": "file_search"},{
    "type":"function","function": {
        "name": "mise_a_jour_informations_projet",
        "description": "Informations détaillées sur le site étudiée, enrichie à chaque nouvelle information collectée en conservant les anciennes",
        "parameters": {
            "type": "object",
            "properties": {
                "sujet": {
                    "type": "string",
                    "description": "Le sujet sur lequel porte la ou les informations"
                    
                },
                "children": {
                    "type": "array",
                    "description": "Sous sujets dans un sujet",
                    "items": {
                        "$ref": "#"
                    }
                },
                "attributes": {
                    "type": "array",
                    "description": "Informations collectée dans un sujet ou un sous-sujet",
                    "items": {
                        "type": "object",
                        "properties": {
                            "titre": {
                                "type": "string",
                                "description": "titre de l'information collectée"
                            },
                            "detail": {
                                "type": "string",
                                "description": "détail de l'information collectée"
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