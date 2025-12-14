# ML Service - Blue-Green Deployment

ML-сервис с REST API для инференса модели и Blue-Green стратегией развертывания.

## Структура проекта

```
├── app/
│   └── main.py                  # FastAPI приложение
├── models/
│   └── model.pkl                # Обученная модель
├── nginx/
│   ├── nginx.conf               # Конфигурация Nginx
│   ├── upstream.conf            # Текущий активный upstream
│   ├── upstream-blue.conf       # Blue upstream
│   └── upstream-green.conf      # Green upstream
├── .github/
│   └── workflows/
│       └── deploy.yml           # CI/CD pipeline
├── Dockerfile                   # Docker образ сервиса
├── docker-compose.blue.yml      # Blue окружение (v1.0.0)
├── docker-compose.green.yml     # Green окружение (v1.1.0)
├── docker-compose.nginx.yml     # Полный стек с Nginx LB
├── switch-to-blue.sh            # Скрипт переключения на Blue
├── switch-to-green.sh           # Скрипт переключения на Green
└── requirements.txt             # Python зависимости
```

## Быстрый старт

### 1. Сборка и запуск

```bash
docker compose -f docker-compose.nginx.yml up -d --build
```

### 2. Проверка health

```bash
curl -s http://localhost/health | jq .
```

Ответ:
```json
{
  "status": "ok",
  "model_version": "v1.0.0",
  "model_loaded": true
}
```

### 3. Выполнение предсказания

```bash
curl -X POST http://localhost/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[1,2,3,4,5,6]]}'
```

Ответ:
```json
{"predictions": [0]}
```

## Blue-Green Deployment

### Переключение на Green (v1.1.0)

```bash
./switch-to-green.sh
```

### Переключение на Blue (v1.0.0) / Откат

```bash
./switch-to-blue.sh
```

### Проверка текущей версии

```bash
curl -s http://localhost/health | jq .model_version
# "v1.1.0" или "v1.0.0"
```

## API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/health` | Статус сервиса и версия модели |
| POST | `/predict` | Инференс модели |

### POST /predict

**Request:**
```json
{
  "features": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]]
}
```

**Response:**
```json
{
  "predictions": [0]
}
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `MODEL_VERSION` | Версия модели | `v1.0.0` |
| `MODEL_PATH` | Путь к файлу модели | `models/model.pkl` |

## CI/CD

При пуше в `main` ветку GitHub Actions автоматически:
1. Собирает Docker образ
2. Пушит в GitHub Container Registry
3. Деплоит на облачный провайдер

### Необходимые секреты в GitHub:
- `CLOUD_TOKEN` — токен для деплоя

