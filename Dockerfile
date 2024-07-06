FROM    python:3.12-slim
WORKDIR /app
COPY    requirements.txt .
RUN     pip install --no-cache-dir -r requirements.txt
COPY    index.py .
EXPOSE  5000
ENV     GITHUB_REPOSITORY=$GITHUB_REPOSITORY \
        GITHUB_REF_NAME=$GITHUB_REF_NAME \
        GITHUB_SHA=$GITHUB_SHA \
        GITHUB_RUN_NUMBER=$GITHUB_RUN_NUMBER
CMD     [ "/usr/local/bin/gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "index:app" ]
