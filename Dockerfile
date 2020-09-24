FROM  rackspacedot/python37:28

RUN python -m pip install -U pip

RUN pip install cmake

RUN pip install dlib --verbose
