from audioop import cross
from flask import Flask, request, send_file
from PIL import Image, ImageOps, ImageFilter
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = './img'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
RED_GREEN = '0'

class Filter:

    def __init__(self, min_in, max_in, min_out, max_out):
        self.minI = min_in
        self.maxI = max_in
        self.minO = min_out
        self.maxO = max_out

    def deltaOut(self):
        return self.maxO - self.minO

    def deltaIn(self):
        return self.maxI - self.minI

    def apply(self, img):
        return (img-self.minI)*(((self.deltaOut())/(self.deltaIn()))+self.minO)

# Parameters for contrast stretching: https://pythontic.com/image-processing/pillow/contrast%20stretching
red_params =    (86,    230,    0,  255)
green_params =  (90,    225,    0,  255)
blue_params =   (100,   210,    0,  255)

red_filter:     Filter = Filter(*red_params)
green_filter:   Filter = Filter(*green_params)
blue_filter:    Filter = Filter(*blue_params)


def enhanceRedGreen(img):
    bands = img.split()

    redBand = bands[0].point(red_filter.apply)
    greenBand = bands[1].point(green_filter.apply)

    return Image.merge("RGB", (redBand, greenBand, bands[2]))


def enhanceBlueYellow(img):
    bands = img.split()

    greenBand = bands[1].point(green_filter.apply)
    blueBand = bands[2].point(blue_filter.apply)

    return Image.merge("RGB", (bands[0], greenBand, blueBand))


@app.route('/api/process', methods=['GET', 'POST'])
# @cross_origin()
def process():
    img = request.files['image']
    mime_type = img.content_type
    ftype = 'png' if 'png' in str(img.content_type) else 'jpg'
    img.save(f'./img/img.{ftype}')
    
    with Image.open(f"./img/img.{ftype}") as img:
        img = img.filter(ImageFilter.EDGE_ENHANCE)
        if request.form['type'] == '0':
            img = enhanceRedGreen(img)
        elif request.form['type'] == '1':
            img = enhanceBlueYellow(img)
        else:
            img = ImageOps.grayscale(img)
            # print("Wrong type")
        img.save(f"./img/imgout.{ftype}")
    
    return send_file(f"./img/imgout.{ftype}", mimetype=mime_type)

app.run()