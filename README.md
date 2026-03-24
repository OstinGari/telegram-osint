# osint-mobile-lab

Мобільно-керований (iPhone-first) каркас OSINT-пайплайну з розділенням ролей:

- **Collector** → збір публічних джерел.
- **Processor** → нормалізація, дедуплікація, базова оцінка.
- **Analyst** → формування пріоритетів та короткого звіту.
- **Dispatcher** → доставка результатів у Telegram.

## Архітектура

```text
SOURCE -> Collector -> Processor -> Analyst -> Dispatcher -> Telegram
```

Структура репозиторію:

```text
collectors/
processors/
analysts/
dispatcher/
scripts/
sources/
output/
.github/workflows/
notes/
```

## Швидкий старт

1. Додайте джерела у `sources/sources.json`.
2. Локальний запуск:

```bash
python scripts/run_pipeline.py
```

3. Для відправки в Telegram задайте змінні середовища:

```bash
export TELEGRAM_BOT_TOKEN='...'
export TELEGRAM_CHAT_ID='...'
python scripts/run_pipeline.py
```

## GitHub Actions

Workflow: `.github/workflows/osint.yml`

- Автозапуск: кожні 30 хвилин.
- Ручний запуск: `workflow_dispatch`.
- Секрети, які треба додати в **Settings → Secrets and variables → Actions**:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

## iPhone workflow

- Редагування: `github.dev` або GitHub Mobile.
- Перевірка ранiв та логів: GitHub Mobile → Actions.
- Отримання алертів: Telegram бот.

Детальніше: `notes/iphone-ops.md`.

## Безпека

- Використовуйте лише **публічні** джерела та дотримуйтесь законодавства.
- Telegram Bot API не дає доступу до приватних чатів/діалогів.
- Якщо токен бота коли-небудь був опублікований, **негайно перевипустіть його через @BotFather**.
