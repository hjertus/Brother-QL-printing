FROM python:3

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    poppler-utils \
    libusb-1.0-0 \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Poppler to the PATH
ENV PATH="${PATH}:/usr/bin"

# Install Python dependencies
RUN pip install -r requirements.txt
RUN pip install pyusb

# Expose port 5000
EXPOSE 5000

# Set the entry point
CMD ["python", "src/printing_shit.py"]
