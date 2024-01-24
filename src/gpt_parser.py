from openai import OpenAI
import re

import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# api key getter
with open(resource_path("gpt-api-key.txt"), "r") as file:
    api_key = file.read()

client = OpenAI(
    api_key=api_key
)

def get_topic():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                  "content": """Can you provide ONLY ONE TOPIC example of TOEFL speaking independence task 
                  with EXCEPT DESCRIBING/EXPERIENCE style??
                  
                  TOPIC SUGGESTION means specific topic like 'Would you prefer to take a challenging course or an easy course at university?".
                  DESCRIPTION means some words like "Include details and explanation." or "State whether you agree or disagree with the following statement. Then explain your reasons using specific details in your explanation."
                  
                  Please answer ONLY with this format. DO NOT USE WORDS LIKE "Topic: ", "Description: ".:
                  
                  Suggestion: <Paragraph that combined TOPIC SUGGESTION and DESCRIPTION>"""}
        ]
    )

    chat_response = completion.choices[0].message.content
    p = re.compile('Suggestion:[ \t\n\r\f\v]')
    result = p.sub('', chat_response)
    print(result)

    return result

def get_sample_response(topic: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",
                   "content": f"""Give me a well-done possible SHORT 45-SECOND-response script composed with 2 reasons of this topic:
                   
                   [{topic}]

                    Please answer ONLY with this format. Please divide paragraphs so that we can see it visually easily:

                    Possible Response: <Your possible response for given topic>"""}
                  ]
    )

    chat_response = completion.choices[0].message.content
    return chat_response

if __name__=="__main__":
    topic = get_topic()
    get_sample_response(topic)