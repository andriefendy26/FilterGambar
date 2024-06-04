from flask import Flask, render_template, request, send_file, redirect,url_for
from PIL import Image, ImageFilter, ImageOps
from datetime import datetime
import os
import platform
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    image_file = request.files['image']
    image = Image.open(image_file)
    image_path = save_uploaded_image(image)
    return render_template('index.html', uploaded_image_path=image_path)

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    uploaded_image_path = request.form['image_path']    
    image = Image.open(uploaded_image_path)
    selected_filter = request.form['filter']
    processed_image_path = None

    filtered_image = apply_selected_filter(image, selected_filter)
    processed_image_path = save_processed_image(filtered_image)
    return render_template('index.html', image_path=uploaded_image_path, processed_image_path=processed_image_path)

@app.route('/download_image', methods=['GET'])
def download_image():
    filename = request.args.get('filename')
    if filename:
        return send_file(filename, as_attachment=True)
    return "File not found."

def save_uploaded_image(image):
    unique_name = datetime.now().strftime("%Y%m%d%H%M%S")
    uploaded_image_path = f"static/uploads/uploaded_image_{unique_name}.jpg"
    image.save(uploaded_image_path)
    return uploaded_image_path

def apply_selected_filter(image, selected_filter):
    filtered_image = None

    if selected_filter == 'BLUR':
        filtered_image = image.filter(ImageFilter.BLUR)
    elif selected_filter == 'CONTOUR':
        filtered_image = image.filter(ImageFilter.CONTOUR)
    elif selected_filter == 'DETAIL':
        filtered_image = image.filter(ImageFilter.DETAIL)
    elif selected_filter == 'EDGE_ENHANCE':
        filtered_image = image.filter(ImageFilter.EDGE_ENHANCE)
    elif selected_filter == 'EDGE_ENHANCE_MORE':
        filtered_image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif selected_filter == 'EMBOSS':
        filtered_image = image.filter(ImageFilter.EMBOSS)
    elif selected_filter == 'FIND_EDGES':
        filtered_image = image.filter(ImageFilter.FIND_EDGES)
    elif selected_filter == 'SHARPEN':
        filtered_image = image.filter(ImageFilter.SHARPEN)
    elif selected_filter == 'SMOOTH':
        filtered_image = image.filter(ImageFilter.SMOOTH)
    elif selected_filter == 'SMOOTH_MORE':
        filtered_image = image.filter(ImageFilter.SMOOTH_MORE)
    elif selected_filter == 'SOLARIZE':
        filtered_image = ImageOps.solarize(image)
    elif selected_filter == 'POSTERIZE':
        filtered_image = ImageOps.posterize(image, 2)
    elif selected_filter == 'AUTOCONTRAST':
        filtered_image = ImageOps.autocontrast(image)
    elif selected_filter == 'GAUSSIAN_BLUR':
        filtered_image = image.filter(ImageFilter.GaussianBlur(4))
    elif selected_filter == 'INVERT_COLOR':
        filtered_image = ImageOps.invert(image)
    elif selected_filter == 'GRAYSCALE':
        filtered_image = ImageOps.grayscale(image)

    return filtered_image

def save_processed_image(image):
    unique_name = datetime.now().strftime("%Y%m%d%H%M%S")
    processed_image_path = f"static/downloads/processed_image_{unique_name}.jpg"
    image.save(processed_image_path)
    return processed_image_path

def open_folder(path):
    system = platform.system()
    if system == 'Darwin':  # macOS
        subprocess.Popen(['open', '--', '-R', path])
    elif system == 'Windows':  # Windows
        subprocess.Popen(['explorer', path])
    elif system == 'Linux':  # Linux
        subprocess.Popen(['xdg-open', path])

if __name__ == '__main__':
    app.run(debug=True)