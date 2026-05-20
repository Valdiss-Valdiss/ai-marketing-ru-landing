#!/usr/bin/env python3
"""
Generate Landing Page CRO Audit Markdown Report — AI Marketing Claude Code Skills
Создаёт профессиональный отчёт в формате Markdown на основе данных анализа.

Новая структура (8 секций):
01. CRO (MECLABS) — 5 факторов
02. LIFT — 6 факторов
03. SS (Scannability) — 6 блоков
04. TF (Trust Factor) — триггеры
05. RR (Resonance Rate) — боли ICP
06. Мобильный аудит
07. A/B Тесты
08. Приоритизированные исправления
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


def format_findings(findings, max_count=10):
    if not findings:
        return "— На основе анализа данные не получены."
    result = ""
    for i, finding in enumerate(findings[:max_count], 1):
        if isinstance(finding, dict):
            text = finding.get("text", "")
            impact = finding.get("impact", "")
            result += f"{i}. {text}"
            if impact:
                result += f"\n   → Влияние: {impact}"
            result += "\n"
        else:
            result += f"{i}. {finding}\n"
    return result.rstrip()


def format_fixes(fixes, max_count=10):
    if not fixes:
        return "— Рекомендации не требуются."
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


def generate_md_report(url, analysis, icp_description="generic problem-aware audience"):
    """Генерация полного Markdown отчёта."""
    metrics = analysis.get("metrics", {})
    cro_data = analysis.get("cro", {})
    lift_data = analysis.get("lift", {})
    ss_data = analysis.get("scannability", {})
    trust_data = analysis.get("trust", {})
    resonance_data = analysis.get("resonance", {})
    mobile_data = analysis.get("mobile_audit", {})
    ab_tests = analysis.get("ab_tests", [])
    all_fixes = analysis.get("all_fixes", [])

    date_str = datetime.now().strftime("%d %m %Y, %H:%M:%S")
    parsed = urlparse(url)
    domain = parsed.netloc

    cro_score = metrics.get("cro_score", 0)
    lift_score = metrics.get("lift_score", 0)
    ss = metrics.get("scannability_score", 0)
    tf = metrics.get("trust_factor", 0)
    rr = metrics.get("resonance_rate", 0)

    # ===== METRICS TABLE =====
    metrics_table = f"""| Метрика | Значение | Описание |
|---------|----------|----------|
| **CRO (MECLABS)** | {cro_score}% | Общий коэффициент конверсии |
| **LIFT** | {lift_score}% | Конверсионный потенциал |
| **SS** | {ss}% | Сканируемость за 5 секунд |
| **TF** | {tf} | Фактор доверия (триггеры) |
| **RR** | {rr}% | Соответствие болям аудитории |
"""

    # ===== MECLABS =====
    motivation = metrics.get("motivation", 0)
    value_prop = metrics.get("value_proposition", 0)
    incentive = metrics.get("incentive", 0)
    friction = metrics.get("friction", 0)
    anxiety = metrics.get("anxiety", 0)

    m_comp = motivation * 4
    v_comp = value_prop * 3
    i_comp = incentive * 2
    f_comp = friction * 2
    a_comp = anxiety * 2

    meclabs_formula = f"{motivation}×4 + {value_prop}×3 + {incentive}×2 + {friction}×2 + {anxiety}×2 = {cro_score}%"

    meclabs_table = f"""| Фактор | Оценка | Компонент | Уровень |
