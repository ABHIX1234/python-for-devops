#take base level for project

FROM python:3.14

#add work direc= app

WORKDIR /app

copy . .

#mix/ process the items

RUN pip install -r requirements.txt

#which port
EXPOSE 8000
#start code

CMD ["python","main.py"]

