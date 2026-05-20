# market-ru-landing

CRO-анализ посадочных страниц на русском языке. Научный подход с использованием MECLABS, LIFT и других фреймворков.

## Что делает этот скилл

Проводит комплексный CRO-анализ (оптимизация коэффициента конверсии) любой посадочной страницы:

- Оценка по научным моделям: MECLABS, LIFT, Fogg Behavior Model
- Анализ 7 секций страницы: Hero, Ценностное предложение, Социальное доказательство, Функции, Обработка возражений, CTA, Футер
- Оценка копирайтинга по 5 измерениям
- Аудит форм и мобильной адаптивности
- Генерация A/B тестов и приоритизированных рекомендаций

## Особенности

### ICP Auto-Detect
Скилл автоматически определяет целевую аудиторию:
- Если ICP указан в команде → используется предоставленный
- Если ICP не указан → используется "generic problem-aware audience"

### Генерация отчётов
- **Python доступен** → агент использует скрипты (Markdown + HTML + JSON)
- **Python недоступен** → агент генерирует отчёты напрямую (fallback)

## Как это работает

### Шаг 1: Анализ страницы

LLM-агент анализирует страницу, применяя научные модели:
- **MECLABS** — формула конверсии (C = M×4 + V×3 + I×2 + F×2 + A×2)
- **LIFT** — 6 факторов влияния на конверсию
- **Fogg Behavior Model** — B = M × A × P
- **7 принципов Чалдини** — триггеры убеждения

### Шаг 2: Оценка

Каждая секция получает оценку 0-10, суммарный CRO Score 0-100:
- **0-40** — низкая конверсия, критические проблемы
- **40-70** — средняя конверсия, требует работы
- **70-100** — высокая конверсия, хорошее состояние

### Шаг 3: Отчёты

Генерируются три файла:
- **JSON** — сырые данные анализа
- **Markdown** — подробный текстовый отчёт
- **HTML** — красивая интерактивная страница с визуализацией

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

Или используй путь к глобальному npm:

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
/market-ru-landing <url>
```

### Пример

```
/market-ru-landing https://example.com
```

## Скрипты

| Скрипт | Назначение |
|--------|------------|
| `scripts/generate_landing_html.py` | Создаёт HTML-отчёт |
| `scripts/generate_landing_md.py` | Создаёт Markdown-отчёт |

Запуск вручную:

```bash
# Генерация HTML
python scripts/generate_landing_html.py <url>

# Генерация Markdown
python scripts/generate_landing_md.py <url>
```

## Метрики

| Метрика | Описание |
|---------|----------|
| **CRO (MECLABS)** | Итоговая оценка конверсии (0-100) по формуле M×4+V×3+I×2+F×2+A×2 |
| **LIFT** | Конверсионный потенциал (0-100%) — драйверы vs ингибиторы |
| **SS** | Scannability Score — сканируемость за 5 секунд |
| **TF** | Trust Factor — количество триггеров доверия |
| **RR** | Resonance Rate — соответствие болям аудитории |

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
- `example-landing-cro.md`
- `example-landing-cro.html`

## Лицензия

MIT License