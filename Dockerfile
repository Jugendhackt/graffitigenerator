FROM python:3.8.2-buster
RUN pip3 install pillow
RUN pip3 install image

WORKDIR /usr/src/graffiti

COPY * ./
COPY fonts fonts/
COPY textures textures/
COPY assets assets/


EXPOSE 80

CMD ["python3", "server.py"]
