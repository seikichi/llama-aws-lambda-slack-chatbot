FROM public.ecr.aws/lambda/python:3.10

# Copy ggml model to Image
COPY model.bin ${LAMBDA_TASK_ROOT}/model.bin

# https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    yum groupinstall -y "Development Tools"

COPY pyproject.toml poetry.lock ./
RUN /root/.local/bin/poetry export --without-hashes --format requirements.txt --output requirements.txt && \
    pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN mkdir llama.cpp && \
    cd llama.cpp && \
    git init && \
    git remote add origin https://github.com/ggerganov/llama.cpp && \
    git fetch --depth 1 origin 348d6926ee31d4476f9b90e1a627b0925a70f847 && \
    git checkout FETCH_HEAD && \
    make

COPY app.py chat.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
