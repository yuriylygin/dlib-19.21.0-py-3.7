FROM  rackspacedot/python37:latest

RUN python -m pip install -U pip

RUN pip install cmake

RUN pip install dlib --verbose

COPY requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

COPY app /src/app

COPY model /src/model

WORKDIR /src/workspace

CMD [ "python", "/src/app/boarding_box.py" ]