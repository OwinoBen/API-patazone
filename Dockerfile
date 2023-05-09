FROM python:3
WORKDIR /ecommerce_api_project
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .