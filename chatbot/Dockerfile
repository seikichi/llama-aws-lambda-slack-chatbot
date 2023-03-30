FROM public.ecr.aws/lambda/python:3.10

# Copy ggml model to Image
COPY model.bin ${LAMBDA_TASK_ROOT}

# https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    yum groupinstall -y "Development Tools"

COPY pyproject.toml poetry.lock ./
RUN /root/.local/bin/poetry export --without-hashes --format requirements.txt --output requirements.txt && \
    pip3 install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

RUN mkdir llama.cpp && \
    cd llama.cpp && \
    git init && \
    git remote add origin https://github.com/ggerganov/llama.cpp && \
    git fetch --depth 1 origin 9cbc404ba6699a9ba4925ea25a60552b13491c7a && \
    git checkout FETCH_HEAD && \
    make

COPY prompt.txt app.py ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]
