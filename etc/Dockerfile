# from ubuntu 20.04
FROM ubuntu:focal

# dependencies
RUN apt-get -y update
RUN apt-get -y install curl git python3 python3-pip python3-dev python3-venv git

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# add $HOME/.local/bin to path
ENV PATH "$PATH:/root/.local/bin"
RUN poetry --version

# install g29
RUN git clone https://github.com/seanavery/g29-py.git && \
    cd g29-py && \
    poetry build && \
    poetry install
