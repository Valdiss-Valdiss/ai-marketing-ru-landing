# market-ru-landing

CRO-анализ посадочных страниц с научным подходом. Автоматический анализ + подробные отчёты.

## Что делает этот скилл

Проводит CRO-анализ (оптимизация коэффициента конверсии) любой посадочной страницы на основе 5 моделей оценки:

- **MECLABS** — формула конверсии (мотивация ×4 + ценностное предложение ×3 + стимулы ×2 + трение ×2 + тревога ×2)
- **LIFT Framework** — 6 факторов конверсии (релевантность, ясность, срочность, ценность, тревога, отвлечение)
- **Scannability Score** — что пользователь видит за 5 секунд (6 блоков: H1, Subheadline, CTA, Структура, Визуал, Пробелы)
- **Trust Factor** — количество и вес триггеров доверия (13 типов от 0.3 до 2.0)
- **Resonance Rate** — насколько закрыты боли ICP (0/25/50/75/100%)

## Как это работает

### Шаг 1: Анализ страницы

LLM-агент получает контент страницы и рассчитывает 5 метрик:
- **MECLABS** — 5 факторов с весами
- **LIFT** — 4 драйвера + 2 ингибитора
- **SS** — 6 блоков сканируемости
- **TF** — 13 типов триггеров доверия
- **RR** — боли ICP и степень их закрытия

### Шаг 2: Генерация отчётов

Скрипты генерируют три файла из JSON-данных:
- **JSON** — сырые данные анализа
- **Markdown** — подробный текстовый отчёт с 8 секциями
- **HTML** — интерактивная страница с аккордеоном, тултипами, визуализацией

## Установка

### OpenCode

```bash
npm install -g market-ru-landing
```

После установки добавь плагин в `opencode.json`:

```json
{
  "plugins": [
    "...existing plugins...",
    "market-ru-landing"
  ]
}
```

### Claude Code

```bash
curl -fsSL https://raw.githubusercontent.com/Valdiss-Valdiss/ai-marketing-ru-landing/main/install.sh | bash
```

Или вручную:

```bash
git clone https://github.com/Valdiss-Valdiss/ai-marketing-ru-landing.git
cd ai-marketing-ru-landing
./install.sh
```

## Использование

```
/market-ru-landing <url>
```

### Пример

```
/market-ru-landing https://example.com
```

### С опциональным описанием аудитории

```
/market-ru-landing https://example.com
Целевая аудитория: B2B SaaS, CTO, growth stage
```

## Скрипты

| Скрипт | Назначение |
|--------|------------|
| `scripts/generate_landing_md.py` | Создаёт Markdown-отчёт |
| `scripts/generate_landing_html.py` | Создаёт HTML-страницу |

Запуск вручную (требует JSON-файл):

```bash
python scripts/generate_landing_md.py --json landing_analysis.json
python scripts/generate_landing_html.py --json landing_analysis.json
```

## Требования

- [Python 3.x](https://www.python.org/downloads/) — для генерации отчётов
- [OpenCode](https://opencode.ai/) или [Claude Code](https://claude.com/product/claude-code) — AI-агент для анализа

## Для AI-агентов

Если ты AI-агент и хочешь установить этот скилл:

1. Прочитай файл `AGENT_INSTALL.md` в этом репозитории
2. Следуй инструкциям по установке для твоей IDE

## Метрики

| Метрика | Описание | Диапазон |
|---------|----------|----------|
| CRO (MECLABS) | Общий коэффициент конверсии | 0-100% |
| LIFT | Конверсионный потенциал | 0-100% |
| SS | Scannability Score (% за 5 сек) | 0-100% |
| TF | Trust Factor (триггеры доверия) | 0-N |
| RR | Resonance Rate (боли аудитории) | 0-100% |

## Лицензия

MIT License