|--------|--------|-----------|---------|
| **M** (Мотивация) | {motivation}/10 | {m_comp} | {get_score_label(motivation, 10)} |
| **V** (Ценностное предложение) | {value_prop}/10 | {v_comp} | {get_score_label(value_prop, 10)} |
| **I** (Стимулы) | {incentive}/10 | {i_comp} | {get_score_label(incentive, 10)} |
| **F** (Трение) | {friction}/10 | {f_comp} | {get_score_label(friction, 10)} |
| **A** (Тревога) | {anxiety}/10 | {a_comp} | {get_score_label(anxiety, 10)} |
| **ИТОГО** | | **{cro_score}%** | {get_score_label(cro_score, 100)} |
"""

    # MECLABS findings/fixes per factor
    cro_factors = cro_data.get("factors", {})
    meclabs_details = ""
    for key, label in [("motivation", "M — Мотивация"), ("value_proposition", "V — Ценностное предложение"),
                        ("incentive", "I — Стимулы"), ("friction", "F — Трение"), ("anxiety", "A — Тревога")]:
        factor = cro_factors.get(key, {})
        findings = factor.get("findings", [])
        fixes = factor.get("fixes", [])
        meclabs_details += f"""
##### {label} [{factor.get('score', 0)}/10]

**Найдено:**
{format_findings(findings)}

**Рекомендации:**
{format_fixes(fixes)}
"""

    # ===== LIFT =====
    lift_relevance = metrics.get("lift_relevance", 0)
    lift_clarity = metrics.get("lift_clarity", 0)
    lift_urgency = metrics.get("lift_urgency", 0)
    lift_value = metrics.get("lift_value", 0)
    lift_anxiety = metrics.get("lift_anxiety", 0)
    lift_distraction = metrics.get("lift_distraction", 0)

    drivers = lift_relevance + lift_clarity + lift_urgency + lift_value
    inhibitors = lift_anxiety + lift_distraction
    lift_raw = drivers - inhibitors

    lift_table = f"""| Фактор | Оценка | Роль |
|--------|--------|------|
| Релевантность | {lift_relevance}/10 | Драйвер |
| Ясность | {lift_clarity}/10 | Драйвер |
| Срочность | {lift_urgency}/10 | Драйвер |
| Ценность | {lift_value}/10 | Базис |
| Тревога | {lift_anxiety}/10 | Ингибитор |
| Отвлечение | {lift_distraction}/10 | Ингибитор |
| **LIFT_raw** | **{lift_raw}** | |
| **LIFT** | **{lift_score}%** | |
"""

    lift_factors = lift_data.get("factors", {})
    lift_details = ""
    for key, label in [("relevance", "Релевантность"), ("clarity", "Ясность"), ("urgency", "Срочность"),
                        ("value", "Ценность"), ("anxiety", "Тревога"), ("distraction", "Отвлечение")]:
        factor = lift_factors.get(key, {})
        findings = factor.get("findings", [])
        fixes = factor.get("fixes", [])
        lift_details += f"""
##### {label} [{factor.get('score', 0)}/10]

**Найдено:**
{format_findings(findings)}

**Рекомендации:**
{format_fixes(fixes)}
"""

    # ===== SCANNABILITY =====
    ss_blocks = ss_data.get("blocks", {})
    ss_table_rows = ""
    block_weights = {"h1": 20, "subheadline": 15, "cta": 20, "structure": 15, "visuals": 15, "whitespace": 15}
    block_labels = {"h1": "H1 (Заголовок)", "subheadline": "Subheadline", "cta": "CTA кнопка",
                    "structure": "Структура H2-H3", "visuals": "Визуал", "whitespace": "Пробелы/воздух"}

    for key, weight in block_weights.items():
        block = ss_blocks.get(key, {})
        score = block.get("score", 0)
        ss_table_rows += f"| {block_labels.get(key, key)} | {weight}% | {score}/10 | {get_score_label(score, 10)} |\n"

    ss_table = f"""| Блок | Вес | Оценка | Уровень |
|------|-----|--------|---------|
{ss_table_rows}"""

    ss_details = ""
    for key, label in block_labels.items():
        block = ss_blocks.get(key, {})
        findings = block.get("findings", [])
        fixes = block.get("fixes", [])
        ss_details += f"""
##### {label} [{block.get('score', 0)}/10]

**Найдено:**
{format_findings(findings)}

