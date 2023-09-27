import argparse
import json
from flask import Flask, request, jsonify
import logging
from ultralytics import YOLO
from io import BytesIO
from PIL import Image, ImageOps
import os
import requests

app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app.logger.info('Loading model...')
model = model = YOLO('yolov8s.pt')
app.logger.info('Loading model done!')

DETECTION_URL = "/v1/object-detection"

def download_image(image_path: str):
    if image_path.startswith("https://") or image_path.startswith("http://"):
        res = requests.get(image_path, verify=False)
        if res.status_code == 200:
            im = Image.open(BytesIO(res.content))
        else:
            raise requests.HTTPError(f"Load image url {image_path} fail")
    else:
        im = Image.open(image_path)

    if im.format.lower() in ("jpg", "jpeg"):
        im = ImageOps.exif_transpose(im)

    return im

@app.route("/", methods=["GET"])
def home():
    app.logger.info('Info level log')
    app.logger.warning('Warning level log')
    return "OK"

@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if not request.data:
        return

    rdata = json.loads(request.data)

    image_uri = rdata['image_uri']
    img = download_image(image_uri)
    results = model.predict(img, imgsz=640)

    res = []
    for r in results:
        boxes = r.boxes
        res.append(boxes.data.tolist())

    return jsonify(res), 200

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask api exposing yolov8 model")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    parser.add_argument('--model', default='yolov8s', help='model to run, i.e. --model yolov8s')
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port)
