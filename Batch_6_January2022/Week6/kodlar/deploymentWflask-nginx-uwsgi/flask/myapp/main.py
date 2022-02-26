from .ObjectDetector import detectImages, detectVideos
import io
from PIL import Image
import os
from werkzeug.utils import secure_filename #Pass it a filename and 
# it will return a secure version of it.
# This filename can then safely be stored on a regular file system

from flask import render_template, request, Response, send_file
from myapp import myapp

#app = Flask(__name__)
UPLOAD_FOLDER = 'myapp/static:css/uploads/'

@myapp.route("/")
def index():
    return render_template('index.html')

@myapp.route("/", methods=['POST'])
def upload():
    if request.form['dtype']=='image':
        imName=Image.open(request.files['file'].stream)
        img = detectImages(imName)
        return send_file(io.BytesIO(img),attachment_filename='image.jpg',mimetype='image/jpg')

    elif request.form['dtype']=='video':
        myapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file=request.files['file']
        filename = secure_filename(file.filename)
        new_filename = os.path.join(myapp.config['UPLOAD_FOLDER'], filename)
        file.save(new_filename)
        return Response(detectVideos(str(new_filename)),
                mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    myapp.run(debug=True)
