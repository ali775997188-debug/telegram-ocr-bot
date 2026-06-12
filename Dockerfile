FROM python:3.10-slim
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-ara libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bpp.py .
EXPOSE 10000
CMD ["python", "bpp.py"]
