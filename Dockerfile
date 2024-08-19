FROM python:3.10-alpine AS base

FROM base

ENV APP_ROOT /app

WORKDIR $APP_ROOT

COPY . $APP_ROOT

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "run.sh"]