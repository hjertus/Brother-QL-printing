FROM python:3

COPY.. .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "src/printing_shit.py"]