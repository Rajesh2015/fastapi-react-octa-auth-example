FROM node:latest

RUN mkdir /frontend
WORKDIR /frontend
ADD ./src /frontend/src
ADD ./public /frontend/public

ENV PATH /frontend/node_modules/.bin:$PATH

COPY package.json /frontend/package.json
RUN npm install
