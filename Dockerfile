FROM python:rc-alpine
RUN apk add build-base py-pip libpng-dev jpeg-dev zlib-dev freetype-dev imagemagick
ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip3 install pillow

RUN apk del build-base py-pip

WORKDIR /usr/src/graffiti

COPY . ./

EXPOSE 80

CMD ["python3", "server.py"]
