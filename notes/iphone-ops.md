# iPhone Operations Playbook

## 1) Стандартний цикл

1. Відкрити репозиторій через `https://github.dev/<user>/<repo>`.
2. Оновити джерела в `sources/sources.json`.
3. За потреби змінити логіку в `collectors/`, `processors/`, `analysts/`, `dispatcher/`.
4. Коміт і пуш.
5. Запустити workflow вручну з GitHub Mobile (Actions → OSINT Monitor → Run workflow).
6. Перевірити алерт у Telegram.

## 2) Telegram як контрольна панель (далі)

Рекомендовані команди для майбутнього розширення:

- `/status` — статус останнього ранa.
- `/run` — запуск pipeline on-demand.
- `/add_source` — додати джерело.
- `/remove_source` — видалити джерело.

## 3) Обмеження

- На iPhone незручно робити важкі обчислення/ML.
- GitHub Actions має ліміти рантайму.
- Telegram Bot API обмежений публічним/дозволеним доступом.
