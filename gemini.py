import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API'])

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
)

PROMPT = """
Describe the image in detail and generate a title and description for it. 
Return the response as a JSON object in the following format:

{
   "title" : "PLACE THE GENERATED TITLE HERE",
   "description" : "PLACE THE GENERATED DESCRIPTION HERE"
}
"""

def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  return file
