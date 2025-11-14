# Base off the official python image
# Define a common stage for dev and prod images called base
FROM python:3.12.4-slim AS python_base
LABEL version="0.1" creator="chochyjj@gmail.com" description="Python 3.12.4"
# Set environment variables
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates systemd openssh-server default-libmysqlclient-dev build-essential libpq-dev apt-utils gcc g++ git git-flow wget curl gfortran cmake pkg-config locales \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && update-ca-certificates \
    && localedef -i ko_KR -c -f UTF-8 -A /usr/share/locale/locale.alias ko_KR.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN systemctl enable ssh
RUN groupadd docker
# Project
RUN mkdir /project/
WORKDIR /project/
COPY ./Build-Default-Settings/_Python-Settings-Files/.vscode .vscode
COPY ./Build-Default-Settings/_Python-Settings-Files/README.Flask.md ./README.md
RUN python -m pip install --upgrade --no-cache-dir pip
RUN pip install --no-cache-dir setuptools pre-commit ruff
# Define an image for local development. Inherits common packages from the base stage.
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
FROM python_base AS dev_flask
LABEL version="0.1" creator="chochyjj@gmail.com" description="Flask"
WORKDIR /project/
RUN mkdir /project/test
RUN mkdir /project/docs
COPY ./Default-Flask/.env.dev.example ./.env
COPY ./Default-Flask/configs ./configs
COPY ./Default-Flask/models ./models
COPY ./Default-Flask/routes ./routes
COPY ./Default-Flask/static ./static
COPY ./Default-Flask/templates ./templates
COPY ./Default-Flask/tests ./tests
COPY ./Default-Flask/views ./views
COPY ./Default-Flask/pyproject.toml .
COPY ./Default-Flask/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# /////////////////////////////////////////////////////////////////
# github SSH key 사용
# /////////////////////////////////////////////////////////////////
COPY ./Build-Default-Settings/_Common-Settings-Files/.ssh /root/.ssh
COPY ./Build-Default-Settings/_Python-Settings-Files/.pre-commit-config.yaml .
COPY ./Build-Default-Settings/_Python-Settings-Files/.gitignore.flask .gitignore
RUN git config --global core.editor "code --wait"
RUN git config --global user.email "chochyjj@gmail.com"
RUN git config --global user.name "Hyunyoun Jo"
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa.pub
# /////////////////////////////////////////////////////////////////
# zsh 설치 : 삭제 가능
# /////////////////////////////////////////////////////////////////
COPY ./Build-Default-Settings/_Common-Settings-Files/zsh-in-docker.sh .
RUN chmod 755 /project/zsh-in-docker.sh
RUN /project/zsh-in-docker.sh \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-history-substring-search \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -p 'history-substring-search' \
    -a 'bindkey "\$terminfo[kcuu1]" history-substring-search-up' \
    -a 'bindkey "\$terminfo[kcud1]" history-substring-search-down'
# /////////////////////////////////////////////////////////////////
ENTRYPOINT [ "zsh" ]
# /////////////////////////////////////////////////////////////////
FROM python_base AS prod_flask
LABEL version="0.1" creator="chochyjj@gmail.com" description="Flask"
COPY ./Default-Flask/requirements.txt .
COPY ./Default-Flask/pyproject.toml .
RUN pip install --no-cache-dir -r requirements.txt
# /////////////////////////////////////////////////////////////////