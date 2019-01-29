FROM mongo:latest
COPY mongo/mongod.conf /etc/mongod.conf
RUN ["mongod", "-f",  "/etc/mongod.conf"]
EXPOSE 27017/tcp
