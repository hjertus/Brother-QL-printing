from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
from pdf2image import convert_from_bytes
import tempfile
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def crop_and_resize_image(image, fixed_width, fixed_height):
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the number of rows (pixels) to remove from the top 10%
    rows_to_remove = int(height * 0.08)

    # Crop the image to remove the top 10%
    cropped_image = image.crop((0, rows_to_remove, width, height))

    # Resize the cropped image to the fixed width and height
    stretched_image = cropped_image.resize((fixed_width, fixed_height))

    return stretched_image

def printing(images):
    # Setting Printer Specifications
    backend = 'pyusb'
    model = 'QL-1100'
    printer = 'usb://0x04F9:0x20A7/000/001'

    # Initialize BrotherQLRaster with the specified model
    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    # Converting print instructions for the Brother printer
    instructions = convert(
        qlr=qlr,
        images=images,  # Pass the list of stretched images
        label='103x164',  # Use the appropriate label size
        rotate='0',  # 'Auto', '0', '90', '270'
        threshold=70.0,  # Black and white threshold in percent.
        dither=False,
        compress=False,
        dpi_600=False,
        hq=True,  # False for low quality.
        cut=True
    )

    # Send the instructions to the printer
    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return redirect(request.url)

        pdf_file = request.files['pdf']

        if pdf_file.filename == '':
            return redirect(request.url)

        if pdf_file:
            # Create a temporary directory to store the PDF and images
            temp_dir = tempfile.mkdtemp()

            pdf_path = os.path.join(temp_dir, 'input.pdf')
            pdf_file.save(pdf_path)

            # Convert PDF pages to images
            pdf_images = convert_from_bytes(open(pdf_path, 'rb').read())

            for i, pdf_image in enumerate(pdf_images):
                images = []  # Initialize an empty list to store stretched images
                # Save each page as an image
                img_path = os.path.join(temp_dir, f'receipt_{i}.jpg')
                pdf_image.save(img_path, 'JPEG')

                # Open the saved image using PIL
                image = Image.open(img_path)

                # Define the desired fixed width and height
                fixed_width = 1200
                fixed_height = 1822

                # Crop and resize the image
                stretched_image = crop_and_resize_image(image, fixed_width, fixed_height)

                # Append the stretched image to the list
                images.append(stretched_image)
                printing(images)

            # Redirect back to the first page with an empty file input field
            return redirect(url_for('upload_pdf'))

    return render_template('upload.html')

@app.route('/upload/<path:url_for_pdf>', methods=['GET'])
def upload_from_url(url_for_pdf):
    try:
        # Download PDF from the provided URL
        response = requests.get(url_for_pdf, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Create a temporary directory to store the PDF and images
        temp_dir = tempfile.mkdtemp()

        pdf_path = os.path.join(temp_dir, 'input.pdf')
        with open(pdf_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)

        # Perform the processing logic
        pdf_images = convert_from_bytes(open(pdf_path, 'rb').read())

        for i, pdf_image in enumerate(pdf_images):
            images = []  # Initialize an empty list to store stretched images
            # Save each page as an image
            img_path = os.path.join(temp_dir, f'receipt_{i}.jpg')
            pdf_image.save(img_path, 'JPEG')

            # Open the saved image using PIL
            image = Image.open(img_path)

            # Define the desired fixed width and height
            fixed_width = 1200
            fixed_height = 1822

            # Crop and resize the image
            stretched_image = crop_and_resize_image(image, fixed_width, fixed_height)

            # Append the stretched image to the list
            images.append(stretched_image)
            printing(images)

        # Return a response or redirect as needed
        return "Processing complete!"

    except requests.RequestException as e:
        return f"Failed to download PDF from {url_for_pdf}. Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
