import os
from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return {"error": "No image file provided"}, 400

    file = request.files['image']

    try:
        input_image = Image.open(file.stream)
        img_byte_arr = io.BytesIO()
        input_image.save(img_byte_arr, format=input_image.format)
        input_image_bytes = img_byte_arr.getvalue()

        output_image_bytes = remove(input_image_bytes)
        output_image = Image.open(io.BytesIO(output_image_bytes))

        output_img_stream = io.BytesIO()
        output_image.save(output_img_stream, format="PNG")
        output_img_stream.seek(0)

        return send_file(output_img_stream, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)
