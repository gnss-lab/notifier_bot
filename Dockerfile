FROM python:3.10-alpine
WORKDIR /app
COPY . .

WORKDIR fast_api
RUN python -m venv venv
RUN source venv/bin/activate && pip install poetry && poetry install
WORKDIR ../

WORKDIR telegram_bot
RUN python -m venv venv
RUN source venv/bin/activate && pip install poetry && poetry install
WORKDIR ../

#CMD pwd; ls fast_api/venv/bin;
CMD ./telegram_bot/venv/bin/python main_bot.py & ./fast_api/venv/bin/python main_api.py