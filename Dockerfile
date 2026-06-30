FROM ubuntu:latest
LABEL authors="joaov"

ENTRYPOINT ["top", "-b"]