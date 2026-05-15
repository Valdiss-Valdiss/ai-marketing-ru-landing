#!/usr/bin/env python3
"""
Generate Landing Page CRO Audit Markdown Report — AI Marketing Claude Code Skills
Создаёт профессиональный отчёт в формате Markdown на основе данных анализа.
"""

import sys
import os
import json
from datetime import datetime
from urllib.parse import urlparse


def escape_md(text):
    """Экранирование специальных символов Markdown."""
    if not isinstance(text, str):
        text = str(text)
    return (text
            .replace("\\", "\\\\")
            .replace("*", "\\*")
            .replace("_", "\\_")
            .replace("#", "\\#")
            .replace("[", "\\[")
            .replace("]", "\\]")
            .replace("(", "\\(")
            .replace(")", "\\)")
            .replace("|", "\\|")
            .replace("`", "\\`")
            .replace(">", "\\>")
            .replace("<", "\\<"))


def truncate(text, length=80):
    """Обрезка текста с добавлением многоточия."""
    if not text:
        return ""
    text = str(text)
    if len(text) > length:
        return text[:length] + "..."
    return text


def get_status_icon(score, max_score):
    """Возвращает иконку статуса на основе соотношения баллов."""
    if max_score == 0:
        return "❌"
    ratio = score / max_score
    if ratio >= 0.8:
        return "✅"
    elif ratio >= 0.5:
        return "⚠️"
    else:
        return "❌"


def get_status_text(score, max_score):
    """Возвращает текст статуса."""
    if max_score == 0:
        return "Не пройдено"
    ratio = score / max_score
    if ratio >= 0.8:
        return "Хорошо"
    elif ratio >= 0.5:
        return "Требует работы"
    else:
        return "Не пройдено"


def get_score_label(score, max_score):
    """Возвращает метку оценки (высокий/средний/низкий)."""
    if max_score == 0:
        return "низкий"
    ratio = score / max_score
    if ratio >= 0.7:
        return "высокий"
    elif ratio >= 0.4:
        return "средний"
    else:
        return "низкий"


def get_timestamp_filename(url, prefix="LANDING-CRO"):
    """Генерация имени файла с timestamp."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"{prefix}-{domain}-{timestamp}"


def format_metric(value, suffix=""):
    """Форматирование метрики с суффиксом."""
    if value is None:
        return "—"
    return f"{value}{suffix}"


def generate_section_score(sections_data, section_name):
    """Генерация строки с оценкой секции."""
    score = sections_data.get(section_name, {}).get("score", 0)
    max_score = sections_data.get(section_name, {}).get("max", 10)
    icon = get_status_icon(score, max_score)
    label = get_score_label(score, max_score)
    return f"{icon} {score}/{max_score} ({label})"


def generate_md_report(url, analysis, icp_description="generic problem-aware audience"):
    """Генерация полного Markdown отчёта."""
    scores = analysis.get("scores", {})
    sections = analysis.get("sections", {})
    metrics = analysis.get("metrics", {})
    copy_score = analysis.get("copy_score", {})
    form_audit = analysis.get("form_audit", {})
    mobile_audit = analysis.get("mobile_audit", {})
    ab_tests = analysis.get("ab_tests", [])
    prioritized_fixes = analysis.get("prioritized_fixes", {})

    date_str = datetime.now().strftime("%d %m %Y, %H:%M:%S")
    parsed = urlparse(url)
    domain = parsed.netloc

    # Основные метрики
    cro_score = scores.get("total", 0)
    vpi = metrics.get("vpi", 0)
    ss = metrics.get("scannability_score", 0)
    tf = metrics.get("trust_factor", 0)
    rr = metrics.get("resonance_rate", 0)

    # Весса секций
    section_weights = {
        "hero": 25,
        "value_proposition": 20,
        "social_proof": 15,
        "features": 15,
        "objection_handling": 10,
        "cta": 10,
        "footer": 5
    }

    # Формируем таблицу секций
    sections_table_rows = ""
    for section_key, weight in section_weights.items():
        section_data = sections.get(section_key, {})
        score = section_data.get("score", 0)
        max_score = section_data.get("max", 10)
        icon = get_status_icon(score, max_score)
        label = section_data.get("label", section_key.replace("_", " ").title())
        contribution = score * weight / 10
        sections_table_rows += f"| {label} | {icon} {score}/{max_score} | {weight}% | {contribution:.1f} |\n"

    sections_table = f"""| Секция | Оценка | Вес | Вклад |
