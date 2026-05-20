# market-ru-landing

CRO-анализ посадочных страниц на русском языке. Научный подход с использованием MECLABS, LIFT, Fogg Behavior Model, Schwartz Awareness Levels и Cialdini's 7 Principles.

## Что делает этот скилл

Проводит комплексный CRO-анализ (оптимизация коэффициента конверсии) любой посадочной страницы:

- **5 научных метрик**: CRO (MECLABS), LIFT, SS (сканируемость), TF (доверие), RR (резонанс)
- **8-секционный отчёт**: 5 метрик + мобильный аудит + A/B тесты + приоритизированные исправления
- **Научные модели**: MECLABS, LIFT Framework, Fogg Behavior Model, Schwartz 5 Levels, Cialdini's 7 Principles
- **Интерактивный HTML-отчёт**: аккордеон-секции, hover-тултипы, цветовая индикация
- **Markdown-отчёт**: структурированный текст с таблицами и рекомендациями

## Особенности

### 5 метрик конверсии

| Метрика | Формула | Диапазон |
|---------|---------|----------|
| **CRO (MECLABS)** | M×4 + V×3 + I×2 + F×2 + A×2 | 0-100% |
| **LIFT** | (Драйверы - Ингибиторы + 16) / 54 × 100 | 0-100% |
| **SS** | Σ(оценка_блока × вес_блока) | 0-100% |
| **TF** | Σ(триггер × вес) | 0-N |
| **RR** | Σ(оценка_боли) / количество_болей | 0-100% |

### ICP Auto-Detect

Скилл автоматически определяет целевую аудиторию:
- Если ICP указан в команде → используется предоставленный
- Если ICP не указан → используется "generic problem-aware audience"

### Условные рекомендации

- **Score < 7/10** → минимум 3 findings + 2 fixes (все найденные проблемы)
- **Score ≥ 7/10** → 1-2 findings, fixes опционально
- Агент НЕ выдумывает проблемы которых нет на странице

### Генерация отчётов

- **Python доступен** → агент использует скрипты (Markdown + HTML + JSON)
- **Python недоступен** → агент генерирует отчёты напрямую (fallback)

## Как это работает

### Шаг 1: Анализ страницы

LLM-агент получает контент страницы и применяет научные модели:
- **MECLABS** — формула конверсии с весами (M×4, V×3, I×2, F×2, A×2)
- **LIFT** — 6 факторов: релевантность, ясность, срочность, ценность, тревога, отвлечение
- **Fogg Behavior Model** — B = M × A × P
- **Schwartz 5 Levels** — уровень осознанности аудитории
- **Cialdini's 7 Principles** — триггеры убеждения

### Шаг 2: Расчёт метрик

Агент рассчитывает 5 метрик по строгим формулам:
1. **CRO Score** — общая оценка конверсии (MECLABS)
2. **LIFT Score** — конверсионный потенциал
3. **Scannability Score** — что пользователь видит за 5 секунд
4. **Trust Factor** — количество и вес триггеров доверия
5. **Resonance Rate** — насколько закрыты боли ICP

### Шаг 3: Генерация отчётов

Скрипты генерируют три файла из JSON-данных:
- **JSON** — сырые данные анализа (для повторной генерации)
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
  "plugin": [
    "...existing plugins...",
    "market-ru-landing"
  ]
}
```

Или используй полный путь:

```json
{
  "plugin": [
    "...existing plugins...",
    "ПУТЬ_К_NPM/node_modules/market-ru-landing/.opencode/plugins/market-ru-landing.js"
  ]
}
```

Найти путь: `npm root -g`

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
/market-ru landing <url>
```

### Пример

```
/market-ru landing https://example.com
```

С опциональным ICP:

```
/market-ru landing https://example.com --icp "B2B SaaS, CTO, growth stage"
```

## Скрипты

| Скрипт | Назначение |
|--------|------------|
| `scripts/generate_landing_html.py` | Создаёт HTML-отчёт |
| `scripts/generate_landing_md.py` | Создаёт Markdown-отчёт |

Запуск вручную (требует JSON-файл):

```bash
# Генерация HTML
python scripts/generate_landing_html.py --json landing_analysis.json

# Генерация Markdown
python scripts/generate_landing_md.py --json landing_analysis.json
```

## Структура отчёта (8 секций)

| # | Секция | Описание |
|---|--------|----------|
| 01 | CRO (MECLABS) | 5 факторов с весами, формула, детализация |
| 02 | LIFT | 4 драйвера + 2 ингибитора, потенциал улучшения |
| 03 | Scannability | 6 блоков: H1, Subheadline, CTA, Структура, Визуал, Пробелы |
| 04 | Trust Factor | 13 типов триггеров доверия с весами |
| 05 | Resonance Rate | Боли ICP и степень их закрытия |
| 06 | Мобильный аудит | CTA, текст, формы, sticky CTA |
| 07 | A/B Тесты | 5 гипотез с вариантами A/B |
| 08 | Приоритизированные исправления | HIGH / MEDIUM / LOW с ожидаемым эффектом |

## Требования

- Python 3.x

**Важно:** Если Python установлен, агент ОБЯЗАН использовать скрипты
для генерации структурированных отчётов. Fallback-режим (без скриптов)
активируется только при отсутствии Python на системе.

## Для AI-агентов

Если ты AI-агент и хочешь установить этот скилл:

1. Прочитай файл `AGENT_INSTALL.md` в этом репозитории
2. Следуй инструкциям по установке для твоей IDE

## Примеры отчётов

См. папку `examples/`:
- `example-landing-cro.md` — Markdown-отчёт
- `example-landing-cro.html` — HTML-отчёт (откройте в браузере)

## Лицензия

MIT License
