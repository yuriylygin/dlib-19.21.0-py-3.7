FROM  rackspacedot/python37:latest

RUN python -m pip install -U pip

RUN pip install cmake

RUN pip install dlib --verbose