#!/usr/bin/env python3
"""
Generate Landing Page CRO Audit HTML Report — AI Marketing Claude Code Skills
Создаёт профессиональный HTML отчёт со стилем open4.dev.

Новая структура (8 секций):
01. CRO (MECLABS) — 5 факторов с 4-блоковыми тултипами
02. LIFT — 6 факторов с 4-блоковыми тултипами
03. SS (Scannability) — 6 блоков с 4-блоковыми тултипами
04. TF (Trust Factor) — триггеры с 4-блоковыми тултипами
05. RR (Resonance Rate) — боли ICP с 4-блоковыми тултипами
06. Мобильный аудит
07. A/B Тесты (site-specific)
08. Приоритизированные исправления (все рекомендации из 01-06)
"""

import sys
import os
import json
from datetime import datetime
from urllib.parse import urlparse


def escape_html(text):
    """Экранирование HTML символов."""
    if not isinstance(text, str):
        text = str(text)
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def truncate(text, length=80):
    """Обрезка текста с добавлением многоточия."""
    if not text:
        return ""
    text = str(text)
    if len(text) > length:
        return text[:length] + "..."
    return text


def get_score_color(score, max_score):
    """Возвращает CSS класс цвета на основе соотношения баллов."""
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    if percentage >= 70:
        return "success"
    elif percentage >= 40:
        return "warning"
    else:
        return "danger"


def get_score_label(score, max_score):
    """Метка: высокий/средний/низкий."""
    if max_score == 0:
        return "низкий"
    ratio = score / max_score
    if ratio >= 0.7:
        return "высокий"
    elif ratio >= 0.4:
        return "средний"
    else:
        return "низкий"


def get_status_label_percent(score):
    """Метка для процентов."""
    if score >= 70:
        return "ВЫСОКИЙ"
    elif score >= 40:
        return "СРЕДНИЙ"
    else:
        return "НИЗКИЙ"


def get_status_label_tf(score):
    """Метка для TF."""
    if score >= 8:
        return "СИЛЬНОЕ"
    elif score >= 5:
        return "ЕСТЬ БАЗА"
    elif score >= 2:
        return "НЕДОСТАТОЧНО"
    else:
        return "КРИТИЧНО"


def get_timestamp_filename(url, prefix="LANDING-CRO"):
    """Генерация имени файла с timestamp."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"{prefix}-{domain}-{timestamp}"


def generate_metrics_section(metrics):
    """Генерация секции с 5 метриками + tooltips."""
    cro_score = metrics.get("cro_score", 0)
    lift_score = metrics.get("lift_score", 0)
    ss = metrics.get("scannability_score", 0)
    tf = metrics.get("trust_factor", 0)
    rr = metrics.get("resonance_rate", 0)

    tooltips = {
        "cro": {
            "title": "CRO Score (MECLABS) — Общий коэффициент конверсии",
            "desc": "Оценка эффективности посадочной страницы по формуле MECLABS: C = M×4 + V×3 + I×2 + F×2 + A×2. Оценивает мотивацию, ценностное предложение, стимулы, трение и тревогу пользователя.",
            "formula": "C = M×4 + V×3 + I×2 + F×2 + A×2",
            "range": "0-100%: <40% низкий, 40-70% средний, >70% высокий"
        },
        "lift": {
            "title": "LIFT Score — Конверсионный потенциал",
            "desc": "Фреймворк конверсии Conversion.com. 4 драйвера (Релевантность, Ясность, Срочность, Ценность) минус 2 ингибитора (Тревога, Отвлечение). Нормализованная формула: LIFT = ((LIFT_raw + 16) / 54) × 100.",
            "formula": "LIFT = ((R+C+U+V) - (A+D) + 16) / 54 × 100",
            "range": "0-100%: <40% низкий, 40-70% средний, >70% высокий"
        },
        "ss": {
            "title": "SS — Индекс сканируемости",
            "desc": "Процент контента, который пользователь способен воспринять за 5 секунд просмотра. 6 блоков: H1 (20%), Subheadline (15%), CTA (20%), Структура (15%), Визуал (15%), Пробелы (15%).",
            "formula": "SS = Σ(оценка_блока × вес_блока) × 100%",
            "range": "0-100%: <50% плохая, 50-70% средняя, >70% хорошая"
        },
        "tf": {
            "title": "TF — Фактор доверия",
            "desc": "Взвешенная сумма триггеров доверия на странице. 13 типов: от отзывов клиентов (2.0) до supplier badges (0.3). Каждый триггер снижает тревогу пользователя.",
            "formula": "TF = Σ (присутствующий_тип × вес)",
            "range": "0-N: <1.5 критично, 2-4.5 недостаточно, 5-7.5 есть база, 8+ сильное"
        },
        "rr": {
            "title": "RR — Коэффициент резонанса",
            "desc": "Процент болей целевой аудитории (ICP), которые закрыты решениями на странице. Универсальные боли + типовые по бизнесу. Оценка каждой боли: 0/25/50/75/100%.",
            "formula": "RR = (Σ оценка_боли / количество_болей) × 100%",
            "range": "0-100%: <30% слабое, 30-60% среднее, >60% сильное"
        }
    }

    cards_html = ""
    cards_data = [
        ("cro", "CRO (MECLABS)", f"{cro_score}%", "cro"),
        ("lift", "LIFT", f"{lift_score}%", "lift"),
        ("ss", "SS", f"{ss}%", "ss"),
        ("tf", "TF", f"{tf}", "tf"),
        ("rr", "RR", f"{rr}%", "rr"),
    ]

    for key, label, value, metric_key in cards_data:
        tt = tooltips[key]
        cards_html += f"""
                        <div class="score-card {key}">
                            <div class="score-card-tooltip">
                                <div class="tooltip-title">{tt['title']}</div>
                                <div class="tooltip-desc">{tt['desc']}</div>
                                <div class="tooltip-formula"><i class="fa-solid fa-function"></i> {tt['formula']}</div>
                                <div class="tooltip-range"><i class="fa-solid fa-ruler"></i> {tt['range']}</div>
                            </div>
                            <div class="score-card-label">{label}</div>
                            <div class="score-card-value">{value}</div>
                        </div>
        """

    return cards_html


def generate_4block_tooltip(generic_what, generic_how, findings, fixes):
    """Генерация 4-блокового тултипа: Что это, Что делать, Найдено, Рекомендации."""
    findings_html = ""
    if findings:
        findings_items = ""
        for f in findings[:8]:
            if isinstance(f, dict):
                text = f.get("text", str(f))
                findings_items += f'<div class="finding-item">{escape_html(text)}</div>'
            else:
                findings_items += f'<div class="finding-item">{escape_html(str(f))}</div>'
        findings_html = f'<div class="tooltip-specific"><div class="tooltip-specific-title"><i class="fa-solid fa-magnifying-glass"></i> Найдено на сайте:</div>{findings_items}</div>'
    else:
        findings_html = '<div class="tooltip-specific"><div class="tooltip-specific-title"><i class="fa-solid fa-magnifying-glass"></i> Найдено на сайте:</div><div class="finding-item">Данные не получены</div></div>'

    fixes_html = ""
    if fixes:
        fixes_items = ""
        for fix in fixes[:5]:
            if isinstance(fix, dict):
                priority = fix.get("priority", "MEDIUM")
                text = fix.get("text", "")
                impact = fix.get("impact", "")
                p_class = "high" if priority == "HIGH" else ("medium" if priority == "MEDIUM" else "low")
                p_emoji = "🔴" if priority == "HIGH" else ("🟡" if priority == "MEDIUM" else "🟢")
                fixes_items += f'<div class="fix-item-tooltip"><span class="fix-priority-dot {p_class}">{p_emoji} {priority}</span><span class="fix-text-tooltip">{escape_html(text)}</span>'
                if impact:
                    fixes_items += f'<span class="fix-impact-tooltip">{escape_html(impact)}</span>'
                fixes_items += '</div>'
        fixes_html = f'<div class="tooltip-specific"><div class="tooltip-specific-title"><i class="fa-solid fa-wand-magic-sparkles"></i> Рекомендации:</div>{fixes_items}</div>'
    else:
        fixes_html = '<div class="tooltip-specific"><div class="tooltip-specific-title"><i class="fa-solid fa-wand-magic-sparkles"></i> Рекомендации:</div><div class="finding-item">Рекомендации не требуются</div></div>'

    return f"""
                            <div class="meaning-content four-block">
                                <div class="meaning-section"><i class="fa-solid fa-lightbulb"></i> <strong>Что это:</strong> {generic_what}</div>
                                <div class="meaning-section"><i class="fa-solid fa-wand-magic-sparkles"></i> <strong>Что делать:</strong> {generic_how}</div>
                                <div class="meaning-divider"></div>
                                {findings_html}
                                {fixes_html}
                            </div>
    """


def generate_meclabs_section(metrics, cro_data):
    """Генерация секции MECLABS с 4-блоковыми тултипами."""
    motivation = metrics.get("motivation", 0)
    value_prop = metrics.get("value_proposition", 0)
    incentive = metrics.get("incentive", 0)
    friction = metrics.get("friction", 0)
    anxiety = metrics.get("anxiety", 0)
    cro_score = metrics.get("cro_score", 0)

    formula = f"{motivation}×4 + {value_prop}×3 + {incentive}×2 + {friction}×2 + {anxiety}×2 = {cro_score}%"

    factors = cro_data.get("factors", {})

    meclabs_items = [
        ("M", "Мотивация", motivation,
         "Внутренняя мотивация пользователя — насколько человек хочет решить свою проблему. Внешний фактор, независящий от страницы.",
         "Исследуйте свою аудиторию. Мотивация не создаётся страницей — она уже существует. Задача: усилить восприятие проблемы.",
         factors.get("motivation", {})),
        ("V", "Ценностное предложение", value_prop,
         "Сила обещания продукта. Оценивается по 4 векторам: Appeal, Exclusivity, Credibility, Clarity.",
         "Чётко ответьте: 'Что получу я и почему это лучше, чем у конкурентов?' Избегайте generic-фраз.",
         factors.get("value_proposition", {})),
        ("I", "Стимулы", incentive,
         "Дополнительные триггеры: бонусы, скидки, urgency-элементы. Снижают порог принятия решения.",
         "Добавьте конкретный стимул: 'Первый месяц бесплатно', 'Осталось 3 места', 'Скидка 20% только сегодня'.",
         factors.get("incentive", {})),
        ("F", "Трение", friction,
         "Всё, что усложняет действие: сложные формы, много полей, непонятный процесс. Чем меньше трения — тем выше конверсия.",
         "Упростите: максимум 3-5 полей в форме, placeholder-тексты, прогресс-бар для многошаговых форм.",
         factors.get("friction", {})),
        ("A", "Тревога", anxiety,
         "Страх совершить ошибку: 'А если не сработает?', 'Мои данные в безопасности?'. Каждый вопрос = потенциальный отказ.",
         "Разместите рядом с CTA: гарантии, отзывы, сертификаты безопасности, политика возврата.",
         factors.get("anxiety", {}))
    ]

    rows = ""
    for code, name, score, meaning, action, factor_data in meclabs_items:
        color_class = get_score_color(score, 10)
        label = get_score_label(score, 10)
        findings = factor_data.get("findings", [])
        fixes = factor_data.get("fixes", [])
        tooltip = generate_4block_tooltip(meaning, action, findings, fixes)

        rows += f"""
                                        <tr>
                                            <td><strong>{code}</strong></td>
                                            <td><strong>{name}</strong></td>
                                            <td class="score-cell {color_class}">{score}/10</td>
                                            <td><span class="score-label {color_class}">{label}</span></td>
                                            <td><button class="meaning-toggle" onclick="toggleMeaning(this)"><i class="fa-solid fa-circle-info"></i></button></td>
                                        </tr>
                                        <tr class="meaning-row">
                                            <td colspan="5">
                                                {tooltip}
                                            </td>
                                        </tr>
        """

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-flask"></i> Научная основа: формула MECLABS</div>
        <div class="explanation-text">
            <p>Формула разработана в институте <strong>MECLABS</strong> (США) после 15+ лет исследований и A/B тестов.
            Каждый фактор имеет вес, определённый эмпирически:</p>
            <ul>
                <li><strong>M×4</strong> — Мотивация имеет наибольший вес. Без мотивации никакой дизайн не сработает.</li>
                <li><strong>V×3</strong> — Ценностное предложение — ядро коммуникации. Должно быть уникальным и конкретным.</li>
                <li><strong>I×2</strong> — Стимулы дают дополнительный толчок, но не заменяют слабое предложение.</li>
                <li><strong>F×2</strong> — Трение снижает конверсию. Каждое лишнее действие = потерянный клиент.</li>
                <li><strong>A×2</strong> — Тревога убивает конверсию. Особенно на этапе принятия решения.</li>
            </ul>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="meclabs-formula">
                                <h4><i class="fa-solid fa-calculator"></i> Формула конверсии</h4>
                                <code class="formula-code">{formula}</code>
                            </div>
                            <div class="table-scroll-wrapper">
                                <table class="check-table meclabs-table">
                                    <thead>
                                        <tr>
                                            <th>Код</th>
                                            <th>Фактор</th>
                                            <th>Оценка</th>
                                            <th>Уровень</th>
                                            <th>Детали</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>
    """


