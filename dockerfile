FROM python:3.11

RUN mkdir API
WORKDIR /API

COPY . .

RUN pip3 install -r requirements.txt

VOLUME [ "/API/SQL", "/API/Log" ]

ENV portSet_MIN 45535
ENV portSet_MAX 65535
ENV GPUSetting 0

CMD [ "python3", "main.py" ]