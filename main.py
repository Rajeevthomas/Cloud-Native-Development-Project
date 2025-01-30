import os
from flask import Flask, redirect, request, send_file
from datetime import datetime

from storage import add_db_entry, download_file, get_list_of_files, upload_file

os.makedirs('files', exist_ok = True)
bucket_name = "cnd_uploads"

app = Flask(__name__)

@app.route('/')
def index():
    index_html="""
<form method="post" enctype="multipart/form-data" action="/upload" method="post">
  <div>
    <label for="file">Choose file to upload</label>
    <input type="file" id="file" name="form_file" accept="image/jpeg"/>
  </div>
  <div>
    <button>Submit</button>
  </div>
</form>"""    

    bucket_files = set(get_list_of_files(bucket_name))
    local_files =  set(list_files())
    files_not_in_local = list(bucket_files - local_files)

    if files_not_in_local:
        for nfile in files_not_in_local: 
            download_file(bucket_name, nfile)

    for file in list_files():
        index_html += "<li><a href=\"/files/" + file + "\">" + file + "</a></li>"

    return index_html

@app.route('/upload', methods=["POST"])
def upload():
    file = request.files['form_file']  
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    filename, ext = os.path.splitext(file.filename)  
    new_filename = f"{filename}_{timestamp}{ext}"  
    path = "files/" +  new_filename
    file.save(path)
    public_url = upload_file(bucket_name, path)
    obj = {"unique_file_name": new_filename,"orginal_file_name": file.filename, "local_path" : path, "public_url" : public_url,"timestamp": timestamp}
    add_db_entry(obj)
    return redirect("/")

@app.route('/files')
def list_files():
    files = os.listdir("./files")
    jpegs = []
    for file in files:
        if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
            jpegs.append(file)
    
    return jpegs

@app.route('/files/<filename>')
def get_file(filename):
  return send_file('./files/'+filename)

if __name__ == '__main__':
    app.run(debug=True)