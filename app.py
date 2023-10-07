from flask import Flask, request, render_template, jsonify
import subprocess
from flask_cors import CORS
import os
from PIL import Image

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
app.config["IMAGE_UPLOADS"] = os.getcwd()



@app.route("/")
def hello_world():
    args = ("./script")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    print(output)
    return "Output printed out"

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():

    if request.method == "POST":
        if request.files:

            im = request.files["image"]
            
            
            # print(image + "Uploaded to Faces")
            # flash('Image successfully Uploaded to Faces.')
            im.save(os.path.join(app.config["IMAGE_UPLOADS"], im.filename))
            image = Image.open(os.path.join(app.config["IMAGE_UPLOADS"], im.filename))

            # Instantiates a client

            # The name of the image file to annotate
            file_name = os.path.abspath(im.filename)
            print(file_name)
            # Loads the image into memory
            with open(file_name, 'rb') as image_file:
                content = image_file.read()

            path = os.path.join(app.config["IMAGE_UPLOADS"], im.filename) 
            
            args = ("python3", "graphanalyzer.py")
            print(args)
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()
            print(output)
            
            return "Image uploaded and output printed out"