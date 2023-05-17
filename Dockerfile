FROM python:3.9.6-alpine
WORKDIR /ecommerce_api_project

#settting environment variables
ENV PYTHONDONTWRITEBYTECODE 1 #Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 #Prevents Python from buffering stdout and stderr

#install dependancies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#copy project
COPY . .
