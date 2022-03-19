FROM python:slim-buster

RUN useradd -ms /bin/bash starbot

USER starbot
RUN pip3 install discord-notify asyncio websocket configparser

CMD [ "sleep" , "infinity" ]