def generate_lift_section(metrics, lift_data):
    """Генерация секции LIFT с 4-блоковыми тултипами."""
    lift_relevance = metrics.get("lift_relevance", 0)
    lift_clarity = metrics.get("lift_clarity", 0)
    lift_urgency = metrics.get("lift_urgency", 0)
    lift_value = metrics.get("lift_value", 0)
    lift_anxiety = metrics.get("lift_anxiety", 0)
    lift_distraction = metrics.get("lift_distraction", 0)
    lift_score = metrics.get("lift_score", 0)

    drivers = lift_relevance + lift_clarity + lift_urgency + lift_value
    inhibitors = lift_anxiety + lift_distraction
    lift_raw = drivers - inhibitors

    factors = lift_data.get("factors", {})

    lift_items = [
        ("01", "Релевантность", lift_relevance, "Драйвер",
         "Насколько заголовок и первые строки соответствуют ожиданиям аудитории.",
         "Заголовок должен отвечать на вопрос 'Это для меня?' в первые 2 секунды.",
         factors.get("relevance", {})),
        ("02", "Ясность", lift_clarity, "Драйвер",
         "Простота языка, отсутствие жаргона, чёткость CTA.",
         "Используйте слова из словаря клиента, а не продукта. Технические термины = барьер.",
         factors.get("clarity", {})),
        ("03", "Срочность", lift_urgency, "Драйвер",
         "Временные ограничения или дефицит. Мотивирует действовать сейчас.",
         "Добавьте: countdown-таймер, 'Осталось X мест', 'Акция до конца недели'.",
         factors.get("urgency", {})),
        ("04", "Ценность", lift_value, "Базис",
         "Соотношение выгод и затрат. 'Что я получу vs сколько стоит/делаю'.",
         "Всегда рядом с ценой показывайте выгоду. '199$/мес — экономия 4 часов/день' = выгодно.",
         factors.get("value", {})),
        ("05", "Тревога", lift_anxiety, "Ингибитор",
         "Отсутствие доверительных сигналов. Каждый вопрос = сомнение = отказ.",
         "Тревога максимальна рядом с CTA. Добавьте: гарантии, отзывы, сертификаты.",
         factors.get("anxiety", {})),
        ("06", "Отвлечение", lift_distraction, "Ингибитор",
         "Лишние ссылки, всплывающие окна, навигация, конкурирующая с CTA.",
         "Уберите всё, что не помогает конвертировать. Оставьте только 'выход'.",
         factors.get("distraction", {}))
    ]

    rows = ""
    for num, name, score, role, meaning, action, factor_data in lift_items:
        color_class = get_score_color(score, 10)
        role_class = "driver" if role == "Драйвер" else ("inhibitor" if role == "Ингибитор" else "")
        findings = factor_data.get("findings", [])
        fixes = factor_data.get("fixes", [])
        tooltip = generate_4block_tooltip(meaning, action, findings, fixes)

        rows += f"""
                                        <tr>
                                            <td><strong>{num}</strong></td>
                                            <td><strong>{name}</strong></td>
                                            <td class="score-cell {color_class}">{score}/10</td>
                                            <td><span class="role-badge {role_class}">{role}</span></td>
                                            <td><button class="meaning-toggle" onclick="toggleMeaning(this)"><i class="fa-solid fa-circle-info"></i></button></td>
                                        </tr>
                                        <tr class="meaning-row">
                                            <td colspan="5">
                                                {tooltip}
                                            </td>
                                        </tr>
        """

    explanation = f"""
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-chart-simple"></i> LIFT Framework — модель конверсии Conversion.com</div>
        <div class="explanation-text">
            <p><strong>LIFT</strong> выделяет 6 факторов, влияющих на решение о конверсии:</p>
            <ul>
                <li><strong>4 драйвера</strong> (повышают): Релевантность, Ясность, Срочность, Ценность</li>
                <li><strong>2 ингибитора</strong> (снижают): Тревога, Отвлечение</li>
            </ul>
            <p>Формула: <strong>LIFT_raw = ({lift_relevance}+{lift_clarity}+{lift_urgency}+{lift_value}) - ({lift_anxiety}+{lift_distraction}) = {lift_raw}</strong></p>
            <p>Нормализация: <strong>LIFT = (({lift_raw} + 16) / 54) × 100 = {lift_score}%</strong></p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="table-scroll-wrapper">
                                <table class="check-table lift-table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Фактор</th>
                                            <th>Оценка</th>
                                            <th>Роль</th>
                                            <th>Детали</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>
    """


def generate_scannability_section(metrics, ss_data):
    """Генерация секции SS (Scannability) с 4-блоковыми тултипами."""
    ss = metrics.get("scannability_score", 0)
    blocks = ss_data.get("blocks", {})

    block_defs = [
        ("01", "H1 (Заголовок)", "h1", 20,
         "Главный заголовок страницы. Первое, что видит пользователь. Должен быть до 10 слов, содержать выгоду, а не функцию.",
         "Сократите до 6-8 слов. Используйте выгоду: 'Тёплые окна за 5 дней' вместо 'Производство окон'.",
         blocks.get("h1", {})),
        ("02", "Subheadline (Подзаголовок)", "subheadline", 15,
         "Раскрывает headline с конкретикой. 1-2 предложения, ценность должна быть ясна.",
         "Добавьте конкретные цифры: '15 лет на рынке, 5000+ установленных окон'.",
         blocks.get("subheadline", {})),
        ("03", "CTA кнопка", "cta", 20,
         "Кнопка призыва к действию. Должна быть контрастной, видимой, с текстом выгоды (не действия).",
         "Используйте first person: 'Получить мою скидку' вместо 'Отправить'.",
         blocks.get("cta", {})),
        ("04", "Структура H2-H3", "structure", 15,
         "Иерархия заголовков страницы. Должна быть логичной и scannable за 3 секунды.",
         "Каждый H2 — отдельная тема. Используйте нумерованные списки и короткие абзацы.",
         blocks.get("structure", {})),
        ("05", "Визуал", "visuals", 15,
         "Фотографии и иллюстрации. Реальные фото клиентов/результатов работают лучше стоковых.",
         "Замените стоковые фото на реальные: фото установленных окон, довольных клиентов.",
         blocks.get("visuals", {})),
        ("06", "Пробелы/воздух", "whitespace", 15,
         "Пространство между элементами. Чистый дизайн улучшает читаемость и восприятие.",
         "Увеличьте отступы между секциями. Не перегружайте страницу текстом.",
         blocks.get("whitespace", {}))
    ]

    rows = ""
    for num, name, key, weight, meaning, action, block_data in block_defs:
        score = block_data.get("score", 0)
        color_class = get_score_color(score, 10)
        label = get_score_label(score, 10)
        findings = block_data.get("findings", [])
        fixes = block_data.get("fixes", [])
        tooltip = generate_4block_tooltip(meaning, action, findings, fixes)

        rows += f"""
                                        <tr>
                                            <td><strong>{num}</strong></td>
                                            <td><strong>{name}</strong></td>
                                            <td><strong>{weight}%</strong></td>
                                            <td class="score-cell {color_class}">{score}/10</td>
                                            <td><span class="score-label {color_class}">{label}</span></td>
                                            <td><button class="meaning-toggle" onclick="toggleMeaning(this)"><i class="fa-solid fa-circle-info"></i></button></td>
                                        </tr>
                                        <tr class="meaning-row">
                                            <td colspan="6">
                                                {tooltip}
                                            </td>
                                        </tr>
        """

    explanation = f"""
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-eye"></i> Scannability Score — индекс сканируемости</div>
        <div class="explanation-text">
            <p><strong>SS</strong> — процент контента, который пользователь способен воспринять за 5 секунд просмотра.
            Зависит от структуры, заголовков, визуальной иерархии и плотности текста.</p>
            <p>Формула: <strong>SS = Σ(оценка_блока × вес_блока) × 100% = {ss}%</strong></p>
            <p>6 блоков с весами: H1 (20%), Subheadline (15%), CTA (20%), Структура (15%), Визуал (15%), Пробелы (15%).</p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="table-scroll-wrapper">
                                <table class="check-table ss-table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Блок</th>
                                            <th>Вес</th>
                                            <th>Оценка</th>
                                            <th>Уровень</th>
                                            <th>Детали</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>
    """


