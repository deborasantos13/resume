import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor

class SubjectDetails(BaseModel):
    title: str
    details: List[str] = Field(..., description="A list of details about the subject")

def prompt_user():
    return input("Enter a topic to learn about (or 'exit' to quit): ")

def fetch_info(topic):
    groq_client = Groq(
        api_key=os.environ.get(
            os.environ.get("GROQ_API_KEY"),
        ),
    )

    groq_client = instructor.from_groq(groq_client, mode=instructor.Mode.TOOLS)

    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": f"Tell me about {topic}",
            }
        ],
        response_model=SubjectDetails,
    )
    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    while True:
        topic_input = prompt_user()
        if topic_input.lower() == 'exit':
            break
        fetch_info(topic_input)