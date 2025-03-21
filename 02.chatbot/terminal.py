import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name = "gemini-2.0-flash")

while True:

    user_input = input("\nEnter your question or (quit) to exit: \n")
    if user_input.lower() =='quit':
        print("\nThanks for chatting! Bye!")
        break


    response = model.generate_content(user_input)

    print(F"\n{response.text}\n")