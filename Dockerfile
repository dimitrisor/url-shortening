FROM python:3.9.2-alpine
RUN mkdir /shorty
WORKDIR /shorty
ADD . /shorty/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","run.py"]