# use python version 3 docker image as base image
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1

# copy the requirements.txt file in to the pwd of docker image.
COPY requirements.txt ./

# now run the command to install dependencies from requirements file
RUN pip install -r requirements.txt

# copy the content of current directory in to the pwd of docker image.
COPY . .

# everytime container is started, run this command
ENTRYPOINT ["python", "main.py"]