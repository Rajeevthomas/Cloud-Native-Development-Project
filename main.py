import os
from flask import Flask, redirect, request, send_file, render_template
from datetime import datetime
from gemini import model, upload_to_gemini, PROMPT
import json
from storage import download_file, get_list_of_files, upload_file

os.makedirs('files', exist_ok=True)
bucket_name = "cnd_uploads"

app = Flask(__name__)

@app.route('/')
def index():
    # Decide which version to show (you can also add logic to split traffic, but here it's set to show blue by default)
    return render_template('blue.html')  # For now, it returns blue version

@app.route('/green')
def green_version():
    # You can switch to the green background version
    return render_template('green.html')

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    filename, ext = os.path.splitext(file.filename)  
    new_filename = f"{filename}_{timestamp}{ext}"  
    path = "files/" + new_filename
    file.save(path)
    upload_file(bucket_name, path)
    response = model.generate_content([upload_to_gemini(path, mime_type="image/jpeg"), "\n\n", PROMPT]).text.replace("```json", "").replace("```", "").replace("\n", "")
    response_data = json.loads(response)
    json_filename_path = f"files/{filename}_{timestamp}.json"   
    with open(json_filename_path, 'w') as json_file:
        json.dump(response, json_file)
    upload_file(bucket_name, json_filename_path)     
    return redirect("/")

@app.route('/files')
def list_files():
    files = os.listdir("./files")
    jpegs = []
    for file in files:
        if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg") or file.lower().endswith(".json"):
            jpegs.append(file)
    
    return jpegs

@app.route('/files/<filename>')
def get_file(filename):
    return send_file('./files/' + filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