def generate_trust_section(metrics, trust_data):
    """Генерация секции TF (Trust Factor) с 4-блоковыми тултипами."""
    tf = metrics.get("trust_factor", 0)
    triggers = trust_data.get("triggers", [])
    missing = trust_data.get("missing", [])
    findings = trust_data.get("findings", [])
    fixes = trust_data.get("fixes", [])

    trigger_labels = {
        "client_reviews": "Отзывы клиентов",
        "client_results": "Результаты клиентов",
        "video_reviews": "Видео-отзывы",
        "case_studies": "Кейсы до/после",
        "client_logos": "Логотипы клиентов",
        "third_party_ratings": "Рейтинги第三方",
        "guarantee": "Гарантия",
        "certificates": "Сертификаты",
        "company_stats": "Статистика компании",
        "return_policy": "Политика возврата",
        "social_media": "Соцсети",
        "contacts": "Контакты",
        "supplier_badges": "Supplier badges"
    }

    trigger_weights = {
        "client_reviews": 2.0, "client_results": 2.0, "video_reviews": 2.0,
        "case_studies": 1.5, "client_logos": 1.5, "third_party_ratings": 1.5,
        "guarantee": 1.5, "certificates": 1.0, "company_stats": 1.0,
        "return_policy": 1.0, "social_media": 0.5, "contacts": 0.5,
        "supplier_badges": 0.3
    }

    rows = ""
    for trig in triggers:
        t_type = trig.get("type", "")
        count = trig.get("count", 1)
        weight = trig.get("weight", 0.3)
        score = trig.get("score", 0)
        label = trigger_labels.get(t_type, t_type)
        color_class = get_score_color(score * 10, 20) if weight >= 1.5 else "warning"
        rows += f"""
                                        <tr>
                                            <td><strong>{label}</strong></td>
                                            <td>{count} шт</td>
                                            <td>×{weight}</td>
                                            <td class="score-cell {color_class}">{score}</td>
                                        </tr>
        """

    missing_html = ""
    if missing:
        missing_items = ""
        for m in missing:
            label = trigger_labels.get(m, m)
            w = trigger_weights.get(m, 0.5)
            missing_items += f'<div class="missing-item"><span class="missing-name">{escape_html(label)}</span><span class="missing-weight">вес: {w}</span></div>'
        missing_html = f'<div class="missing-triggers"><h4><i class="fa-solid fa-triangle-exclamation"></i> Отсутствуют (добавьте для роста TF):</h4>{missing_items}</div>'

    tooltip = generate_4block_tooltip(
        "Взвешенная сумма триггеров доверия на странице. 13 типов от 0.3 до 2.0. Каждый триггер снижает тревогу пользователя.",
        "Добавьте отзывы клиентов, гарантию рядом с CTA, рейтинги第三方, кейсы до/после.",
        findings, fixes
    )

    explanation = f"""
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-shield-halved"></i> Trust Factor — фактор доверия</div>
        <div class="explanation-text">
            <p><strong>TF</strong> — взвешенная сумма триггеров доверия. 13 типов с разными весами:</p>
            <ul>
                <li><strong>2.0</strong> — Отзывы клиентов, Результаты клиентов, Видео-отзывы</li>
                <li><strong>1.5</strong> — Кейсы до/после, Логотипы клиентов, Рейтинги, Гарантия</li>
                <li><strong>1.0</strong> — Сертификаты, Статистика компании, Политика возврата</li>
                <li><strong>0.5</strong> — Соцсети, Контакты</li>
                <li><strong>0.3</strong> — Supplier badges</li>
            </ul>
            <p>Формула: <strong>TF = Σ (тип × вес) = {tf}</strong></p>
            <p>Статус: <strong>{get_status_label_tf(tf)}</strong></p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="table-scroll-wrapper">
                                <table class="check-table trust-table">
                                    <thead>
                                        <tr>
                                            <th>Тип триггера</th>
                                            <th>Количество</th>
                                            <th>Вес</th>
                                            <th>Балл</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>
                            {missing_html}
                            <div class="meaning-content four-block" style="margin-top: 20px;">
                                {tooltip}
                            </div>
    """


def generate_resonance_section(metrics, resonance_data, icp_description):
    """Генерация секции RR (Resonance Rate) с 4-блоковыми тултипами."""
    rr = metrics.get("resonance_rate", 0)
    pains = resonance_data.get("pains", [])
    findings = resonance_data.get("findings", [])
    fixes = resonance_data.get("fixes", [])

    rows = ""
    for pain_data in pains:
        pain = pain_data.get("pain", "")
        score = pain_data.get("score", 0)
        evidence = pain_data.get("evidence", "")
        color_class = get_score_color(score, 100)
        rows += f"""
                                        <tr>
                                            <td><strong>{escape_html(pain)}</strong></td>
                                            <td class="score-cell {color_class}">{score}%</td>
                                            <td>{escape_html(evidence)}</td>
                                        </tr>
        """

    tooltip = generate_4block_tooltip(
        f"Процент болей ICP ({icp_description}), которые закрыты решениями на странице. Универсальные боли + типовые по бизнесу.",
        "Для каждой незакрытой боли добавьте секцию с решением и доказательством (цифры, отзывы, кейсы).",
        findings, fixes
    )

    explanation = f"""
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-bullseye"></i> Resonance Rate — коэффициент резонанса</div>
        <div class="explanation-text">
            <p><strong>RR</strong> — процент болей целевой аудитории, закрытых решениями на странице.</p>
            <p>Алгоритм: 1) Определить тип бизнеса → 2) Взять универсальные + типовые боли → 3) Оценить каждую (0/25/50/75/100%) → 4) Среднее</p>
            <p>Формула: <strong>RR = (Σ оценка_боли / количество_болей) × 100% = {rr}%</strong></p>
            <p>Статус: <strong>{get_status_label_percent(rr)}</strong></p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="table-scroll-wrapper">
                                <table class="check-table resonance-table">
                                    <thead>
                                        <tr>
                                            <th>Боль ICP</th>
                                            <th>Закрыто</th>
                                            <th>Доказательство</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>
                            <div class="meaning-content four-block" style="margin-top: 20px;">
                                {tooltip}
                            </div>
    """


