import os
from flask import Flask, redirect, request, send_from_directory, render_template
from datetime import datetime
from gemini import model, upload_to_gemini, PROMPT
import json
from storage import download_json,download_image, get_list_of_files, upload_file

os.makedirs('files', exist_ok=True)

app = Flask(__name__)

@app.route('/')
def index():
    files = list_files()
    return render_template('index.html', files=files)

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    filename, ext = os.path.splitext(file.filename)  
    new_filename = f"{filename}_{timestamp}{ext}"  
    path = "files/" + new_filename
    file.save(path)
    upload_file(path)
    response = model.generate_content([upload_to_gemini(path, mime_type="image/jpeg"), "\n\n", PROMPT]).text.replace("```json", "").replace("```", "").replace("\n", "")
    response_data = json.loads(response)
    json_filename_path = f"files/{filename}_{timestamp}.json"   
    with open(json_filename_path, 'w') as json_file:
        json.dump(response_data, json_file)
    upload_file(json_filename_path)
    return redirect("/")

@app.route('/files')
def list_files():
    files = get_list_of_files()
    jpegs = []
    for file in files:
        if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
            jpegs.append(file)
    return jpegs

@app.route('/files/<filename>')
def get_file(filename):
    file_path = 'files/' + filename
    title,description = download_json(file_path)
    return render_template('file_details.html', title=title, description=description, filename=filename)

@app.route('/images/<filename>')
def get_image(filename):
    file_path = 'files/' + filename
    download_image(file_path)
    return send_from_directory('files', filename)

if __name__ == '__main__':
    app.run(debug=True)
