FROM registry.redhat.io/ubi9/ubi
LABEL maintainer="ruthvik and the team  ruthvikshinde553@gmail.com"
LABEL decription="This image contains a python program which is a Machine Learning Model that detects the stuttering the given audio file (model is alpha)"
WORKDIR /code
RUN mkdir /code/templates
COPY ./app.py /code
COPY ./templates/index.html /code/templates
COPY ./requirements.txt /code
COPY ./stutter_detection_model.json /code
COPY ./stutter_detection_modela.h5 /code
RUN yum install -y python \
&& yum install -y pip \
&& pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]