def generate_mobile_audit(mobile_data):
    """Генерация секции мобильного аудита."""
    cta = mobile_data.get("cta_accessible", "—")
    text = mobile_data.get("text_readable", "—")
    recommendation = mobile_data.get("recommendation", "—")
    findings = mobile_data.get("findings", [])
    fixes = mobile_data.get("fixes", [])

    findings_html = ""
    if findings:
        for f in findings:
            if isinstance(f, dict):
                findings_html += f'<li>{escape_html(f.get("text", str(f)))}</li>'
            else:
                findings_html += f'<li>{escape_html(str(f))}</li>'

    fixes_html = ""
    if fixes:
        for fix in fixes:
            if isinstance(fix, dict):
                priority = fix.get("priority", "MEDIUM")
                text_fix = fix.get("text", "")
                impact = fix.get("impact", "")
                p_class = priority.lower()
                fixes_html += f'''
                                <div class="fix-item priority-{p_class}">
                                    <span class="fix-priority">{priority}</span>
                                    <span class="fix-text">{escape_html(text_fix)}</span>
                                    <span class="fix-impact">{escape_html(impact)}</span>
                                </div>
                '''

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-mobile-screen"></i> Мобильный аудит</div>
        <div class="explanation-text">
            <p>Более 60% трафика — мобильные устройства. Страница должна быть оптимизирована:</p>
            <ul>
                <li><strong>CTA в thumb-zone</strong> — кнопка в нижней половине экрана</li>
                <li><strong>Текст ≥16px</strong> — читаемость без зума</li>
                <li><strong>Формы для tap</strong> — поля достаточно большие для пальца</li>
                <li><strong>Без горизонтального скролла</strong></li>
                <li><strong>Sticky CTA</strong> — кнопка видна при скролле</li>
            </ul>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="form-audit-grid">
                                <div class="form-audit-item">
                                    <div class="form-audit-label">CTA доступен (thumb zone)</div>
                                    <div class="form-audit-value">{cta}</div>
                                </div>
                                <div class="form-audit-item">
                                    <div class="form-audit-label">Текст читаемый (16px+)</div>
                                    <div class="form-audit-value">{text}</div>
                                </div>
                            </div>
                            <div class="form-recommendation">
                                <h4><i class="fa-solid fa-clipboard-list"></i> Рекомендация</h4>
                                <p>{escape_html(recommendation)}</p>
                            </div>
                            {f'<h4 class="subsection-title"><i class="fa-solid fa-magnifying-glass"></i> Что найдено</h4><ul class="findings-list">{findings_html}</ul>' if findings_html else ''}
                            {f'<h4 class="subsection-title"><i class="fa-solid fa-wand-magic-sparkles"></i> Что делать</h4><div class="fixes-list">{fixes_html}</div>' if fixes_html else ''}
    """


def generate_ab_tests(ab_tests):
    """Генерация секции A/B тестов с site-specific данными."""
    if not ab_tests:
        return '<p class="no-data">— A/B тесты не сгенерированы. Для точного определения влияния изменений необходимо тестирование.</p>'

    tests_html = ""
    for i, test in enumerate(ab_tests[:10], 1):
        hypothesis = test.get("hypothesis", "")
        metric = test.get("metric", "")
        variant_a = test.get("variant_a", "")
        variant_b = test.get("variant_b", "")

        tests_html += f"""
                                <div class="ab-test-item">
                                    <div class="ab-test-number">{i}</div>
                                    <div class="ab-test-content">
                                        <div class="ab-test-hypothesis">{escape_html(hypothesis)}</div>
                                        {f'<div class="ab-test-metric"><i class="fa-solid fa-chart-line"></i> Метрика: {escape_html(metric)}</div>' if metric else ''}
                                        <div class="ab-variants">
                                            <div class="ab-variant variant-a">
                                                <span class="ab-variant-label">A (текущий):</span>
                                                <code>{escape_html(variant_a)}</code>
                                            </div>
                                            <div class="ab-variant variant-b">
                                                <span class="ab-variant-label">B (рекомендуемый):</span>
                                                <code>{escape_html(variant_b)}</code>
                                            </div>
                                        </div>
                                    </div>
                                </div>
        """

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-flask"></i> A/B тестирование — научный метод оптимизации</div>
        <div class="explanation-text">
            <p>Каждая рекомендация должна быть проверена через <strong>A/B тест</strong>. Принципы:</p>
            <ul>
                <li><strong>Одна переменная</strong> за раз — изменяйте только заголовок ИЛИ только CTA</li>
                <li><strong>Статистическая значимость</strong> — минимум 100 конверсий на вариант</li>
                <li><strong>Минимальный срок</strong> — 2 недели, чтобы исключить day-of-week эффект</li>
                <li><strong>Сегментация</strong> — одна кнопка может работать по-разному для разных сегментов</li>
            </ul>
            <p><strong>Формула значимости:</strong> p-value &lt; 0.05 (95% доверительный интервал)</p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="ab-tests-list">
                                {tests_html}
                            </div>
    """


