
# StoreBot Bot

## Необходиме переменные окружения:
```
BOT_TOKEN=

DJANGO_SECRET_KEY=
DJANGO_DEBUG=<True or False>
DJANGO_ALLOWED_HOSTS=<HOST_SEPARATED_BY_COMMA>

PRIVACY_POLICY_FILE_TELEGRAM_ID=

MEDIA_URL=http://<INSERT_YOUR_HOST_HERE>/media/
```

### Хранить их нужно в файле `.env` в корне проекта (на одном уровне с модулем `main.py`)

## Сборка проекта осуществляется командой:
```sudo docker-compose up --build```