|------------|--------|-----|-------|
{sections_table_rows}"""

    # Копирайтинг - поддержка flat и nested структуры
    if "dimensions" in copy_score and copy_score["dimensions"]:
        dimensions = copy_score["dimensions"]
    else:
        dimensions = copy_score
    clarity = dimensions.get("clarity", 0)
    urgency = dimensions.get("urgency", 0)
    specificity = dimensions.get("specificity", 0)
    proof = dimensions.get("proof", 0)
    action_orientation = dimensions.get("action") or dimensions.get("action_orientation", 0)
    copy_total = copy_score.get("total", 0)

    # Копирайтинг таблица
    copy_table = f"""| Измерение | Оценка |
|-------------|--------|
| Ясность (Clarity) | {get_status_icon(clarity, 10)} {clarity}/10 |
| Срочность (Urgency) | {get_status_icon(urgency, 10)} {urgency}/10 |
| Конкретность (Specificity) | {get_status_icon(specificity, 10)} {specificity}/10 |
| Доказательность (Proof) | {get_status_icon(proof, 10)} {proof}/10 |
| Ориентация на действие | {get_status_icon(action_orientation, 10)} {action_orientation}/10 |
| **ИТОГО** | **{get_status_icon(copy_total, 100)} {copy_total}/100** |"""

    # Детали секций - единый формат для всех
    def format_findings(findings, max_count=10):
        if not findings:
            return "— На основе анализа данные не получены."
        result = ""
        for i, finding in enumerate(findings[:max_count], 1):
            if isinstance(finding, dict):
                text = finding.get("text", "")
                impact = finding.get("impact", "")
                finding_type = finding.get("type", "")
                icon = "✅" if finding_type == "strength" else ("⚠️" if finding_type == "issue" else "ℹ️")
                result += f"{i}. {icon} **{text}**"
                if impact:
                    result += f"\n   → Влияние: {impact}"
                result += "\n"
            else:
                result += f"{i}. {finding}\n"
        return result.rstrip()

    def format_fixes_section(fixes, max_count=10):
        if not fixes:
            return "— Рекомендации не требуются — секция в хорошем состоянии."
        result = ""
        for i, fix in enumerate(fixes[:max_count], 1):
            if isinstance(fix, dict):
                priority = fix.get("priority", "MEDIUM")
                text = fix.get("text", "")
                impact = fix.get("impact", "")
                priority_emoji = "🔴" if priority == "HIGH" else ("🟡" if priority == "MEDIUM" else "🟢")
                result += f"{i}. {priority_emoji} **{priority}**: {text}"
                if impact:
                    result += f"\n   → Ожидаемый эффект: {impact}"
                result += "\n"
            else:
                result += f"{i}. {fix}\n"
        return result.rstrip()

    def format_section(section_key, section_num, section_title):
        section_data = sections.get(section_key, {})
        score = section_data.get("score", 0)
        max_score = section_data.get("max", 10)
        weight = section_weights.get(section_key, 0)
        contribution = score * weight / 10
        findings = section_data.get("findings", [])
        fixes = section_data.get("fixes", [])

        return f"""
## {section_num}. {section_title} [{score}/{max_score}]

**Вес:** {weight}% | **Вклад в итоговый score:** {contribution:.1f}

### Находки
{format_findings(findings)}

### Приоритетные исправления
{format_fixes_section(fixes)}
"""

    # MECLABS формула и пояснения
    motivation = metrics.get("motivation", 0)
    value_prop = metrics.get("value_proposition", 0)
    incentive = metrics.get("incentive", 0)
    friction = metrics.get("friction", 0)
    anxiety = metrics.get("anxiety", 0)

    meclabs_formula = f"{motivation}×4 + {value_prop}×3 + {incentive}×2 + {friction}×2 + {anxiety}×2 = {cro_score}"

    meclabs_details = f"""
### MECLABS Формула конверсии

```
C = M×4 + V×3 + I×2 + F×2 + A×2
{meclabs_formula}
```

Где:
- **M (Motivation)** — Мотивация: {motivation}/10 — Внутренняя мотивация пользователя. Без мотивации никакой дизайн не сработает.
- **V (Value Proposition)** — Ценностное предложение: {value_prop}/10 — Сила обещания продукта. Должно быть уникальным и конкретным.
- **I (Incentive)** — Стимулы: {incentive}/10 — Дополнительные триггеры: бонусы, скидки, urgency. Катализатор действия.
- **F (Friction)** — Трение: {friction}/10 — Всё, что усложняет действие. Каждое лишнее действие = потерянный клиент.
- **A (Anxiety)** — Тревога: {anxiety}/10 — Страх совершить ошибку. Убивает конверсию рядом с CTA.