def generate_fixes_section(all_fixes):
    """Генерация секции приоритизированных фиксов."""
    quick_wins = [f for f in all_fixes if f.get("priority", "").upper() in ("HIGH", "CRITICAL")]
    medium_term = [f for f in all_fixes if f.get("priority", "").upper() == "MEDIUM"]
    strategic = [f for f in all_fixes if f.get("priority", "").upper() not in ("HIGH", "CRITICAL", "MEDIUM")]

    def format_fixes(fixes_list, priority, icon_class, priority_label):
        if not fixes_list:
            return ""
        html = f'<div class="priority-section">'
        html += f'<h4 class="priority-title {priority}"><i class="fa-solid {icon_class}"></i> {priority_label}</h4>'
        html += '<div class="priority-items">'
        for i, fix in enumerate(fixes_list, 1):
            text = fix.get("text", "")
            impact = fix.get("impact", "")
            source = fix.get("source", "")
            source_label = source.replace("_", " ").replace(".", " → ").title() if source else ""
            html += f"""
                                    <div class="priority-item {priority}">
                                        <div class="priority-item-header">
                                            <span class="priority-num">{i}</span>
                                            <h5>{escape_html(text)}</h5>
                                        </div>
                                        {f'<p class="priority-source"><i class="fa-solid fa-tag"></i> {escape_html(source_label)}</p>' if source_label else ''}
                                        <p class="priority-impact"><i class="fa-solid fa-bullseye"></i> {escape_html(impact) if impact else 'Ожидаемый эффект не указан'}</p>
                                    </div>
            """
        html += '</div></div>'
        return html

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-list-check"></i> Приоритизация исправлений — матрица Эйзенхауэра</div>
        <div class="explanation-text">
            <p>Все обнаруженные проблемы распределяются по <strong>3 категориям</strong>:</p>
            <ul>
                <li><strong>Быстрые победы (эта неделя)</strong> — высокое влияние, низкое усилие</li>
                <li><strong>Среднесрочные (этот месяц)</strong> — высокое влияние, высокое усилие</li>
                <li><strong>Стратегические (этот квартал)</strong> — среднее влияние, высокое усилие</li>
            </ul>
            <p><strong>Принцип:</strong> Сосредоточьтесь на быстрых победах — они дают максимальный ROI.</p>
        </div>
    </div>
    """

    fixes_html = explanation
    fixes_html += format_fixes(quick_wins, "high", "fa-bolt", f"Быстрые победы (эта неделя) — {len(quick_wins)}")
    fixes_html += format_fixes(medium_term, "medium", "fa-calendar-week", f"Среднесрочные (этот месяц) — {len(medium_term)}")
    fixes_html += format_fixes(strategic, "low", "fa-chart-line", f"Стратегические (этот квартал) — {len(strategic)}")

    if not quick_wins and not medium_term and not strategic:
        fixes_html += '<p class="no-data">— Значительных проблем не обнаружено. Страница в хорошем состоянии.</p>'

    return fixes_html


def generate_html_report(url, analysis, icp_description):
    """Генерация полного HTML отчёта."""
    metrics = analysis.get("metrics", {})
    cro_data = analysis.get("cro", {})
    lift_data = analysis.get("lift", {})
    ss_data = analysis.get("scannability", {})
    trust_data = analysis.get("trust", {})
    resonance_data = analysis.get("resonance", {})
    mobile_data = analysis.get("mobile_audit", {})
    ab_tests = analysis.get("ab_tests", [])
    all_fixes = analysis.get("all_fixes", [])

    timestamp = datetime.now().strftime("%d %m %Y, %H:%M:%S")
    parsed = urlparse(url)
    domain = parsed.netloc

    metrics_section = generate_metrics_section(metrics)
    meclabs_section = generate_meclabs_section(metrics, cro_data)
    lift_section = generate_lift_section(metrics, lift_data)
    ss_section = generate_scannability_section(metrics, ss_data)
    trust_section = generate_trust_section(metrics, trust_data)
    resonance_section = generate_resonance_section(metrics, resonance_data, icp_description)
    mobile_section = generate_mobile_audit(mobile_data)
    ab_section = generate_ab_tests(ab_tests)
    fixes_section = generate_fixes_section(all_fixes)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CRO-анализ — {escape_html(domain)}</title>
    <meta name="description" content="CRO-анализ посадочной страницы {escape_html(domain)}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {{
            --tp-primary: #1a1a1a;
            --tp-secondary: #666666;
            --tp-accent: #ff6b35;
            --tp-accent-2: #f7b731;
            --tp-white: #ffffff;
            --tp-black: #000000;
            --tp-gray: #f5f5f5;
            --tp-gray-2: #e0e0e0;
            --tp-text: #333333;
            --tp-text-light: #666666;
            --tp-bg: #ffffff;
            --tp-bg-alt: #f9f9f9;
            --tp-transition: all 0.3s ease;
            --tp-radius: 8px;
            --success: #00C853;
            --danger: #FF1744;
            --warning: #FFB300;
        }}

        *, *::before, *::after {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Outfit', 'Poppins', sans-serif;
            font-size: 18px;
            line-height: 1.6;
            color: var(--tp-text);
            background-color: var(--tp-bg);
            overflow-x: hidden;
        }}

        a {{
            text-decoration: none;
            color: inherit;
            transition: var(--tp-transition);
        }}

        ul {{
            list-style: none;
        }}

        img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}

        button {{
            border: none;
            background: none;
            cursor: pointer;
            font-family: inherit;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 0 30px;
        }}

        /* Header */
        .tp-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            padding: 15px 0;
            background-color: var(--tp-white);
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
            transition: var(--tp-transition);
        }}

        .tp-header-inner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
        }}

        .tp-header-logo {{
            flex-shrink: 0;
            z-index: 1002;
        }}

        .tp-header-logo img {{
            width: 120px;
            max-width: 120px;
            height: auto;
        }}

        .tp-main-menu {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }}

        .tp-nav-menu {{
            display: flex;
            gap: 60px;
            align-items: center;
        }}

        .tp-nav-menu .nav-links {{
            position: relative;
            font-weight: 500;
            font-size: 17px;
            color: var(--tp-primary);
            padding: 10px 0;
            text-decoration: none;
            transition: color 0.3s ease;
        }}

        .tp-nav-menu .nav-links::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--tp-accent);
            transform: scaleX(0);
            transform-origin: right;
            transition: transform 0.3s ease;
        }}

        .tp-nav-menu .nav-links:hover {{
            color: var(--tp-accent);
        }}

        .tp-nav-menu .nav-links:hover::after {{
            transform: scaleX(1);
            transform-origin: left;
        }}

        .tp-header-action {{
            display: flex;
            align-items: center;
            gap: 20px;
            flex-shrink: 0;
        }}

        .tp-menu-toggle {{
            width: 40px;
            height: 30px;
            position: relative;
            display: none;
            flex-direction: column;
            justify-content: space-between;
            z-index: 1002;
        }}

        .tp-menu-toggle span {{
            display: block;
            width: 100%;
            height: 2px;
            background-color: var(--tp-primary);
            position: absolute;
            left: 0;
            transition: var(--tp-transition);
        }}

        .tp-menu-toggle span:nth-child(1) {{ top: 0; }}
        .tp-menu-toggle span:nth-child(2) {{ top: 50%; transform: translateY(-50%); }}
        .tp-menu-toggle span:nth-child(3) {{ top: 100%; transform: translateY(-100%); }}

        .tp-menu-toggle::before,
        .tp-menu-toggle::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--tp-primary);
            transform: translateY(-50%) rotate(0deg);
            transition: transform 0.3s ease;
            pointer-events: none;
        }}

        .tp-menu-toggle.active span {{
            opacity: 0;
        }}

        .tp-menu-toggle.active::before {{
            transform: translateY(-50%) rotate(45deg);
        }}

        .tp-menu-toggle.active::after {{
            transform: translateY(-50%) rotate(-45deg);
        }}

        /* Buttons */
        .tp-btn {{
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 14px 30px;
            background-color: var(--tp-primary);
            color: var(--tp-white);
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-radius: var(--tp-radius);
            overflow: hidden;
            transition: var(--tp-transition);
            white-space: nowrap;
        }}

        .tp-btn:hover {{
            background-color: var(--tp-accent);
            color: var(--tp-white);
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
        }}

        .tp-btn-accent {{
            background-color: var(--tp-accent);
        }}

        .tp-btn-accent:hover {{
            background-color: var(--tp-primary);
        }}

        /* Mobile Backdrop */
        .mobile-menu-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }}

        .mobile-menu-backdrop.active {{
            opacity: 1;
            visibility: visible;
        }}

        /* Scoring Explanation */
        .scoring-explanation {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 30px 30px;
        }}

        .scoring-toggle {{
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
            padding: 15px 20px;
            background: var(--tp-bg-alt);
            border: 1px solid var(--tp-gray-2);
            border-radius: var(--tp-radius);
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            color: var(--tp-text);
            transition: var(--tp-transition);
        }}

        .scoring-toggle:hover {{
            background: var(--tp-gray);
        }}

        .scoring-toggle i {{
            transition: transform 0.3s ease;
        }}

        .scoring-toggle.active i {{
            transform: rotate(180deg);
        }}

        .scoring-content {{
            display: none;
            padding: 20px;
            background: var(--tp-white);
            border: 1px solid var(--tp-gray-2);
            border-top: none;
            border-radius: 0 0 var(--tp-radius) var(--tp-radius);
        }}

        .scoring-content.active {{
            display: block;
        }}

        .scoring-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .scoring-block {{
            padding: 15px;
            background: var(--tp-bg);
            border-radius: var(--tp-radius);
        }}

        .scoring-block h4 {{
            margin-bottom: 10px;
            font-size: 15px;
            font-weight: 700;
            color: var(--tp-accent);
        }}

        .scoring-block ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .scoring-block li {{
            padding: 5px 0;
            font-size: 14px;
            color: var(--tp-text);
            border-bottom: 1px solid var(--tp-gray-2);
        }}

        .scoring-block li:last-child {{
            border-bottom: none;
        }}

        /* New scoring explanation */
        .scoring-scale {{
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }}

        .scoring-scale-item {{
            flex: 1;
            min-width: 180px;
            padding: 12px 18px;
            background: var(--tp-bg);
            border-radius: var(--tp-radius);
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 15px;
        }}

        .scoring-scale-item .scale-color {{
            font-size: 18px;
        }}

        .scoring-scale-item.good {{ border-left: 4px solid var(--success); }}
        .scoring-scale-item.warning {{ border-left: 4px solid var(--warning); }}
        .scoring-scale-item.danger {{ border-left: 4px solid var(--danger); }}

        .scoring-order {{
            background: var(--tp-bg);
            padding: 20px;
            border-radius: var(--tp-radius);
            margin-bottom: 25px;
        }}

        .scoring-order h4 {{
            font-size: 16px;
            font-weight: 700;
            color: var(--tp-primary);
            margin-bottom: 12px;
        }}

        .scoring-order ol {{
            padding-left: 20px;
            margin: 0;
        }}

        .scoring-order li {{
            font-size: 15px;
            padding: 6px 0;
            color: var(--tp-text);
            line-height: 1.6;
        }}

        .scoring-order li strong {{
            color: var(--tp-accent);
        }}

        .scoring-info-btn {{
            background: var(--tp-bg);
            padding: 20px;
            border-radius: var(--tp-radius);
        }}

        .scoring-info-btn h4 {{
            font-size: 16px;
            font-weight: 700;
            color: var(--tp-primary);
            margin-bottom: 12px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}

        .info-item {{
            font-size: 15px;
            padding: 10px 14px;
            background: var(--tp-white);
            border-radius: 8px;
        }}

        .info-item strong {{
            color: var(--tp-accent);
        }}

        @media (max-width: 768px) {{
            .scoring-scale {{
                flex-direction: column;
            }}
            .info-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Hero Section */
        .tp-hero {{
            position: relative;
            min-height: 40vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
            overflow: hidden;
            padding: 120px 0 60px;
        }}

        .tp-hero-bg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}

        .tp-hero-shape {{
            position: absolute;
            border-radius: 50%;
            opacity: 0.1;
        }}

        .tp-hero-shape-1 {{
            width: clamp(200px, 50vw, 600px);
            height: clamp(200px, 50vw, 600px);
            background: linear-gradient(135deg, var(--tp-accent), var(--tp-accent-2));
            top: clamp(-50px, -10vw, -200px);
            right: clamp(-20px, -8vw, -100px);
            animation: float 15s ease-in-out infinite;
        }}

        .tp-hero-shape-2 {{
            width: clamp(120px, 35vw, 400px);
            height: clamp(120px, 35vw, 400px);
            background: linear-gradient(135deg, #667eea, #764ba2);
            bottom: clamp(-30px, -8vw, -100px);
            left: clamp(-20px, -8vw, -100px);
            animation: float 12s ease-in-out infinite reverse;
        }}

        .tp-hero-shape-3 {{
            width: clamp(80px, 18vw, 200px);
            height: clamp(80px, 18vw, 200px);
            background: linear-gradient(135deg, var(--tp-accent-2), #ff6b35);
            top: 50%;
            left: 20%;
            animation: float 10s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            33% {{ transform: translate(30px, -30px) rotate(10deg); }}
            66% {{ transform: translate(-20px, 20px) rotate(-5deg); }}
        }}

        .tp-hero-content {{
            position: relative;
            z-index: 10;
            text-align: center;
        }}

        .tp-hero-subtitle {{
            display: inline-block;
            font-size: 16px;
            font-weight: 500;
            color: var(--tp-text);
            margin-bottom: 4px;
        }}

        .tp-hero-title {{
            font-size: clamp(40px, 8vw, 80px);
            font-weight: 800;
            line-height: 1.1;
            color: var(--tp-primary);
            margin-bottom: 20px;
        }}

        .tp-hero-description {{
            font-size: 20px;
            color: var(--tp-text-light);
            margin-bottom: 10px;
            line-height: 1.8;
        }}

        .tp-hero-date {{
            font-size: 16px;
            color: var(--tp-secondary);
        }}

        .icp-badge {{
            display: inline-block;
            margin-top: 15px;
            padding: 8px 20px;
            background-color: var(--tp-bg);
            border-radius: 20px;
            font-size: 15px;
            color: var(--tp-text-light);
        }}

        /* Score Cards */
        .scores-section {{
            padding: 60px 0;
            background-color: var(--tp-bg);
        }}

        .scores-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .score-card {{
            position: relative;
            padding: 30px 20px;
            background-color: var(--tp-white);
            border-radius: var(--tp-radius);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: var(--tp-transition);
        }}

        .score-card:hover {{
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
            z-index: 2;
        }}

        .score-card.cro {{ border-top: 4px solid var(--tp-primary); }}
        .score-card.lift {{ border-top: 4px solid var(--tp-accent); }}
        .score-card.ss {{ border-top: 4px solid #667eea; }}
        .score-card.tf {{ border-top: 4px solid var(--success); }}
        .score-card.rr {{ border-top: 4px solid var(--warning); }}

        .score-card-label {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--tp-text-light);
            margin-bottom: 10px;
        }}

        .score-card-value {{
            font-size: 48px;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 5px;
        }}

        .score-card.cro .score-card-value {{ color: var(--tp-primary); }}
        .score-card.lift .score-card-value {{ color: var(--tp-accent); }}
        .score-card.ss .score-card-value {{ color: #667eea; }}
        .score-card.tf .score-card-value {{ color: var(--success); }}
        .score-card.rr .score-card-value {{ color: var(--warning); }}

        .score-card-max {{
            font-size: 14px;
            color: var(--tp-text-light);
        }}

        /* Score Card Tooltips */
        .score-card-tooltip {{
            display: none;
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            width: 320px;
            background: var(--tp-primary);
            color: var(--tp-white);
            padding: 20px;
            border-radius: var(--tp-radius);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
            z-index: 10001;
            text-align: left;
            margin-top: 15px;
        }}

        .score-card:hover .score-card-tooltip {{
            display: block;
        }}

        .score-card-tooltip::after {{
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 10px solid transparent;
            border-bottom-color: var(--tp-primary);
        }}

        .tooltip-title {{
            font-weight: 700;
            font-size: 15px;
            margin-bottom: 8px;
            color: var(--tp-accent);
        }}

        .tooltip-desc {{
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 10px;
        }}

        .tooltip-formula, .tooltip-range {{
            font-size: 13px;
            color: rgba(255,255,255,0.7);
            margin-bottom: 4px;
        }}

        .tooltip-formula i, .tooltip-range i {{
            margin-right: 5px;
            color: var(--tp-accent);
        }}

        /* Accordion */
        .tp-sections {{
            padding: 80px 0 100px;
            background-color: var(--tp-bg-alt);
        }}

        .services-accordion {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .services-accordion-item {{
            border-bottom: 1px solid var(--tp-gray-2);
            margin-bottom: 0;
        }}

        .services-accordion-item:nth-child(odd) {{
            background-color: var(--tp-bg);
        }}

        .services-accordion-item:nth-child(even) {{
            background-color: var(--tp-bg-alt);
        }}

        .services-accordion-item.active .services-accordion-toggle {{
            background-color: var(--tp-accent);
            color: var(--tp-white);
        }}

        .services-accordion-header {{
            display: flex;
            align-items: center;
            padding: 25px 0;
            cursor: pointer;
            transition: var(--tp-transition);
        }}

        .services-accordion-header:hover {{
            color: var(--tp-accent);
        }}

        .services-accordion-number {{
            font-size: 48px;
            font-weight: 800;
            color: var(--tp-gray-2);
            line-height: 1;
            margin-right: 30px;
            font-family: 'Outfit', sans-serif;
            opacity: 0.7;
            min-width: 70px;
            text-align: left;
        }}

        .services-accordion-title {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .services-accordion-title i {{
            font-size: 24px;
            color: var(--tp-accent);
        }}

        .services-accordion-title h3 {{
            font-size: 22px;
            font-weight: 700;
            color: var(--tp-primary);
            margin: 0;
        }}

        .section-score {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 600;
            margin-right: 15px;
        }}

        .section-score.success {{ background-color: rgba(0, 200, 83, 0.1); color: var(--success); }}
        .section-score.warning {{ background-color: rgba(255, 179, 0, 0.1); color: var(--warning); }}
        .section-score.danger {{ background-color: rgba(255, 23, 68, 0.1); color: var(--danger); }}

        .services-accordion-toggle {{
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: var(--tp-white);
            border-radius: 50%;
            color: var(--tp-primary);
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        .services-accordion-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease;
        }}

        .services-accordion-item.active .services-accordion-content {{
            max-height: 10000px;
        }}

        .services-accordion-body {{
            padding: 0 0 40px 90px;
            padding-right: 40px;
        }}

        /* Tables */
        .table-scroll-wrapper {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            margin-bottom: 8px;
        }}

        .check-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            min-width: 600px;
        }}

        .check-table th {{
            text-align: left;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--tp-text-light);
            padding: 12px 15px;
            border-bottom: 2px solid #e0e0e0;
            background-color: var(--tp-bg);
            white-space: normal;
            word-wrap: break-word;
        }}

        .check-table td {{
            padding: 14px 15px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 16px;
            white-space: normal;
            word-wrap: break-word;
        }}

        .check-table tr:last-child td {{
            border-bottom: none;
        }}

        .check-table tr:hover td {{
            background-color: rgba(255, 107, 53, 0.03);
        }}

        .score-cell {{
            font-family: monospace;
            font-weight: 700;
            text-align: center;
            white-space: nowrap;
        }}

        .score-cell.success {{ color: var(--success); }}
        .score-cell.warning {{ color: var(--warning); }}
        .score-cell.danger {{ color: var(--danger); }}

        .status-pass {{ color: var(--success); font-weight: 600; }}
        .status-fail {{ color: var(--danger); font-weight: 600; }}
        .status-warn {{ color: var(--warning); font-weight: 600; }}

        .total-row td {{
            background-color: var(--tp-bg-alt);
        }}

        .score-label {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .score-label.success {{ background-color: rgba(0, 200, 83, 0.1); color: var(--success); }}
        .score-label.warning {{ background-color: rgba(255, 179, 0, 0.1); color: var(--warning); }}
        .score-label.danger {{ background-color: rgba(255, 23, 68, 0.1); color: var(--danger); }}

        /* Role badges */
        .role-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .role-badge.driver {{ background-color: rgba(0, 200, 83, 0.1); color: var(--success); }}
        .role-badge.inhibitor {{ background-color: rgba(255, 23, 68, 0.1); color: var(--danger); }}

        /* Meaning toggle rows */
        .meaning-toggle {{
            padding: 5px 10px;
            background: var(--tp-bg-alt);
            border-radius: 50%;
            color: var(--tp-accent);
            transition: var(--tp-transition);
        }}

        .meaning-toggle:hover {{
            background: var(--tp-accent);
            color: var(--tp-white);
        }}

        .meaning-row {{
            display: none;
        }}

        .meaning-row.visible {{
            display: table-row;
        }}

        .meaning-content {{
            padding: 15px 20px;
            background: var(--tp-bg-alt);
            border-radius: var(--tp-radius);
            margin: 5px 0;
        }}

        /* 4-block tooltip */
        .meaning-content.four-block {{
            padding: 20px;
        }}

        .meaning-divider {{
            height: 1px;
            background: var(--tp-gray-2);
            margin: 15px 0;
        }}

        .tooltip-specific {{
            margin-top: 10px;
        }}

        .tooltip-specific-title {{
            font-size: 15px;
            font-weight: 700;
            color: var(--tp-primary);
            margin-bottom: 10px;
        }}

        .tooltip-specific-title i {{
            color: var(--tp-accent);
            margin-right: 8px;
        }}

        .finding-item {{
            font-size: 14px;
            color: var(--tp-text);
            padding: 6px 0;
            border-bottom: 1px solid var(--tp-gray-2);
            line-height: 1.5;
        }}

        .finding-item:last-child {{
            border-bottom: none;
        }}

        .fix-item-tooltip {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding: 8px 0;
            border-bottom: 1px solid var(--tp-gray-2);
        }}

        .fix-item-tooltip:last-child {{
            border-bottom: none;
        }}

        .fix-priority-dot {{
            font-size: 13px;
            font-weight: 600;
        }}

        .fix-priority-dot.high {{ color: var(--tp-accent); }}
        .fix-priority-dot.medium {{ color: var(--warning); }}
        .fix-priority-dot.low {{ color: var(--success); }}

        .fix-text-tooltip {{
            font-size: 14px;
            color: var(--tp-text);
        }}

        .fix-impact-tooltip {{
            font-size: 13px;
            color: var(--tp-text-light);
        }}

        .meaning-section {{
            font-size: 15px;
            color: var(--tp-text);
            margin-bottom: 10px;
            line-height: 1.6;
        }}

        .meaning-section:last-child {{
            margin-bottom: 0;
        }}

        .meaning-section i {{
            color: var(--tp-accent);
            margin-right: 8px;
        }}

        .meaning-section strong {{
            color: var(--tp-primary);
        }}

        /* Section explanation */
        .section-explanation {{
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.05) 0%, rgba(247, 183, 49, 0.05) 100%);
            padding: 20px 25px;
            border-radius: var(--tp-radius);
            border-left: 4px solid var(--tp-accent);
            margin-bottom: 25px;
        }}

        .explanation-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--tp-primary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .explanation-title i {{
            color: var(--tp-accent);
        }}

        .explanation-text {{
            font-size: 16px;
            color: var(--tp-text);
            line-height: 1.7;
        }}

        .explanation-text p {{
            margin-bottom: 10px;
        }}

        .explanation-text ul {{
            padding-left: 20px;
            list-style: disc;
            margin-bottom: 10px;
        }}

        .explanation-text li {{
            margin-bottom: 5px;
        }}

        .explanation-formula, .explanation-check, .explanation-freq {{
            font-size: 15px;
            margin-top: 10px;
            padding: 8px 12px;
            background: var(--tp-white);
            border-radius: 6px;
        }}

        .explanation-formula i, .explanation-check i, .explanation-freq i {{
            color: var(--tp-accent);
            margin-right: 8px;
        }}

        /* MECLABS Formula */
        .meclabs-formula {{
            background: linear-gradient(135deg, var(--tp-primary) 0%, #2a2a2a 100%);
            padding: 25px 30px;
            border-radius: var(--tp-radius);
            margin-bottom: 25px;
            text-align: center;
        }}

        .meclabs-formula h4 {{
            color: var(--tp-white);
            font-size: 16px;
            margin-bottom: 15px;
        }}

        .meclabs-formula h4 i {{
            color: var(--tp-accent);
            margin-right: 8px;
        }}

        .formula-code {{
            font-family: monospace;
            font-size: 20px;
            color: var(--tp-accent);
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 6px;
        }}

        /* Subsection title */
        .subsection-title {{
            font-size: 18px;
            font-weight: 600;
            color: var(--tp-primary);
            margin: 25px 0 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--tp-accent);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .subsection-title i {{
            color: var(--tp-accent);
        }}

        /* Findings list */
        .findings-list {{
            list-style: disc;
            padding-left: 20px;
        }}

        .findings-list li {{
            padding: 10px 0;
            border-bottom: 1px solid var(--tp-gray);
            color: var(--tp-text);
            font-size: 16px;
        }}

        .findings-list li:last-child {{
            border-bottom: none;
        }}

        /* Fixes list */
        .fixes-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .fix-item {{
            display: flex;
            align-items: flex-start;
            gap: 15px;
            padding: 15px 20px;
            background: var(--tp-white);
            border-radius: var(--tp-radius);
            border-left: 4px solid;
        }}

        .fix-item.priority-high {{ border-color: var(--tp-accent); }}
        .fix-item.priority-medium {{ border-color: var(--warning); }}
        .fix-item.priority-low {{ border-color: var(--success); }}

        .fix-priority {{
            flex-shrink: 0;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .fix-item.priority-high .fix-priority {{ background-color: rgba(255, 107, 53, 0.1); color: var(--tp-accent); }}
        .fix-item.priority-medium .fix-priority {{ background-color: rgba(255, 179, 0, 0.1); color: var(--warning); }}
        .fix-item.priority-low .fix-priority {{ background-color: rgba(0, 200, 83, 0.1); color: var(--success); }}

        .fix-text {{
            flex: 1;
            font-size: 16px;
            color: var(--tp-text);
        }}

        .fix-impact {{
            font-size: 14px;
            color: var(--tp-text-light);
            margin-top: 5px;
        }}

        /* Scoring explanation mobile */
        @media (max-width: 768px) {{
            .scoring-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Form audit */
        .form-audit-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }}

        .form-audit-item {{
            background: var(--tp-white);
            padding: 20px;
            border-radius: var(--tp-radius);
            border: 1px solid var(--tp-gray-2);
        }}

        .form-audit-label {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--tp-text-light);
            margin-bottom: 8px;
        }}

        .form-audit-value {{
            font-size: 26px;
            font-weight: 700;
            color: var(--tp-primary);
        }}

        .form-audit-note {{
            font-size: 14px;
            color: var(--tp-text-light);
            margin-top: 5px;
        }}

        .form-recommendation {{
            background: linear-gradient(135deg, rgba(255, 107, 53, 0.05) 0%, rgba(247, 183, 49, 0.05) 100%);
            padding: 20px 25px;
            border-radius: var(--tp-radius);
            border-left: 4px solid var(--tp-accent);
        }}

        .form-recommendation h4 {{
            font-size: 18px;
            font-weight: 600;
            color: var(--tp-primary);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .form-recommendation h4 i {{
            color: var(--tp-accent);
        }}

        .form-recommendation p {{
            font-size: 16px;
            color: var(--tp-text);
        }}

        /* A/B Tests */
        .ab-tests-list {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .ab-test-item {{
            display: flex;
            align-items: flex-start;
            gap: 15px;
            padding: 20px;
            background: var(--tp-white);
            border-radius: var(--tp-radius);
        }}

        .ab-test-number {{
            flex-shrink: 0;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--tp-accent);
            color: var(--tp-white);
            font-weight: 700;
            border-radius: 50%;
        }}

        .ab-test-content {{
            flex: 1;
        }}

        .ab-test-hypothesis {{
            font-size: 16px;
            color: var(--tp-text);
            line-height: 1.6;
            margin-bottom: 8px;
        }}

        .ab-test-metric {{
            font-size: 14px;
            color: var(--tp-accent);
            margin-bottom: 10px;
        }}

        .ab-test-metric i {{
            margin-right: 5px;
        }}

        .ab-variants {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .ab-variant {{
            padding: 10px 15px;
            background: var(--tp-bg-alt);
            border-radius: 6px;
        }}

        .ab-variant-label {{
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--tp-text-light);
            display: block;
            margin-bottom: 5px;
        }}

        .ab-variant code {{
            font-size: 15px;
            color: var(--tp-text);
            word-break: break-word;
        }}

        .ab-variant.variant-b {{
            background: rgba(255, 107, 53, 0.05);
            border: 1px solid rgba(255, 107, 53, 0.2);
        }}

        /* Missing triggers */
        .missing-triggers {{
            margin: 20px 0;
            padding: 15px 20px;
            background: var(--tp-bg-alt);
            border-radius: var(--tp-radius);
        }}

        .missing-triggers h4 {{
            font-size: 14px;
            font-weight: 600;
            color: var(--tp-primary);
            margin-bottom: 10px;
        }}

        .missing-triggers h4 i {{
            color: var(--warning);
            margin-right: 8px;
        }}

        .missing-item {{
            display: inline-block;
            padding: 4px 12px;
            background: var(--tp-white);
            border: 1px solid var(--tp-gray-2);
            border-radius: 15px;
            font-size: 14px;
            color: var(--tp-text);
            margin: 3px;
        }}

        .missing-weight {{
            color: var(--tp-text-light);
            font-size: 13px;
        }}

        /* Priority fixes */
        .priority-section {{
            margin-bottom: 25px;
        }}

        .priority-section:last-child {{
            margin-bottom: 0;
        }}

        .priority-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 12px;
            padding-left: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .priority-title i {{
            color: inherit;
        }}

        .priority-title.high {{ color: var(--tp-accent); }}
        .priority-title.medium {{ color: var(--warning); }}
        .priority-title.low {{ color: var(--success); }}

        .priority-items {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .priority-item {{
            padding: 16px 20px;
            background: var(--tp-white);
            border-radius: var(--tp-radius);
            border-left: 4px solid;
        }}

        .priority-item.high {{ border-color: var(--tp-accent); }}
        .priority-item.medium {{ border-color: var(--warning); }}
        .priority-item.low {{ border-color: var(--success); }}

        .priority-item-header {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 8px;
        }}

        .priority-num {{
            flex-shrink: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--tp-bg-alt);
            color: var(--tp-text-light);
            font-weight: 700;
            font-size: 14px;
            border-radius: 50%;
        }}

        .priority-item h5 {{
            flex: 1;
            font-size: 16px;
            font-weight: 600;
            color: var(--tp-primary);
        }}

        .priority-source {{
            font-size: 13px;
            color: var(--tp-text-light);
            margin: 0 0 4px 36px;
        }}

        .priority-source i {{
            color: var(--tp-accent);
            margin-right: 5px;
        }}

        .priority-impact {{
            font-size: 14px;
            color: var(--tp-text-light);
            margin: 0;
            padding-left: 36px;
        }}

        .priority-impact i {{
            color: var(--tp-accent);
            margin-right: 5px;
        }}

        /* No data */
        .no-data {{
            color: var(--tp-text-light);
            font-style: italic;
            padding: 15px 20px;
            background: var(--tp-bg-alt);
            border-radius: var(--tp-radius);
        }}

        /* Section summary */
        .section-summary {{
            margin-bottom: 20px;
        }}

        .summary-score {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 600;
        }}

        .summary-score i {{
            margin-right: 8px;
        }}

        .summary-score.success {{ background-color: rgba(0, 200, 83, 0.1); color: var(--success); }}
        .summary-score.warning {{ background-color: rgba(255, 179, 0, 0.1); color: var(--warning); }}
        .summary-score.danger {{ background-color: rgba(255, 23, 68, 0.1); color: var(--danger); }}

        /* CTA Section */
        .cta-section {{
            padding: 80px 20px;
            background: linear-gradient(135deg, var(--tp-primary) 0%, #2a2a2a 100%);
            text-align: center;
        }}

        .cta-section h2 {{
            font-size: clamp(24px, 4vw, 36px);
            font-weight: 700;
            color: var(--tp-white);
            margin-bottom: 20px;
            line-height: 1.3;
        }}

        .cta-section p {{
            font-size: 18px;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 30px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}

        .cta-section .tp-btn {{
            font-size: 14px;
            padding: 18px 40px;
        }}

        /* Footer */
        .tp-footer {{
            padding: 40px 0;
            background-color: var(--tp-bg-alt);
            text-align: center;
            border-top: 1px solid var(--tp-gray-2);
        }}

        .tp-footer p {{
            font-size: 14px;
            color: var(--tp-text-light);
        }}

        /* Responsive */
        @media (max-width: 1200px) {{
            .container {{
                max-width: 100%;
                padding: 0 20px;
            }}

            .services-accordion {{
                max-width: 100%;
            }}

            .scores-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        @media (max-width: 991px) {{
            .tp-menu-toggle {{
                display: flex !important;
            }}

            .tp-header-action .tp-btn {{
                display: none;
            }}

            .tp-main-menu {{
                position: fixed;
                top: 0;
                right: 0;
                left: auto;
                width: 320px;
                max-width: 100%;
                height: 100vh;
                background-color: var(--tp-white);
                clip-path: inset(0 0 0 100%);
                transition: clip-path 0.3s ease;
                z-index: 1001;
                box-shadow: -5px 0 20px rgba(0, 0, 0, 0.1);
                transform: none;
            }}

            .tp-main-menu.active {{
                clip-path: inset(0 0 0 0);
            }}

            .tp-nav-menu {{
                display: flex !important;
                flex-direction: column;
                gap: 0;
                padding-top: 100px;
                height: 100%;
            }}

            .tp-nav-menu .nav-links {{
                font-size: 18px;
                padding: 15px 0;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                display: block;
            }}

            .scores-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .services-accordion-number {{
                font-size: 32px;
                margin-right: 15px;
                min-width: 50px;
            }}

            .services-accordion-body {{
                padding-left: 0;
            }}

            .form-audit-grid {{
                grid-template-columns: 1fr;
            }}

            .score-card-tooltip {{
                display: none !important;
            }}

            .ab-variants {{
                grid-template-columns: 1fr;
            }}
        }}

        @media (max-width: 767px) {{
            .tp-hero {{
                padding: 100px 0 50px;
            }}

            .tp-hero-title {{
                font-size: 32px;
            }}

            .services-accordion-header {{
                flex-wrap: wrap;
                padding: 20px 0;
            }}

            .services-accordion-number {{
                font-size: 28px;
                width: 100%;
                margin-bottom: 10px;
            }}

            .section-score {{
                margin-left: 0;
                margin-top: 10px;
            }}

            .scores-grid {{
                grid-template-columns: 1fr;
            }}

            .score-card-value {{
                font-size: 36px;
            }}

            .cta-section h2 {{
                font-size: 24px;
            }}

            .cta-section p {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="tp-header" id="header-sticky">
        <div class="mobile-menu-backdrop" id="mobile_backdrop"></div>
        <div class="container">
            <div class="tp-header-inner">
                <div class="tp-header-logo">
                    <a href="https://open4.dev/">
                        <img src="https://open4.dev/images/open4_logo_small.png" alt="open4">
                    </a>
                </div>

                <nav class="tp-main-menu" id="main_menu">
                    <ul class="tp-nav-menu">
                        <li><a href="https://open4.dev/index.html" class="nav-links">Главная</a></li>
                        <li><a href="https://open4.dev/work.html" class="nav-links">Работы</a></li>
                        <li><a href="https://open4.dev/services.html" class="nav-links">Услуги</a></li>
                    </ul>
                </nav>

                <div class="tp-header-action">
                    <a href="https://open4.dev/#contact" class="tp-btn">
                        <span>Связаться</span>
                    </a>
                    <button class="tp-menu-toggle" id="menu_toggle" aria-label="Toggle menu">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="tp-hero">
        <div class="tp-hero-bg">
            <div class="tp-hero-shape tp-hero-shape-1"></div>
            <div class="tp-hero-shape tp-hero-shape-2"></div>
            <div class="tp-hero-shape tp-hero-shape-3"></div>
        </div>
        <div class="container">
            <div class="tp-hero-content">
                <span class="tp-hero-subtitle">CRO-анализ</span>
                <h1 class="tp-hero-title">{escape_html(domain)}</h1>
                <p class="tp-hero-description">Комплексный анализ конверсии посадочной страницы</p>
                <p class="tp-hero-date">{timestamp}</p>
                <div class="icp-badge">
                    <i class="fa-solid fa-users"></i> ЦА: {escape_html(icp_description)}
                </div>
            </div>
        </div>
    </section>

    <!-- Score Cards -->
    <section class="scores-section">
        <div class="container">
            <div class="scores-grid">
                {metrics_section}
            </div>
        </div>
    </section>

    <!-- Scoring Explanation -->
    <section class="scoring-explanation">
        <button class="scoring-toggle" onclick="toggleScoring()">
            <i class="fa-solid fa-chevron-down"></i>
            <span>📊 Как читать этот отчёт</span>
        </button>
        <div class="scoring-content" id="scoring_content">
            <!-- Шкала оценок -->
            <div class="scoring-scale">
                <div class="scoring-scale-item good">
                    <span class="scale-color">🟢</span>
                    <strong>70-100%</strong> — Отлично
                </div>
                <div class="scoring-scale-item warning">
                    <span class="scale-color">🟡</span>
                    <strong>40-69%</strong> — Есть потенциал роста
                </div>
                <div class="scoring-scale-item danger">
                    <span class="scale-color">🔴</span>
                    <strong>0-39%</strong> — Критично, требует внимания
                </div>
            </div>

            <!-- Порядок анализа -->
            <div class="scoring-order">
                <h4>🔍 Порядок анализа</h4>
                <ol>
                    <li><strong>Карточки</strong> — общая картина за 5 секунд</li>
                    <li><strong>01: CRO (MECLABS)</strong> — главный драйвер конверсии, 5 факторов с весами</li>
                    <li><strong>02: LIFT</strong> — потенциал улучшения, драйверы vs ингибиторы</li>
                    <li><strong>03-05: SS / TF / RR</strong> — детали оптимизации</li>
                    <li><strong>06-08: Мобильный / A/B / Действия</strong> — что делать дальше</li>
                </ol>
            </div>

            <!-- Кнопка ⓘ -->
            <div class="scoring-info-btn">
                <h4>💡 Кнопка ⓘ в таблицах раскрывает:</h4>
                <div class="info-grid">
                    <div class="info-item"><strong>Что это</strong> — объяснение фактора</div>
                    <div class="info-item"><strong>Что делать</strong> — общий совет</div>
                    <div class="info-item"><strong>Найдено</strong> — конкретные факты со страницы</div>
                    <div class="info-item"><strong>Рекомендации</strong> — конкретные действия с приоритетами</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Accordion Sections -->
    <section class="tp-sections">
        <div class="container">
            <div class="services-accordion">

                <!-- 01: MECLABS -->
                <div class="services-accordion-item active">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;01</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-calculator"></i>
                            <h3>CRO (MECLABS)</h3>
                        </div>
                        <span class="section-score {get_score_color(metrics.get('cro_score', 0), 100)}">{metrics.get('cro_score', 0)}%</span>
                        <span class="services-accordion-toggle"><i class="fas fa-minus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {meclabs_section}
                        </div>
                    </div>
                </div>

                <!-- 02: LIFT -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;02</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-chart-simple"></i>
                            <h3>LIFT</h3>
                        </div>
                        <span class="section-score {get_score_color(metrics.get('lift_score', 0), 100)}">{metrics.get('lift_score', 0)}%</span>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {lift_section}
                        </div>
                    </div>
                </div>

                <!-- 03: Scannability -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;03</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-eye"></i>
                            <h3>Scannability Score</h3>
                        </div>
                        <span class="section-score {get_score_color(metrics.get('scannability_score', 0), 100)}">{metrics.get('scannability_score', 0)}%</span>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {ss_section}
                        </div>
                    </div>
                </div>

                <!-- 04: Trust Factor -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;04</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-shield-halved"></i>
                            <h3>Trust Factor</h3>
                        </div>
                        <span class="section-score {get_score_color(min(metrics.get('trust_factor', 0), 10) * 10, 100)}">{metrics.get('trust_factor', 0)}</span>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {trust_section}
                        </div>
                    </div>
                </div>

                <!-- 05: Resonance Rate -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;05</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-bullseye"></i>
                            <h3>Resonance Rate</h3>
                        </div>
                        <span class="section-score {get_score_color(metrics.get('resonance_rate', 0), 100)}">{metrics.get('resonance_rate', 0)}%</span>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {resonance_section}
                        </div>
                    </div>
                </div>

                <!-- 06: Mobile Audit -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;06</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-mobile-screen"></i>
                            <h3>Мобильный аудит</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {mobile_section}
                        </div>
                    </div>
                </div>

                <!-- 07: A/B Tests -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;07</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-flask"></i>
                            <h3>A/B Тесты</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {ab_section}
                        </div>
                    </div>
                </div>

                <!-- 08: Prioritized Fixes -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;08</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-list-check"></i>
                            <h3>Приоритизированные исправления</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {fixes_section}
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Хотите радикально повысить конверсию?</h2>
            <p>Мы внедряем передовые инструменты ИИ для кратного роста конверсии. Напишите нам!</p>
            <a href="https://open4.dev/#contact" class="tp-btn tp-btn-accent">
                <span>Связаться</span>
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="tp-footer">
        <div class="container">
            <p>&copy; 2026 open4. Отчёт сгенерирован ИИ. ИИ может ошибаться — проверяйте рекомендации.</p>
        </div>
    </footer>

    <!-- Scripts -->
    <script>
        document.addEventListener('DOMContentLoaded', function(){{
            // Accordion
            const accordionItems = document.querySelectorAll('.services-accordion-item');
            accordionItems.forEach(item => {{
                const header = item.querySelector('.services-accordion-header');
                const toggle = item.querySelector('.services-accordion-toggle i');
                header.addEventListener('click', () => {{
                    const isActive = item.classList.contains('active');
                    if (isActive) {{
                        item.classList.remove('active');
                        toggle.classList.remove('fa-minus');
                        toggle.classList.add('fa-plus');
                    }} else {{
                        accordionItems.forEach(i => {{
                            i.classList.remove('active');
                            const t = i.querySelector('.services-accordion-toggle i');
                            if (t) {{
                                t.classList.remove('fa-minus');
                                t.classList.add('fa-plus');
                            }}
                        }});
                        item.classList.add('active');
                        toggle.classList.remove('fa-plus');
                        toggle.classList.add('fa-minus');
                    }}
                }});
            }});

            // Mobile menu
            const menuToggle = document.getElementById('menu_toggle');
            const mainMenu = document.getElementById('main_menu');
            const mobileBackdrop = document.getElementById('mobile_backdrop');

            if (menuToggle && mainMenu) {{
                menuToggle.addEventListener('click', () => {{
                    menuToggle.classList.toggle('active');
                    mainMenu.classList.toggle('active');
                    mobileBackdrop.classList.toggle('active');
                }});

                mobileBackdrop.addEventListener('click', () => {{
                    menuToggle.classList.remove('active');
                    mainMenu.classList.remove('active');
                    mobileBackdrop.classList.remove('active');
                }});
            }}
        }});

        function toggleScoring() {{
            const toggle = document.querySelector('.scoring-toggle');
            const content = document.getElementById('scoring_content');
            toggle.classList.toggle('active');
            content.classList.toggle('active');
        }}

        function toggleMeaning(btn) {{
            const row = btn.closest('tr').nextElementSibling;
            if (row && row.classList.contains('meaning-row')) {{
                row.classList.toggle('visible');
            }}
        }}
    </script>
</body>
</html>
    """

    return html


