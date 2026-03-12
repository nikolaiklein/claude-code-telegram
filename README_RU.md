# Claude Code Telegram Bot — README на русском

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

Telegram-бот для удалённого доступа к [Claude Code](https://claude.ai/code). Общайся с Claude о своих проектах из любого места — без терминала.

---

## Что это такое?

Бот соединяет Telegram с Claude Code — ты получаешь разговорный AI-интерфейс для работы с кодом:

- **Общайся естественно** — проси Claude анализировать, редактировать или объяснять код на человеческом языке
- **Контекст сохраняется** — автоматическая персистентность сессии по каждому проекту
- **Работай с телефона** — с любого устройства через Telegram
- **Получай уведомления** — от вебхуков, крон-задач, CI/CD событий
- **Безопасность** — встроенная аутентификация, изоляция директорий, аудит-лог

---

## Быстрый старт

### Пример диалога

```
Ты: Помоги добавить обработку ошибок в src/api.py

Бот: Анализирую src/api.py...
     [Claude читает код, предлагает улучшения и может сразу внести изменения]

Ты: Отлично. Теперь запусти тесты, убедись что ничего не сломалось.

Бот: Запускаю pytest...
     Все 47 тестов прошли успешно.
```

### 1. Что нужно

- **Python 3.11+**
- **Claude Code CLI** — [установить здесь](https://claude.ai/code)
- **Токен Telegram-бота** — получить у [@BotFather](https://t.me/botfather)

### 2. Установка

#### Вариант А: Из релиза (рекомендуется)

```bash
uv tool install git+https://github.com/RichardAtCT/claude-code-telegram@v1.3.0
# или через pip
pip install git+https://github.com/RichardAtCT/claude-code-telegram@v1.3.0
```

#### Вариант Б: Из исходников (для разработки)

```bash
git clone https://github.com/nikolaiklein/claude-code-telegram.git
cd claude-code-telegram
make dev  # требует Poetry
```

> ⚠️ Для стабильности всегда ставь конкретный тег, не `main`.

### 3. Конфигурация

```bash
cp .env.example .env
# Открой .env и заполни:
```

**Минимально необходимые параметры:**
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABC-...     # токен от BotFather
TELEGRAM_BOT_USERNAME=my_claude_bot       # username бота
APPROVED_DIRECTORY=/root                  # базовая директория проектов
ALLOWED_USERS=123456789                   # твой Telegram user ID
```

> Как узнать свой ID: напиши боту [@userinfobot](https://t.me/userinfobot)

### 4. Запуск

```bash
make run          # Продакшн
make run-debug    # С debug-логами
```

---

## Режимы работы

### 🤖 Агентный режим (по умолчанию)

Разговорный режим. Просто общайся с Claude — никаких специальных команд.

**Команды:** `/start`, `/new`, `/status`, `/verbose`, `/repo`  
Если `ENABLE_PROJECT_THREADS=true`: `/sync_threads`

**Пример:**
```
Ты: Что за файлы в этом проекте?
Бот: Working... (3 сек)
     📖 Read / 📂 LS
     Бот: [описывает структуру проекта]

Ты: Добавь retry-декоратор в HTTP-клиент
Бот: Working... (8 сек)
     📖 Read: http_client.py
     ✏️ Edit: http_client.py
     💻 Bash: pytest tests/ -v
     [показывает изменения и результаты тестов]
```

#### Уровни подробности `/verbose 0|1|2`

| Уровень | Что показывает |
|---------|---------------|
| **0** (тихий) | Только финальный ответ |
| **1** (нормальный, по умолчанию) | Названия инструментов + фрагменты рассуждений |
| **2** (подробный) | Инструменты с входными данными + полный текст рассуждений |

#### ⏹ Кнопка Stop (добавлено нами)

При запуске задачи появляется кнопка **⏹ Stop** — нажми чтобы прервать Claude прямо в процессе работы, не дожидаясь завершения.

#### Работа с GitHub

Claude Code знает `gh` CLI и `git`. Авторизуйся: `gh auth login`, потом работай разговорно:

```
Ты: Покажи мои репозитории по мониторингу
Ты: Клонируй uptime-monitor
Ты: /repo  →  выбери проект
Ты: Создай fix-ветку и запушь
```

---

### 🖥 Классический режим

Установи `AGENTIC_MODE=false` — получишь 13 команд в стиле терминала.

**Команды:** `/start`, `/help`, `/new`, `/continue`, `/end`, `/status`, `/cd`, `/ls`, `/pwd`, `/projects`, `/export`, `/actions`, `/git`

```
Ты: /cd my-web-app
Бот: Директория изменена: my-web-app/

Ты: /actions
Бот: [Запустить тесты] [Установить зависимости] [Форматировать код]
```

---

## Автоматизация по событиям

- **Вебхуки** — получай GitHub-события (push, PR, issues) через Claude для авто-ревью
- **Планировщик** — запускай задачи по крон-расписанию (например, ежедневная проверка здоровья кода)
- **Уведомления** — доставка ответов агента в Telegram-чаты

Включить: `ENABLE_API_SERVER=true` и `ENABLE_SCHEDULER=true`

---

## Конфигурация (.env)

### Обязательные

```bash
TELEGRAM_BOT_TOKEN=...           # от BotFather
TELEGRAM_BOT_USERNAME=...        # username бота
APPROVED_DIRECTORY=...           # базовая директория (например /root)
ALLOWED_USERS=123456789          # твой Telegram ID
```

### Основные опции

```bash
# Claude
ANTHROPIC_API_KEY=sk-ant-...     # API ключ (не нужен если используешь CLI auth)
CLAUDE_MAX_COST_PER_USER=10.0    # лимит расходов на пользователя (USD)
CLAUDE_TIMEOUT_SECONDS=300       # таймаут операции
CLAUDE_MAX_TURNS=20              # макс. число ходов агента

# Режим
AGENTIC_MODE=true                # агентный (по умолчанию) или классический
VERBOSE_LEVEL=1                  # 0=тихо, 1=нормально, 2=подробно

# Ограничение запросов
RATE_LIMIT_REQUESTS=10           # запросов в окне
RATE_LIMIT_WINDOW=60             # окно в секундах
```

### Топики по проектам (Project Threads)

```bash
ENABLE_PROJECT_THREADS=true              # включить маршрутизацию по топикам
PROJECT_THREADS_MODE=private             # private или group
PROJECTS_CONFIG_PATH=config/projects.yaml  # YAML-реестр проектов
PROJECT_THREADS_CHAT_ID=-1001234567890   # ID группы (только для group-режима)
```

В строгом режиме вне топиков работают только `/start` и `/sync_threads`.

---

## Возможности

### Работает сейчас ✅

- Агентный разговорный режим
- Классический режим с 13 командами
- Полная интеграция Claude Code (SDK + CLI fallback)
- Персистентность сессий по пользователю/директории
- Многоуровневая аутентификация (whitelist + токен)
- Ограничение запросов (token bucket)
- Изоляция директорий от path traversal
- Загрузка файлов с извлечением архивов
- Загрузка изображений с анализом
- Транскрипция голосовых (Mistral Voxtral / OpenAI Whisper)
- Git-интеграция
- Быстрые действия (inline-кнопки)
- Экспорт сессий: Markdown, HTML, JSON
- SQLite с миграциями
- Трекинг использования и стоимости
- Аудит-лог
- Вебхук-сервер (GitHub HMAC-SHA256 + Bearer token)
- Планировщик задач (cron)
- ⏹ Кнопка Stop для прерывания (добавлено нами)
- Загрузка PDF, DOCX, XLSX, PNG, JPG и др. (добавлено нами)
- Сохранение загруженных файлов в /root/uploads/ (добавлено нами)

### Планируется 🔜

- Плагин-система для сторонних расширений

---

## Безопасность

- **Контроль доступа** — whitelist пользователей
- **Изоляция директорий** — только approved_directory
- **Ограничение запросов** — по количеству и стоимости
- **Валидация входных данных** — защита от инъекций
- **Аутентификация вебхуков** — HMAC-SHA256 и Bearer token
- **Аудит-лог** — полное отслеживание действий

---

## Разработка

```bash
make dev           # Установка зависимостей
make test          # Тесты с покрытием
make lint          # Black + isort + flake8 + mypy
make format        # Автоформатирование
make run-debug     # Запуск с debug-логами
```

### Версионирование

```bash
make bump-patch    # 1.2.0 → 1.2.1 (багфиксы)
make bump-minor    # 1.2.0 → 1.3.0 (новые фичи)
make bump-major    # 1.2.0 → 2.0.0 (ломающие изменения)
```

---

## Лицензия

MIT — см. [LICENSE](LICENSE).

---

*Форк: [nikolaiklein/claude-code-telegram](https://github.com/nikolaiklein/claude-code-telegram)*  
*Оригинал: [RichardAtCT/claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram)*
