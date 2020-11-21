FROM python:3.8.1

ENV HOME=/home/doggo
COPY requirements.txt $HOME/requirements.txt
RUN pip3 install -r $HOME/requirements.txt
RUN useradd --create-home --home-dir $HOME doggo
COPY entrypoint.sh $HOME/entrypoint.sh
COPY dev.env $HOME/dev.env
COPY prod.env $HOME/prod.env
COPY doggo $HOME/doggo
RUN chown --recursive doggo $HOME

WORKDIR $HOME

USER doggo
