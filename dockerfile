FROM python:3

RUN mkdir API
WORKDIR /API

COPY . .

RUN pip3 install -r requirements.txt

VOLUME [ "/SQL", "/Log" ]

ENV portSet_MIN 45535
ENV portSet_MAX 65535

CMD [ "python3", "main.py" ]