**Важно:** Оценки M, V, I, F, A — субъективны и основаны на контент-анализе страницы. Для точного расчёта используйте A/B тесты.
"""

    # LIFT факторы
    lift_relevance = metrics.get("lift_relevance", 0)
    lift_clarity = metrics.get("lift_clarity", 0)
    lift_urgency = metrics.get("lift_urgency", 0)
    lift_value = metrics.get("lift_value", 0)
    lift_anxiety = metrics.get("lift_anxiety", 0)
    lift_distraction = metrics.get("lift_distraction", 0)

    lift_details = f"""
### LIFT Framework

| Фактор | Оценка | Роль | Суть |
|--------|--------|------|------|
| Релевантность | {lift_relevance}/10 | Драйвер | Заголовок соответствует ожиданиям аудитории. Если нет — уходит. |
| Ясность | {lift_clarity}/10 | Драйвер | Простота языка. Пользователь должен мгновенно понять, что делать. |
| Срочность | {lift_urgency}/10 | Драйвер | Временные ограничения. Мотивирует действовать СЕЙЧАС. |
| Ценностное предложение | {lift_value}/10 | Базис | Соотношение выгод и затрат. 'Что получу vs сколько стоит'. |
| Тревога | {lift_anxiety}/10 | Ингибитор | Отсутствие доверительных сигналов. Максимальна рядом с CTA. |
| Отвлечение | {lift_distraction}/10 | Ингибитор | Лишние ссылки, навигация. Всё, что уводит от цели. |

**Формула:** Конверсия = Σ(Драйверы) - Σ(Ингибиторы)
"""

    # Форма аудита
    form_fields = form_audit.get("field_count", "—")
    form_button = form_audit.get("button_text", "—")
    form_recommendation = form_audit.get("recommendation", "—")
    form_fixes = form_audit.get("fixes", [])

    form_audit_section = f"""
## Аудит форм

| Параметр | Текущее | Рекомендация |
|----------|---------|--------------|
| Количество полей | {form_fields} | Максимум 3-5 для лидогенерации |
| Текст кнопки | {form_button} | Описать ценность, а не действие |

### Рекомендация
{form_recommendation if form_recommendation else "—"}

### Приоритетные исправления
{format_fixes_section(form_fixes)}
"""

    # Мобильный аудит
    mobile_cta = mobile_audit.get("cta_accessible", "—")
    mobile_text = mobile_audit.get("text_readable", "—")
    mobile_recommendation = mobile_audit.get("recommendation", "—")

    mobile_audit_section = f"""
## Мобильный аудит

| Параметр | Статус | Рекомендация |
|----------|--------|--------------|
| CTA доступен (thumb zone) | {mobile_cta} | — |
| Текст читаемый (16px+) | {mobile_text} | — |

### Рекомендация
{mobile_recommendation if mobile_recommendation else "—"}
"""

    # A/B тесты
    ab_tests_md = ""
    if ab_tests:
        for i, test in enumerate(ab_tests[:10], 1):
            hypothesis = test.get("hypothesis", "")
            if hypothesis:
                ab_tests_md += f"{i}. {hypothesis}\n\n"
    if not ab_tests_md:
        ab_tests_md = "— A/B тесты не сгенерированы. Для точного определения влияния изменений необходимо тестирование."

    ab_tests_section = f"""
## A/B Тесты (гипотезы)

{ab_tests_md}

**Шаблон гипотезы:** 'Если мы [изменим X], тогда [метрика Y] [улуччшится/увеличится], потому что [причина Z].'
"""

    # Приоритизированные фиксы - собираем ВСЕ фиксы из всех секций
    all_fixes = []
    for section_key, section_data in sections.items():
        for fix in section_data.get("fixes", []):
            fix_copy = fix.copy()
            fix_copy["section"] = section_key
            all_fixes.append(fix_copy)

    def format_all_fixes(fixes_list, max_count=20):
        if not fixes_list:
            return "— Значительных проблем не обнаружено."
        result = ""
        for i, fix in enumerate(fixes_list[:max_count], 1):
            section = fix.get("section", "").replace("_", " ").title()
            text = fix.get("text", "")
            impact = fix.get("impact", "")
            priority = fix.get("priority", "MEDIUM")
            priority_emoji = "🔴" if priority == "HIGH" else ("🟡" if priority == "MEDIUM" else "🟢")
            result += f"{i}. {priority_emoji} **{section}**: {text}"
            if impact:
                result += f"\n   → {impact}"
            result += "\n"
        return result.rstrip()

    # Разделяем по приоритетам
    quick_wins = [f for f in all_fixes if f.get("priority", "").upper() in ("HIGH", "CRITICAL")]
    medium_term = [f for f in all_fixes if f.get("priority", "").upper() == "MEDIUM"]
    strategic = [f for f in all_fixes if f.get("priority", "").upper() not in ("HIGH", "CRITICAL", "MEDIUM")]

    prioritized_section = f"""
