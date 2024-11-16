import google.generativeai as gai
import os
from dotenv import load_dotenv

load_dotenv()
gai.configure(api_key= os.getenv("GOOGLE_API_KEY"))
model = gai.GenerativeModel("gemini-pro")

def give_responces(artical):
    
    promt = "Analyze the input text and generate 5 essential questions **don't show these qusntion in the summary use that intenally for understand how to generate summary** that, when answered, capture the main points and core meaning of the text. 2.) When formulating your questions: a. Address the central theme or argument b. Identify key supporting ideas c. Highlight important facts or evidence d. Reveal the author's purpose or perspective e. Explore any significant implications or conclusions. 3.) Answer all of your generated questions in one paragraph in detail 4.) make it in between 80-150 words 5.) don't show the genrated quesntions"
    
    response = model.generate_content(f"{promt} : '{artical}'")
    
    if response.text:
        return response.text
    else:
        return ""
