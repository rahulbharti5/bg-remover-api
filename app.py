from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def welcome():
    return "Welcome to the Background Remover API!"

@app.route('/process-image', methods=['POST'])
def process_image():
    # Check if a file is provided
    if 'image' not in request.files:
        return {"error": "No image file provided"}, 400

    # Read the uploaded image file
    file = request.files['image']

    try:
        # Open the image
        input_image = Image.open(file.stream)

        # Convert to bytes for processing
        img_byte_arr = io.BytesIO()
        input_image.save(img_byte_arr, format=input_image.format)
        input_image_bytes = img_byte_arr.getvalue()

        # Remove the background
        output_image_bytes = remove(input_image_bytes)

        # Convert back to an image
        output_image = Image.open(io.BytesIO(output_image_bytes))

        # Save the output image to bytes
        output_img_stream = io.BytesIO()
        output_image.save(output_img_stream, format="PNG")
        output_img_stream.seek(0)

        # Send the processed image back to the client
        return send_file(output_img_stream, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    # Run the app on localhost and port 5000
    app.run(host='0.0.0.0', port=5000)
