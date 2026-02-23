###########
# BUILDER #
###########

# pull official base image
FROM python:3.14-alpine AS builder
LABEL maintainer="Daniel Schlich <calendaronline@k51.de>"

WORKDIR /app

ARG APP_UID=1000
ARG APP_GID=1000

RUN apk add --no-cache uv && \
    addgroup --system --gid "${APP_GID}" calendaronline && \
    adduser --system -u "${APP_UID}" -G calendaronline calendaronline && \
    chown calendaronline:calendaronline -R /app

USER calendaronline

COPY --chown=calendaronline:calendaronline pyproject.toml ./
COPY --chown=calendaronline:calendaronline Docker/ ./bin

ENV PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  UV_COMPILE_BYTECODE=1 \
  UV_PROJECT_ENVIRONMENT="/home/calendaronline/.local" \
  PATH="${PATH}:/home/calendaronline/.local/bin" \
  USER="calendaronline"

RUN uv lock && \
    uv sync --frozen --no-install-project

CMD ["sh"]

#########
# FINAL #
#########

FROM python:3.14-alpine AS app
LABEL maintainer="Daniel Schlich <calendaronline@k51.de>"
LABEL org.opencontainers.image.source=https://github.com/dpmpc/calendaronline
LABEL org.opencontainers.image.description="A simple tool to create beautiful photo calendars as PDF for self printing."
LABEL org.opencontainers.image.licenses=GPL-3.0

WORKDIR /app

ARG APP_UID=1000
ARG APP_GID=1000
ENV GUNICORN_PORT=8001

RUN apk add --no-cache poppler-utils uv && \
    addgroup --system --gid "${APP_GID}" calendaronline && \
    adduser --system -u "${APP_UID}" -G calendaronline calendaronline && \
    chown calendaronline:calendaronline -R /app

USER calendaronline

ENV  PYTHONUNBUFFERED="true" \
  PYTHONPATH="." \
  UV_PROJECT_ENVIRONMENT="/home/calendaronline/.local" \
  PATH="${PATH}:/home/calendaronline/.local/bin" \
  USER="calendaronline"

COPY --chown=calendaronline:calendaronline --from=builder /home/calendaronline/.local /home/calendaronline/.local
COPY --from=builder /app/bin/startup.prod.sh /usr/local/bin/
COPY --chown=calendaronline:calendaronline creator ./creator/
COPY --chown=calendaronline:calendaronline calendaronline ./calendaronline/
COPY --chown=calendaronline:calendaronline files ./files/

ENTRYPOINT ["/usr/local/bin/startup.prod.sh"]
CMD ["calendaronline.wsgi:application"]