def main():
    if len(sys.argv) < 2:
        print("ОШИБКА: Не указан JSON файл с данными анализа.")
        print("")
        print("Использование:")
        print("  py -3 scripts/generate_landing_html.py --json <analysis.json>   # Windows")
        print("  python3 scripts/generate_landing_html.py --json <analysis.json>  # Linux/Mac")
        print("")
        print("Агент должен:")
        print("  1. Выполнить CRO-анализ страницы по научной методике")
        print("  2. Создать JSON файл с ключом 'analysis'")
        print("  3. Передать JSON в этот скрипт")
        sys.exit(1)

    url = sys.argv[1]
    json_data = None

    if url == "--json" and len(sys.argv) > 2:
        json_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("OPENCODE_WORKING_DIR", os.getcwd())
        print(f"Загрузка данных из JSON: {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        url = json_data.get("url", "unknown")
        icp_description = json_data.get("icp", "generic problem-aware audience")
        analysis = json_data.get("analysis", json_data)
    else:
        print("ОШИБКА: Скрипт требует JSON файл с данными.")
        print("Сначала выполните анализ страницы, затем передайте JSON:")
        print("  py -3 scripts/generate_landing_html.py --json <file.json>")
        sys.exit(1)

    html = generate_html_report(url, analysis, icp_description)

    os.makedirs(output_dir, exist_ok=True)
    filename = get_timestamp_filename(url, "LANDING-CRO") + ".html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML отчёт сохранён: {filepath}")
    return filepath


if __name__ == "__main__":
    main()