**Рекомендации:**
{format_fixes(fixes)}
"""

    # ===== TRUST =====
    triggers = trust_data.get("triggers", [])
    missing = trust_data.get("missing", [])
    tf_findings = trust_data.get("findings", [])
    tf_fixes = trust_data.get("fixes", [])

    trigger_labels = {
        "client_reviews": "Отзывы клиентов", "client_results": "Результаты клиентов",
        "video_reviews": "Видео-отзывы", "case_studies": "Кейсы до/после",
        "client_logos": "Логотипы клиентов", "third_party_ratings": "Рейтинги",
        "guarantee": "Гарантия", "certificates": "Сертификаты",
        "company_stats": "Статистика компании", "return_policy": "Политика возврата",
        "social_media": "Соцсети", "contacts": "Контакты", "supplier_badges": "Supplier badges"
    }

    tf_table_rows = ""
    for t in triggers:
        t_type = t.get("type", "")
        count = t.get("count", 1)
        weight = t.get("weight", 0.3)
        score = t.get("score", 0)
        label = trigger_labels.get(t_type, t_type)
        tf_table_rows += f"| {label} | {count} шт | ×{weight} | {score} |\n"

    tf_table = f"""| Тип триггера | Количество | Вес | Балл |
|--------------|------------|-----|------|
{tf_table_rows}| **ИТОГО** | | | **{tf}** |
"""

    missing_str = ", ".join([trigger_labels.get(m, m) for m in missing]) if missing else "—"

    # ===== RESONANCE =====
    pains = resonance_data.get("pains", [])
    rr_findings = resonance_data.get("findings", [])
    rr_fixes = resonance_data.get("fixes", [])

    rr_table_rows = ""
    for p in pains:
        pain = p.get("pain", "")
        score = p.get("score", 0)
        evidence = p.get("evidence", "")
        rr_table_rows += f"| {pain} | {score}% | {evidence} |\n"

    rr_table = f"""| Боль ICP | Закрыто | Доказательство |
|----------|---------|----------------|
{rr_table_rows}"""

    # ===== MOBILE =====
    mobile_cta = mobile_data.get("cta_accessible", "—")
    mobile_text = mobile_data.get("text_readable", "—")
    mobile_rec = mobile_data.get("recommendation", "—")
    mobile_findings = mobile_data.get("findings", [])
    mobile_fixes = mobile_data.get("fixes", [])

    mobile_section = f"""| Параметр | Статус |
|----------|--------|
| CTA доступен (thumb zone) | {mobile_cta} |
| Текст читаемый (16px+) | {mobile_text} |

**Рекомендация:** {mobile_rec}

**Найдено:**
{format_findings(mobile_findings)}

**Рекомендации:**
{format_fixes(mobile_fixes)}
"""

    # ===== A/B TESTS =====
    ab_md = ""
    for i, test in enumerate(ab_tests[:10], 1):
        hypothesis = test.get("hypothesis", "")
        metric = test.get("metric", "")
        variant_a = test.get("variant_a", "")
        variant_b = test.get("variant_b", "")
        ab_md += f"""
**{i}. {hypothesis}**

- **Метрика:** {metric}
- **A (текущий):** `{variant_a}`
- **B (рекомендуемый):** `{variant_b}`
"""

    if not ab_md:
        ab_md = "— A/B тесты не сгенерированы."

    # ===== ALL FIXES =====
    quick_wins = [f for f in all_fixes if f.get("priority", "").upper() in ("HIGH", "CRITICAL")]
    medium_term = [f for f in all_fixes if f.get("priority", "").upper() == "MEDIUM"]
    strategic = [f for f in all_fixes if f.get("priority", "").upper() not in ("HIGH", "CRITICAL", "MEDIUM")]

    def format_all_fixes(fixes_list):
        if not fixes_list:
            return "— Значительных проблем не обнаружено."
        result = ""
        for i, fix in enumerate(fixes_list, 1):
            text = fix.get("text", "")
            impact = fix.get("impact", "")
            priority = fix.get("priority", "MEDIUM")
            source = fix.get("source", "")
            source_label = source.replace("_", " ").replace(".", " → ").title() if source else ""
            priority_emoji = "🔴" if priority == "HIGH" else ("🟡" if priority == "MEDIUM" else "🟢")
            result += f"{i}. {priority_emoji} **{priority}** [{source_label}]: {text}"
            if impact:
                result += f"\n   → {impact}"
            result += "\n"
        return result.rstrip()

    prioritized_section = f"""
