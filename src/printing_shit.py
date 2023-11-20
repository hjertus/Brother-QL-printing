from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
import cv2
from pdf2image import convert_from_bytes
import tempfile
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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

            images = []  # Initialize an empty list to store stretched images

            # Convert PDF pages to images
            pdf_images = convert_from_bytes(open(pdf_path, 'rb').read())

            for i, pdf_image in enumerate(pdf_images):
                # Save each page as an image
                img_path = os.path.join(temp_dir, f'receipt_{i}.jpg')
                pdf_image.save(img_path, 'JPEG')

                # Load the saved image
                image = cv2.imread(img_path)

                # Get the dimensions of the image
                height, width, _ = image.shape

                # Calculate the number of rows (pixels) to remove from the top 10%
                rows_to_remove = int(height * 0.08)

                # Crop the image to remove the top 10%
                cropped_image = image[rows_to_remove:, :]

                # Define the desired fixed width and height
                fixed_width = 1200
                fixed_height = 1822

                # Resize the cropped image to the fixed width and height
                stretched_image = cv2.resize(cropped_image, (fixed_width, fixed_height))

                # Append the stretched image to the list
                images.append(Image.fromarray(stretched_image))

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

            # Redirect back to the first page with an empty file input field
            return redirect(url_for('upload_pdf'))

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
