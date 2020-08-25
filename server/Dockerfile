FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY /requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY /app /app
ADD https://storage.googleapis.com/poem_gen_gpt2_model/run1.zip /app/checkpoint/run1.zip
RUN unzip /app/checkpoint/run1.zip -d /app/checkpoint