### Быстрые победы (эта неделя) — {len(quick_wins)}
{format_all_fixes(quick_wins)}

### Среднесрочные (этот месяц) — {len(medium_term)}
{format_all_fixes(medium_term)}

### Стратегические (этот квартал) — {len(strategic)}
{format_all_fixes(strategic)}
"""

    # ===== ASSEMBLE =====
    md = f"""# CRO-анализ посадочной страницы

**URL:** [{url}]({url})
**Дата:** {date_str}
**Целевая аудитория:** {icp_description}

---

## Метрики

{metrics_table}

---

## 01. CRO Score (MECLABS): {cro_score}%

### Формула

```
C = M×4 + V×3 + I×2 + F×2 + A×2
{meclabs_formula}
```

### Таблица факторов

{meclabs_table}

### Детализация по факторам

{meclabs_details}

---

## 02. LIFT Score: {lift_score}%

### Формула

```
LIFT_raw = ({lift_relevance}+{lift_clarity}+{lift_urgency}+{lift_value}) - ({lift_anxiety}+{lift_distraction}) = {lift_raw}
LIFT = (({lift_raw} + 16) / 54) × 100 = {lift_score}%
```

### Таблица факторов

{lift_table}

### Детализация по факторам

{lift_details}

---

## 03. Scannability Score: {ss}%

### Формула

```
SS = Σ(оценка_блока × вес_блока) × 100% = {ss}%
```

### Таблица блоков

{ss_table}

### Детализация по блокам

{ss_details}

---

## 04. Trust Factor: {tf}

### Таблица триггеров

{tf_table}

**Отсутствуют:** {missing_str}

### Находки и рекомендации

{format_findings(tf_findings)}

{format_fixes(tf_fixes)}

---

## 05. Resonance Rate: {rr}%

### Таблица болей

{rr_table}

### Находки и рекомендации

{format_findings(rr_findings)}

{format_fixes(rr_fixes)}

---

## 06. Мобильный аудит

{mobile_section}

---

## 07. A/B Тесты

{ab_md}

---

## 08. Приоритизированные исправления

{prioritized_section}

---

*Отчёт сгенерирован ИИ. ИИ может ошибаться — проверяйте рекомендации перед внедрением.*
"""

    return md


def main():
    url = None
    icp_description = "generic problem-aware audience"
    output_dir = os.environ.get("OPENCODE_WORKING_DIR", os.getcwd())
    json_file = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--json" and i + 1 < len(args):
            json_file = args[i + 1]
            i += 2
        elif arg == "--url" and i + 1 < len(args):
            url = args[i + 1]
            i += 2
        elif arg == "--icp" and i + 1 < len(args):
            icp_description = args[i + 1]
            i += 2
        elif arg == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif not arg.startswith("--") and url is None:
            url = arg
            i += 1
        else:
            i += 1

    if not url and not json_file:
        print("ОШИБКА: Не указан JSON файл с данными анализа.")
        print("")
        print("Использование:")
        print("  py -3 scripts/generate_landing_md.py --json <analysis.json>   # Windows")
        print("  python3 scripts/generate_landing_md.py --json <analysis.json>  # Linux/Mac")
        sys.exit(1)

    if json_file:
        print(f"Чтение JSON из: {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        url = data.get("url", url or "unknown")
        icp_description = data.get("icp", icp_description)
        analysis = data.get("analysis", data)
    else:
        print("ОШИБКА: Скрипт требует JSON файл с данными.")
        sys.exit(1)

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
