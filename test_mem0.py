from dotenv import load_dotenv
from mem0 import MemoryClient
import logging 
import json


load_dotenv()
user_name ='Ausaaf'
mem0 = MemoryClient()

def add_memory():

    messages_formatted = [
        {        "role": "user",
            "content": "I really like old musics."
        },
        {  
             "role": "assistant",
            "content": "that is a good choise."
        },
        {  
             "role": "user",
            "content": "i think so too,"
        },
        {  
             "role":"assistant",
            "content": "what is your favorite song by them?"
        },
    ]

    mem0.add(messages_formatted, user_id="Ausaaf")

def get_memory_by_query():
    mem0 = MemoryClient()
    query = "what are {user_name}'s preferences?"
    result = mem0.search(query, user_id =user_name) 

    memories = [
            {
                "memory": result["memory"],
                "updated_at": result["updated_at"]
             }
             for result in result 
         ]
    memories_str =json.dumps(memories)
    print(f"Memories: {memories_str}")
    return memories_str


if __name__ =="__main__":
    logging.basicConfig(level=logging.INFO)
    add_memory()
    get_memory_by_query()