## Приоритизированный список исправлений

### Быстрые победы (эта неделя)
{format_all_fixes(quick_wins)}

### Среднесрочные (этот месяц)
{format_all_fixes(medium_term)}

### Стратегические (этот квартал)
{format_all_fixes(strategic)}
"""

    # Собираем все секции
    sections_md = ""
    section_order = [
        ("hero", "1", "Hero-секция"),
        ("value_proposition", "2", "Ценностное предложение"),
        ("social_proof", "3", "Социальное доказательство"),
        ("features", "4", "Функции и выгоды"),
        ("objection_handling", "5", "Обработка возражений"),
        ("cta", "6", "Призыв к действию"),
        ("footer", "7", "Футер и элементы"),
    ]

    for section_key, section_num, section_title in section_order:
        sections_md += format_section(section_key, section_num, section_title)

    # Footer CTA
    footer_cta = f"""
---

## Хотите радикально повысить конверсию?

Мы внедряем передовые инструменты ИИ для кратного роста конверсии. Напишите нам!

**[Хочу увеличить конверсию](https://open4.dev/#contact)**

---

*Отчёт сгенерирован ИИ. ИИ может ошибаться — проверяйте рекомендации перед внедрением.*
"""

    md = f"""# CRO-анализ посадочной страницы

**URL:** [{url}]({url})
**Дата:** {date_str}
**Целевая аудитория:** {icp_description}

---

## CRO Score: {cro_score}/100

### Метрики эффективности

| Метрика | Значение | Описание |
|---------|----------|----------|
| **VPI** (Value Proposition Index) | {vpi}/10 | Сила ценностного предложения |
| **SS** (Scannability Score) | {ss}% | Сканируемость за 5 секунд |
| **TF** (Trust Factor) | {tf} триггеров | Фактор доверия |
| **RR** (Resonance Rate) | {rr}% | Соответствие болям аудитории |

{meclabs_details}

{lift_details}

---

## Детализация по секциям

{sections_table}

---

{sections_md}

---

## Оценка копирайтинга [{copy_total}/100]

{copy_table}

---

{form_audit_section}

---

{mobile_audit_section}

---

{ab_tests_section}

---

{prioritized_section}

{footer_cta}
"""

    return md


def main():
    url = None
    icp_description = "generic problem-aware audience"
    output_dir = os.environ.get("OPENCODE_WORKING_DIR", os.getcwd())
    json_file = None

    for i, arg in enumerate(sys.argv[1:], 0):
        if arg == "--json" and i + 1 < len(sys.argv):
            json_file = sys.argv[i + 1]
        elif arg == "--url" and i + 1 < len(sys.argv):
            url = sys.argv[i + 1]
        elif arg == "--icp" and i + 1 < len(sys.argv):
            icp_description = sys.argv[i + 1]
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
        elif not arg.startswith("--") and url is None:
            url = arg

    if not url and not json_file:
        print("Использование: python3 generate_landing_md.py --json <file.json> [--url <url>] [--icp <description>] [--output <dir>]")
        print("Или: python3 generate_landing_md.py <url> [icp_description] [output_dir]")
        sys.exit(1)

    if json_file:
        print(f"Чтение JSON из: {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        url = data.get("url", url or "unknown")
        icp_description = data.get("icp", icp_description)
        analysis = data.get("analysis", data)
    else:
        if not url.startswith("http"):
            url = "https://" + url
        print(f"Анализ: {url}")
        print("Внимание: analyze_landing.py не используется. Используем пустую структуру.")
        analysis = {
            "scores": {"total": 0},
            "sections": {},
            "metrics": {},
            "copy_score": {},
            "form_audit": {},
            "mobile_audit": {},
            "ab_tests": [],
            "prioritized_fixes": {}
        }

    md = generate_md_report(url, analysis, icp_description)

    os.makedirs(output_dir, exist_ok=True)
    filename = get_timestamp_filename(url, "LANDING-CRO") + ".md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Markdown отчёт сохранён: {filepath}")
    return filepath


if __name__ == "__main__":
    main()