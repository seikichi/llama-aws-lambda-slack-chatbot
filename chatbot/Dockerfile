FROM public.ecr.aws/lambda/python:3.10

# https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    yum groupinstall -y "Development Tools"

RUN mkdir llama.cpp && \
    cd llama.cpp && \
    git init && \
    git remote add origin https://github.com/ggerganov/llama.cpp && \
    git fetch --depth 1 origin e899bf54b291e8c84173a0e534a2c262f3f63229 && \
    git checkout FETCH_HEAD && \
    make

COPY pyproject.toml poetry.lock ./
RUN /root/.local/bin/poetry export --without-hashes --format requirements.txt --output requirements.txt && \
    pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY model.bin ${LAMBDA_TASK_ROOT}/model.bin
COPY app.py chat.py ${LAMBDA_TASK_ROOT}
CMD [ "app.handler" ]
