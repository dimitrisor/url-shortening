FROM python:3.9.2-alpine
WORKDIR /shorty
ADD . /shorty
RUN pip3 install -r requirements.txt
CMD ["python3","run.py"]