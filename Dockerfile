FROM python:3.9.6-alpine
WORKDIR /ecommerce_api_project

#settting environment variables
ENV PYTHONDONTWRITEBYTECODE 1 #Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 #Prevents Python from buffering stdout and stderr

#install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

#install dependancies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#copy entrypoint.sh

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /ecommerce_api_project/entrypoint.sh
RUN chmod +x /ecommerce_api_project/entrypoint.sh

#copy project
COPY . .


#run entrypoint.sh
ENTRYPOINT ["/ecommerce_api_project/entrypoint.sh"]