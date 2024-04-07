FROM python:3.11.8-bullseye

# ユーザの追加
ARG USER_NAME="estatuser"
RUN groupadd  "${USER_NAME}" && \
    useradd -s /bin/bash -m "${USER_NAME}" -g "${USER_NAME}"
USER ${USER_NAME}

WORKDIR /workspaces/

# poetryのインストール先の指定
ENV POETRY_HOME=/home/"${USER_NAME}"/bin/poetry

# poetryインストール
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    # poetryコマンドの追加
    echo "alias poetry=/home/${USER_NAME}/bin/poetry/bin/poetry" >> "/home/${USER_NAME}/.bash_aliases" 
