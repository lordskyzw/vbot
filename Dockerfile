FROM python:3.9.6
WORKDIR /vbot
COPY requirements.txt /vbot/
RUN pip install -r requirements.txt
COPY . /vbot/
CMD ["python", "app.py"]