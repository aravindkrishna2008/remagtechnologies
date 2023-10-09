import json
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
    # print(output)
    return "Output printed out"

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    print("hello world")

    if request.method == "POST":
        if request.files:

            im = request.files["image"]
            im.filename = "graph-1.png"
            
            
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
            popen = subprocess.Popen(args)
            popen.wait()
            
            args = ("./script")
            popen = subprocess.Popen(args, stdout=subprocess.PIPE)
            popen.wait()
            output = popen.stdout.read()

            input_string = output.decode('utf-8')

            # Split the input string by newline character '\n'
            lines = input_string.split('\n')

            # Initialize an empty list to store the objects
            objects = []

            # Iterate over each line and split it by space
            for line in lines:
                parts = line.split()
                
                # Check if there are enough parts to create an object
                if len(parts) >= 6:
                    obj = {
                        'day': int(parts[0]),
                        'reconrate': float(parts[1]),
                        'imfpeak': int(parts[2]),
                        'imfflip': int(parts[3]),
                        'potsolarevent': int(parts[4]),
                        'severity': int(parts[5])
                    }
                    objects.append(obj)

            # Print the resulting list of objects
            for obj in objects:
                print(obj)
                
            return objects