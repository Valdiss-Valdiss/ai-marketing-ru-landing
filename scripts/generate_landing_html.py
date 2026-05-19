#!/usr/bin/env python3
"""
Generate Landing Page CRO Audit HTML Report — AI Marketing Claude Code Skills
Создаёт профессиональный HTML отчёт со стилем open4.dev.

Исправления:
1. Tooltips на score-карточках (CRO Score, VPI, SS, TF, RR)
2. Все заголовки секций — только числа 1-13 (без слов)
3. Уникальные иконки для каждой секции
4. Детальные пояснения для каждой секции
5. Findings с конкретными фактами + чёткие рекомендации
6. Accordion: минус когда открыто, плюс когда закрыто
7. Все фиксы из анализа в приоритизированных исправлениях
8. Сохранение в директорию запуска скилла
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


def get_timestamp_filename(url, prefix="LANDING-CRO"):
    """Генерация имени файла с timestamp."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"{prefix}-{domain}-{timestamp}"


def get_metric_value(key, vpi, ss, tf, rr, cro_score):
    """Получить числовое значение метрики для color calculation."""
    if key == "cro":
        return int(cro_score) if cro_score else 0
    elif key == "vpi":
        return int(vpi) if vpi else 0
    elif key == "ss":
        return int(ss) if ss else 0
    elif key == "tf":
        return int(tf) if tf else 0
    elif key == "rr":
        return int(rr) if rr else 0
    return 0

def get_metric_max(key):
    """Получить максимум для метрики."""
    return 100 if key in ("cro", "ss", "rr") else 10


def generate_metrics_section(metrics):
    """Генерация секции с метриками + tooltips."""
    vpi = metrics.get("vpi", 0)
    ss = metrics.get("scannability_score", 0)
    tf = metrics.get("trust_factor", 0)
    rr = metrics.get("resonance_rate", 0)
    cro_score = metrics.get("cro_score", 0)

    tooltips = {
        "cro": {
            "title": "CRO Score — Общий коэффициент конверсии",
            "desc": "综合ная оценка эффективности посадочной страницы по формуле MECLABS. Оценивает мотивацию, ценностное предложение, стимулы, трение и тревогу пользователя.",
            "formula": "C = M×4 + V×3 + I×2 + F×2 + A×2",
            "range": "0-100: <40 низкий, 40-70 средний, >70 высокий"
        },
        "vpi": {
            "title": "VPI — Индекс ценностного предложения",
            "desc": "Оценивает силу и ясность обещания продукта. Включает 4 вектора: Appeal (привлекательность), Exclusivity (эксклюзивность), Credibility (достоверность), Clarity (ясность). Чем выше — тем убедительнее оффер.",
            "formula": "Среднее 4 векторов × 10",
            "range": "1-10: <4 слабое, 4-7 среднее, >7 сильное"
        },
        "ss": {
            "title": "SS — Индекс сканируемости",
            "desc": "Процент контента, который пользователь способен воспринять за 5 секунд просмотра. Зависит от структуры, заголовков, визуальной иерархии и плотности текста.",
            "formula": "(Читаемые блоки / Всего блоков) × 100",
            "range": "0-100%: <50% плохая, 50-70% средняя, >70% хорошая"
        },
        "tf": {
            "title": "TF — Фактор доверия",
            "desc": "Количество активных триггеров доверия на странице. Включает: гарантии, отзывы, сертификаты, логотипы клиентов, кейсы, упоминания в СМИ. Каждый триггер снижает тревогу.",
            "formula": "Σ триггеров доверия",
            "range": "0-N: <3 критично, 3-5 недостаточно, >5 достаточно"
        },
        "rr": {
            "title": "RR — Коэффициент резонанса",
            "desc": "Процент болей целевой аудитории, которые закрыты решениями на странице. Измеряет соответствие контента потребностям посетителя. Чем выше — тем релевантнее предложение.",
            "formula": "(Решённые боли / Все боли ICP) × 100",
            "range": "0-100%: <30% слабое, 30-60% среднее, >60% сильное"
        }
    }

    cards_html = ""
    cards_data = [
        ("cro", "CRO", cro_score, "100", "fa-chart-line"),
        ("vpi", "VPI", vpi, "10", "fa-gift"),
        ("ss", "SS", f"{ss}%", "Сканируемость", "fa-eye"),
        ("tf", "TF", tf, "Триггеров", "fa-shield-halved"),
        ("rr", "RR", f"{rr}%", "Резонанс", "fa-bullseye"),
    ]

    for key, label, value, max_val, icon in cards_data:
        tt = tooltips[key]
        metric_val = get_metric_value(key, vpi, ss, tf, rr, cro_score)
        metric_max = get_metric_max(key)
        color_class = get_score_color(metric_val, metric_max)
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
                            <div class="score-card-max">/ {max_val}</div>
                        </div>
        """

    return cards_html


def generate_meclabs_section(metrics):
    """Генерация секции MECLABS с детальным пояснением."""
    motivation = metrics.get("motivation", 0)
    value_prop = metrics.get("value_proposition", 0)
    incentive = metrics.get("incentive", 0)
    friction = metrics.get("friction", 0)
    anxiety = metrics.get("anxiety", 0)
    cro_score = metrics.get("cro_score", 0)

    formula = f"{motivation}×4 + {value_prop}×3 + {incentive}×2 + {friction}×2 + {anxiety}×2 = {cro_score}"

    meclabs_items = [
        ("M", "Мотивация", motivation, "Внутренняя мотивация пользователя — насколько человек хочет решить свою проблему. Внешний фактор, независящий от страницы. Чем сильнее боль или желание — тем выше мотивация.",
         "Исследуйте свою аудиторию. Мотивация не создаётся страницей — она уже существует. Задача: усилить восприятие проблемы."),
        ("V", "Ценностное предложение", value_prop, "Сила обещания продукта. Оценивается по 4 векторам: Appeal (привлекательность), Exclusivity (эксклюзивность), Credibility (достоверность), Clarity (ясность).",
         "Чётко ответьте на вопрос: 'Что получу я и почему это лучше, чем у конкурентов?' Избегайте generic-фраз."),
        ("I", "Стимулы", incentive, "Дополнительные триггеры: бонусы, скидки, urgency-элементы, ограниченные предложения. Снижают порог принятия решения.",
         "Добавьте конкретный стимул: 'Первый месяц бесплатно', 'Осталось 3 места', 'Скидка 20% только сегодня'."),
        ("F", "Трение", friction, "Всё, что усложняет действие: сложные формы, много полей, непонятный процесс, длинные тексты без структуры. Чем меньше трения — тем выше конверсия.",
         "Упростите: максимум 3-5 полей в форме, используйте placeholder-тексты, добавьте прогресс-бар для многошаговых форм."),
        ("A", "Тревога", anxiety, "Страх совершить ошибку: 'А если не сработает?', 'Мои данные в безопасности?', 'А если не понравится?'. Каждый вопрос = потенциальный отказ.",
         "Разместите тревогу рядом с CTA: гарантии, отзывы, сертификаты безопасности, политика возврата.")
    ]

    rows = ""
    for code, name, score, meaning, action in meclabs_items:
        color_class = get_score_color(score, 10)
        label = get_score_label(score, 10)
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
                                                <div class="meaning-content">
                                                    <div class="meaning-section"><i class="fa-solid fa-lightbulb"></i> <strong>Что это:</strong> {meaning}</div>
                                                    <div class="meaning-section"><i class="fa-solid fa-wand-magic-sparkles"></i> <strong>Что делать:</strong> {action}</div>
                                                </div>
                                            </td>
                                        </tr>
        """

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-flask"></i> Научная основа: формула MECLABS</div>
        <div class="explanation-text">
            <p>Формула разработана в институте <strong>MECLABS</strong> (США) после 15+ лет исследований и A/B тестов на миллионах посадочных страниц.
            Каждый фактор имеет вес, определённый эмпирически:</p>
            <ul>
                <li><strong>M×4</strong> — Мотивация имеет наибольший вес. Без мотивации никакой дизайн не сработает.</li>
                <li><strong>V×3</strong> — Ценностное предложение — ядро коммуникации. Должно быть уникальным и конкретным.</li>
                <li><strong>I×2</strong> — Стимулы дают дополнительный толчок, но не заменяют слабое предложение.</li>
                <li><strong>F×2</strong> — Трение снижает конверсию. Каждое лишнее действие = потерянный клиент.</li>
                <li><strong>A×2</strong> — Тревога убивает конверсию. Особенно на этапе принятия решения.</li>
            </ul>
            <p><strong>Важно:</strong> Оценки M, V, I, F, A — субъективны и основаны на контент-анализе страницы. Для точного расчёта используйте A/B тесты.</p>
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


def generate_lift_section(metrics):
    """Генерация секции LIFT с детальным пояснением."""
    lift_relevance = metrics.get("lift_relevance", 0)
    lift_clarity = metrics.get("lift_clarity", 0)
    lift_urgency = metrics.get("lift_urgency", 0)
    lift_value = metrics.get("lift_value", 0)
    lift_anxiety = metrics.get("lift_anxiety", 0)
    lift_distraction = metrics.get("lift_distraction", 0)

    lift_items = [
        ("01", "Релевантность", lift_relevance, "Драйвер", "Насколько заголовок и первые строки соответствуют ожиданиям аудитории. Если посетитель не видит себя в сообщении — уходит.",
         "Проверьте: заголовок должен отвечать на вопрос 'Это для меня?' в первые 2 секунды."),
        ("02", "Ясность", lift_clarity, "Драйвер", "Простота языка, отсутствие жаргона, чёткость CTA. Посетитель должен мгновенно понять, что делать.",
         "Используйте слова из словаря клиента, а не продукта. Технические термины = барьер."),
        ("03", "Срочность", lift_urgency, "Драйвер", "Временные ограничения или дефицит. Мотивирует действовать сейчас, а не потом.",
         "Добавьте: countdown-таймер, 'Осталось X мест', 'Акция до конца недели'. Без срочности — откладывают."),
        ("04", "Ценностное предложение", lift_value, "Базис", "Соотношение выгод и затрат. Пользователь оценивает: 'Что я получу vs сколько стоит/делаю'.",
         "Всегда рядом с ценой показывайте выгоду. '199$/мес' без контекста = дорого. '199$/мес — экономия 4 часов/день' = выгодно."),
        ("05", "Тревога", lift_anxiety, "Ингибитор", "Отсутствие доверительных сигналов. Каждый вопрос в голове пользователя = сомнение = отказ.",
         "Тревога максимальна рядом с CTA. Добавьте: гарантии, отзывы, сертификаты, 'Без кредитной карты'."),
        ("06", "Отвлечение", lift_distraction, "Ингибитор", "Лишние ссылки, всплывающие окна, навигация, конкурирующая с CTA. Всё, что уводит от цели.",
         "Уберите всё, что не помогает конвертировать. Каждая ссылка = потенциальный уход. Оставьте только 'выход'.")
    ]

    rows = ""
    for num, name, score, role, meaning, action in lift_items:
        color_class = get_score_color(score, 10)
        role_class = "driver" if role == "Драйвер" else "inhibitor"
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
                                                <div class="meaning-content">
                                                    <div class="meaning-section"><i class="fa-solid fa-lightbulb"></i> <strong>Суть:</strong> {meaning}</div>
                                                    <div class="meaning-section"><i class="fa-solid fa-wand-magic-sparkles"></i> <strong>Что делать:</strong> {action}</div>
                                                </div>
                                            </td>
                                        </tr>
        """

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-chart-simple"></i> LIFT Framework — модель конверсии Крис Говарда</div>
        <div class="explanation-text">
            <p><strong>LIFT</strong> (Low Investment Fuelled Transaction) — фреймворк для оптимизации конверсии, разработанный <strong>Conversion.com</strong>.
            Выделяет 6 факторов, влияющих на решение о конверсии:</p>
            <ul>
                <li><strong>4 драйвера</strong> (повышают конверсию): Релевантность, Ясность, Срочность, Ценностное предложение</li>
                <li><strong>2 ингибитора</strong> (снижают конверсию): Тревога, Отвлечение</li>
            </ul>
            <p>Формула: <strong>Конверсия = Σ(Драйверы) - Σ(Ингибиторы)</strong></p>
            <p>Каждый фактор оценивается от 1 до 10. Идеальная страница: высокие драйверы + низкие ингибиторы.</p>
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


def generate_sections_table(sections):
    """Генерация таблицы секций с числами."""
    section_order = [
        ("hero", "01", "Hero-секция", 25),
        ("value_proposition", "02", "Ценностное предложение", 20),
        ("social_proof", "03", "Социальное доказательство", 15),
        ("features", "04", "Функции и выгоды", 15),
        ("objection_handling", "05", "Обработка возражений", 10),
        ("cta", "06", "Призыв к действию", 10),
        ("footer", "07", "Футер и элементы", 5),
    ]

    rows = ""
    for key, num, name, weight in section_order:
        score = sections.get(key, {}).get("score", 0)
        max_score = sections.get(key, {}).get("max", 10)
        color_class = get_score_color(score, max_score)
        contribution = score * weight / 10
        rows += f"""
                                        <tr>
                                            <td><strong>{num}</strong></td>
                                            <td>{name}</td>
                                            <td class="score-cell {color_class}">{score}/{max_score}</td>
                                            <td>{weight}%</td>
                                            <td>{contribution:.1f}</td>
                                        </tr>
        """

    return f"""
                            <div class="table-scroll-wrapper">
                                <table class="check-table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Секция</th>
                                            <th>Оценка</th>
                                            <th>Вес</th>
                                            <th>Вклад</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>
    """


def get_section_icon(section_key):
    """Уникальная иконка для каждой секции."""
    icons = {
        "hero": "fa-rocket",
        "value_proposition": "fa-gem",
        "social_proof": "fa-users",
        "features": "fa-list-check",
        "objection_handling": "fa-comments",
        "cta": "fa-hand-pointer",
        "footer": "fa-sitemap"
    }
    return icons.get(section_key, "fa-circle")


def get_section_meaning(section_key):
    """Детальное пояснение для каждой секции."""
    meanings = {
        "hero": {
            "title": "Зачем анализировать Hero-секцию",
            "desc": "Первый экран — это <strong>80% решений о конверсии</strong>. Посетитель решает за 2-5 секунд, остаться или уйти. Hero должна:"
                     "<br/>1) Показать, что это для НЕГО"
                     "<br/>2) Дать конкретную выгоду (не функцию)"
                     "<br/>3) Показать следующий шаг (CTA)"
                     "<br/>4) Создать доверие (badges, логотипы)",
            "formula": "First Impression Score = (Headline×0.3 + Subheadline×0.2 + CTA×0.3 + Trust×0.2)",
            "what_to_check": "Заголовок до 10 слов? Выгода, а не функция? CTA над сгибом? Контрастный цвет? Визуал релевантный?",
            "frequency": "A/B-тестируйте каждые 2-4 недели. Hero даёт максимальный ROI на изменение."
        },
        "value_proposition": {
            "title": "Зачем анализировать Ценностное предложение",
            "desc": "Ценностное предложение — это <strong>ответ на вопрос 'Почему я?'</strong>. Оно должно быть:"
                     "<br/>1) Конкретным (числа, результаты)"
                     "<br/>2) Уникальным (отличие от конкурентов)"
                     "<br/>3) Релевантным (для моей проблемы)"
                     "<br/>4) Квантифицированным (сколько сэкономлю/заработаю)",
            "formula": "VPI = (Appeal + Exclusivity + Credibility + Clarity) / 4 × 10",
            "what_to_check": "Используйте 4U-тест: Useful? Urgent? Unique? Ultra-specific?",
            "frequency": "Пересматривайте при каждом изменении продукта или выхода на новый сегмент."
        },
        "social_proof": {
            "title": "Зачем анализировать Социальное доказательство",
            "desc": "Люди <strong>следуют за толпой</strong>. Социальное доказательство снижает тревогу и ускоряет решение. Ранжирование по силе:"
                     "<br/>1) Revenue/результаты ('2.4 млрд обработано')"
                     "<br/>2) Именованные отзывы с фото, должностью, компанией"
                     "<br/>3) Узнаваемые логотипы клиентов"
                     "<br/>4) Кейсы с конкретными результатами"
                     "<br/>5) Рейтинги и количество отзывов",
            "formula": "Trust Score = Σ(типы_доказательств × коэффициент_убедительности)",
            "what_to_check": "Размещено ли социальное доказательство рядом с CTA? Не дальше 200 символов.",
            "frequency": "Добавляйте новые отзывы ежемесячно. Удаляйте устаревшие."
        },
        "features": {
            "title": "Зачем анализировать Функции и выгоды",
            "desc": "Пользователи покупают <strong>выгоды, а не функции</strong>. Задача секции:"
                     "<br/>1) Показать, ЧТО делает продукт"
                     "<br/>2) Объяснить, КАК это помогает"
                     "<br/>3) Показать конкретный результат",
            "formula": "Feature→Benefit трансформация: 'Функция' → 'Что это делает для меня' → 'Конкретный результат'",
            "what_to_check": "Плохо: 'AI-аналитика'. Хорошо: 'Узнайте точно какие кампании приносят доход — AI анализирует ваши данные'.",
            "frequency": "Проверяйте каждый feature на соответствие: function → benefit → value."
        },
        "objection_handling": {
            "title": "Зачем анализировать Обработку возражений",
            "desc": "У каждого посетителя <strong>есть возражения</strong>. Задача страницы — ответить на них ДО того, как он уйдёт. Топ-5 возражений:"
                     "<br/>1) 'Слишком дорого' → ROI калькулятор, сравнение, гарантия"
                     "<br/>2) 'Не уверен что работает' → Кейсы, пробный период, демо"
                     "<br/>3) 'Слишком сложно' → Онбординг, 'начните за 5 минут'"
                     "<br/>4) 'Не уверен что нужно' → Проблема → стоимость бездействия"
                     "<br/>5) 'А если не понравится?' → Пробный период, гарантия",
            "formula": "Objection Coverage = (Отвеченные возражения / Все возражения) × 100%",
            "what_to_check": "Есть ли FAQ? Гарантии рядом с CTA? Отзывы решают конкретные страхи?",
            "frequency": "Собирайте возражения из support-тикетов и добавляйте на страницу ежеквартально."
        },
        "cta": {
            "title": "Зачем анализировать CTA",
            "desc": "CTA — <strong>момент истины</strong>. Всё, что построили до этого, готовит кнопку. Оценка:"
                     "<br/>• Слабый: 'Отправить', 'Узнать больше'"
                     "<br/>• Средний: 'Зарегистрироваться', 'Начать'"
                     "<br/>• Сильный: 'Начать мой бесплатный период', 'Получить мою скидку'",
            "formula": "CTA Power = (Ценность_в_тексте + Контрастность + Позиционирование + Микротекст) × Первое_лицо",
            "what_to_check": "Текст описывает ценность? Кнопка визуально доминирует? Использует первое лицо ('Мой', не 'Ваш')?",
            "frequency": "A/B тестируйте тексты CTA постоянно. Это самое простое изменение с высоким ROI."
        },
        "footer": {
            "title": "Зачем анализировать Футер",
            "desc": "Футер — <strong>финальный якорь доверия</strong>. Даже если пользователь прокрутил всю страницу, он может конвертироваться здесь."
                     "<br/>Обязательные элементы:"
                     "<br/>1) Повторный CTA"
                     "<br/>2) Контактные данные"
                     "<br/>3) Политика конфиденциальности"
                     "<br/>4) Повторные trust badges"
                     "<br/>5) Ссылки на соцсети (если помогают доверию)",
            "formula": "Footer Trust Score = (Контакты × 0.2 + Политика × 0.2 + Trust × 0.3 + CTA × 0.3)",
            "what_to_check": "Нет ли конкурирующих ссылок? Trust badges повторены? Final CTA присутствует?",
            "frequency": "Проверяйте актуальность контактов и политик ежеквартально."
        }
    }
    return meanings.get(section_key, {})


def generate_section_detail(section_key, section_num, section_title, sections):
    """Генерация детальной секции с находками, пояснениями и рекомендациями."""
    data = sections.get(section_key, {})
    score = data.get("score", 0)
    max_score = data.get("max", 10)
    findings = data.get("findings", [])
    fixes = data.get("fixes", [])
    color_class = get_score_color(score, max_score)

    meaning = get_section_meaning(section_key)

    icon = get_section_icon(section_key)

    findings_html = ""
    if findings:
        findings_html = "<ul class='findings-list'>"
        for finding in findings[:10]:
            if isinstance(finding, dict):
                finding_text = finding.get("text", str(finding))
                finding_impact = finding.get("impact", "")
                if finding_impact:
                    findings_html += f"<li><strong>Что:</strong> {escape_html(finding_text)}<br><strong>Как влияет:</strong> {escape_html(finding_impact)}</li>"
                else:
                    findings_html += f"<li>{escape_html(finding_text)}</li>"
            else:
                findings_html += f"<li>{escape_html(str(finding))}</li>"
        findings_html += "</ul>"
    else:
        findings_html = "<p class='no-data'>— На основе анализа данные не получены. Возможно, страница не содержит достаточной информации для оценки этой секции.</p>"

    fixes_html = ""
    if fixes:
        fixes_html = "<div class='fixes-list'>"
        for fix in fixes:
            priority = fix.get("priority", "MEDIUM")
            text = fix.get("text", "")
            impact = fix.get("impact", "")
            priority_class = priority.lower()
            fixes_html += f"""
                                    <div class="fix-item priority-{priority_class}">
                                        <span class="fix-priority">{priority}</span>
                                        <span class="fix-text">{escape_html(text)}</span>
                                        <span class="fix-impact">{escape_html(impact)}</span>
                                    </div>
        """
        fixes_html += "</div>"
    else:
        fixes_html = "<p class='no-data'>— Рекомендации не требуются — секция в хорошем состоянии.</p>"

    explanation_html = ""
    if meaning:
        explanation_html = f"""
                            <div class="section-explanation">
                                <div class="explanation-title"><i class="fa-solid fa-book-open"></i> {meaning.get('title', '')}</div>
                                <div class="explanation-text">
                                    <p>{meaning.get('desc', '')}</p>
                                    <div class="explanation-formula"><i class="fa-solid fa-function"></i> <strong>Формула/логика:</strong> {meaning.get('formula', '')}</div>
                                    <div class="explanation-check"><i class="fa-solid fa-clipboard-check"></i> <strong>Что проверять:</strong> {meaning.get('what_to_check', '')}</div>
                                    <div class="explanation-freq"><i class="fa-solid fa-calendar"></i> <strong>Частота проверки:</strong> {meaning.get('frequency', '')}</div>
                                </div>
                            </div>
    """

    return f"""
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;{section_num}</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid {icon}"></i>
                            <h3>{escape_html(section_title)}</h3>
                        </div>
                        <span class="section-score {color_class}">{score}/{max_score}</span>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
{explanation_html}
                            <div class="section-summary">
                                <div class="summary-score {color_class}">
                                    <i class="fa-solid fa-chart-column"></i> {get_score_label(score, max_score).upper()}
                                </div>
                            </div>
                            <h4 class="subsection-title"><i class="fa-solid fa-magnifying-glass"></i> Что найдено</h4>
                            {findings_html}
                            <h4 class="subsection-title"><i class="fa-solid fa-wand-magic-sparkles"></i> Что делать</h4>
                            {fixes_html}
                        </div>
                    </div>
                </div>
    """


def generate_copy_fixes(fixes):
    """Генерация блока рекомендаций по копирайтингу."""
    if not fixes:
        return "<p class='no-data'>— Рекомендации не требуются.</p>"

    html = ""
    for fix in fixes:
        priority = fix.get("priority", "MEDIUM")
        text = fix.get("text", "")
        impact = fix.get("impact", "")
        priority_class = priority.lower()
        html += f"""
                                <div class="fix-item priority-{priority_class}">
                                    <span class="fix-priority">{priority}</span>
                                    <span class="fix-text">{escape_html(text)}</span>
                                    <span class="fix-impact">{escape_html(impact)}</span>
                                </div>
        """
    return html


def generate_copy_section(copy_score, all_fixes):
    """Генерация секции копирайтинга с детальным пояснением."""
    # Support both nested (dimensions) and flat (direct keys) JSON structures
    if "dimensions" in copy_score and copy_score["dimensions"]:
        dimensions = copy_score["dimensions"]
    else:
        dimensions = copy_score  # flat structure fallback

    clarity = dimensions.get("clarity", 0)
    urgency = dimensions.get("urgency", 0)
    specificity = dimensions.get("specificity", 0)
    proof = dimensions.get("proof", 0)
    # Handle both "action" and "action_orientation" key names
    action_orientation = dimensions.get("action") or dimensions.get("action_orientation", 0)
    total = copy_score.get("total", 0)

    copy_items = [
        ("01", "Ясность (Clarity)", clarity, "Может ли посетитель понять предложение за 5 секунд? Оценивается: понятны ли заголовок, подзаголовок, CTA без дополнительного контекста.",
         "Проверка: покажите страницу человеку на 5 секунд. Спросите: 'Что это за продукт?' Если ответить не может — ясность низкая."),
        ("02", "Срочность (Urgency)", urgency, "Есть ли причина действовать СЕЙЧАС, а не через неделю? Без срочности пользователь откладывает решение 'на потом', и чаще всего не возвращается.",
         "Добавьте: временные ограничения, дефицит, специальные условия только для новых клиентов."),
        ("03", "Конкретность (Specificity)", specificity, "Заявления конкретны с числами, сроками, результатами? Размытые фразы ('улучшим эффективность') не убеждают. Конкретика ('+40% конверсии за 2 недели') — убеждает.",
         "Замените泛-фразы на числа. 'Быстро' → 'за 15 минут'. 'Экономит время' → 'сэкономит 3 часа в день'."),
        ("04", "Доказательность (Proof)", proof, "Заявления подкреплены доказательствами? Любой факт должен быть подтверждён: отзывом, кейсом, статистикой, сертификатом.",
         "К каждому утверждению добавьте доказательство: 'Мы #1' → 'Нас выбрали 10,000+ компаний'. 'Лучшее решение' → 'Рейтинг 4.9/5 на G2'."),
        ("05", "Ориентация на действие", action_orientation, "Копирайтинг ведёт к конкретному следующему шагу? Каждый абзац должен подталкивать к действию, а не просто информировать.",
         "Используйте 'Транзитные' фразы: 'Итак, вы видите преимущества → Теперь попробуйте бесплатно'. Каждый блок контента = подготовка к CTA."),
    ]

    rows = ""
    for num, name, score, meaning, action in copy_items:
        color_class = get_score_color(score, 10)
        rows += f"""
                                        <tr>
                                            <td><strong>{num}</strong></td>
                                            <td><strong>{name}</strong></td>
                                            <td class="score-cell {color_class}">{score}/10</td>
                                            <td><button class="meaning-toggle" onclick="toggleMeaning(this)"><i class="fa-solid fa-circle-info"></i></button></td>
                                        </tr>
                                        <tr class="meaning-row">
                                            <td colspan="4">
                                                <div class="meaning-content">
                                                    <div class="meaning-section"><i class="fa-solid fa-lightbulb"></i> <strong>Что это:</strong> {meaning}</div>
                                                    <div class="meaning-section"><i class="fa-solid fa-wand-magic-sparkles"></i> <strong>Как улучшить:</strong> {action}</div>
                                                </div>
                                            </td>
                                        </tr>
        """

    total_color = get_score_color(total, 100)
    rows += f"""
                                        <tr class="total-row">
                                            <td colspan="2"><strong>ИТОГО</strong></td>
                                            <td class="score-cell {total_color}"><strong>{total}/100</strong></td>
                                            <td></td>
                                        </tr>
    """

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-pen-fancy"></i> Оценка копирайтинга — 5 измерений</div>
        <div class="explanation-text">
            <p>Копирайтинг посадочной страницы оценивается по 5 ключевым измерениям. Каждое влияет на конверсию по-разному:</p>
            <ul>
                <li><strong>Ясность (30% вес)</strong> — без неё пользователь не поймёт предложение. Это фундамент.</li>
                <li><strong>Срочность (20% вес)</strong> — без неё откладывает решение. Катализатор действия.</li>
                <li><strong>Конкретность (20% вес)</strong> — без неё нет доверия. Делает обещания реальными.</li>
                <li><strong>Доказательность (20% вес)</strong> — без неё голословные заявления. Снижает тревогу.</li>
                <li><strong>Ориентация на действие (10% вес)</strong> — без неё нет направления. Весь контент должен вести к CTA.</li>
            </ul>
            <p><strong>Формула:</strong> Total = (Clarity×0.3 + Urgency×0.2 + Specificity×0.2 + Proof×0.2 + Action×0.1) × 10</p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="table-scroll-wrapper">
                                <table class="check-table copy-table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Измерение</th>
                                            <th>Оценка</th>
                                            <th>Детали</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {rows}
                                    </tbody>
                                </table>
                            </div>

                            <h4 class="subsection-title"><i class="fa-solid fa-magnifying-glass"></i> Что найдено</h4>
                            <div class="findings-box">
                                <ul class="findings-list">
                                    <li>Ясность: {get_score_label(clarity, 10).lower()} ({clarity}/10) — {'заголовок и CTA понятны' if clarity >= 7 else 'есть неоднозначности в формулировках'}</li>
                                    <li>Срочность: {get_score_label(urgency, 10).lower()} ({urgency}/10) — {'призыв к действию ощущается' if urgency >= 7 else 'отсутствуют триггеры срочности'}</li>
                                    <li>Конкретность: {get_score_label(specificity, 10).lower()} ({specificity}/10) — {'заявления подкреплены цифрами' if specificity >= 7 else 'много размытых фраз без квантификации'}</li>
                                    <li>Доказательность: {get_score_label(proof, 10).lower()} ({proof}/10) — {'есть социальное доказательство' if proof >= 7 else 'мало данных для подтверждения'}</li>
                                    <li>Ориентация на действие: {get_score_label(action_orientation, 10).lower()} ({action_orientation}/10) — {'контент ведёт к CTA' if action_orientation >= 7 else 'нет чёткого направления к действию'}</li>
                                </ul>
                            </div>

                            <h4 class="subsection-title"><i class="fa-solid fa-wand-magic-sparkles"></i> Что делать</h4>
                            <div class="fixes-list">
                                {generate_copy_fixes(copy_score.get("fixes", []))}
                            </div>
    """


def generate_form_audit(form_audit, all_fixes):
    """Генерация секции аудита форм."""
    field_count = form_audit.get("field_count", "—")
    button_text = form_audit.get("button_text", "—")
    recommendation = form_audit.get("recommendation", "—")

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-wpforms"></i> Аудит форм — критический элемент конверсии</div>
        <div class="explanation-text">
            <p>Форма — <strong>момент принятия решения</strong>. Каждое дополнительное поле снижает конверсию на ~7%.</p>
            <ul>
                <li><strong>3 поля</strong> (имя, email, телефон) — оптимально для лидогенерации</li>
                <li><strong>5 полей</strong> — приемлемо для квалификации лида</li>
                <li><strong>7+ полей</strong> — критично, оставляют только самых мотивированных</li>
            </ul>
            <p><strong>Формула влияния:</strong> Conversion_Drop = (Fields - 3) × 7%</p>
            <p><strong>Лучшие практики:</strong></p>
            <ul>
                <li>Подписи полей над полем (не в placeholder)</li>
                <li>Текст кнопки = ценность ('Получить стратегию роста'), не действие ('Отправить')</li>
                <li>Inline-валидация с конкретными ошибками</li>
                <li>Placeholder с примером ('your@email.com')</li>
                <li>Прогресс-бар для многошаговых форм</li>
            </ul>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="form-audit-grid">
                                <div class="form-audit-item">
                                    <div class="form-audit-label">Количество полей</div>
                                    <div class="form-audit-value">{field_count}</div>
                                    <div class="form-audit-note">Рекомендуется: 3-5</div>
                                </div>
                                <div class="form-audit-item">
                                    <div class="form-audit-label">Текст кнопки</div>
                                    <div class="form-audit-value">{escape_html(truncate(button_text, 40))}</div>
                                    <div class="form-audit-note">Должен описывать ценность</div>
                                </div>
                            </div>
                            <div class="form-recommendation">
                                <h4><i class="fa-solid fa-clipboard-list"></i> Рекомендация</h4>
                                <p>{escape_html(recommendation)}</p>
                            </div>
    """


def generate_ab_tests(ab_tests):
    """Генерация секции A/B тестов."""
    if not ab_tests:
        return '<p class="no-data">— A/B тесты не сгенерированы. Для точного определения влияния изменений необходимо тестирование.</p>'

    tests_html = ""
    for i, test in enumerate(ab_tests[:10], 1):
        hypothesis = test.get("hypothesis", "")
        tests_html += f"""
                                <div class="ab-test-item">
                                    <div class="ab-test-number">{i}</div>
                                    <div class="ab-test-hypothesis">{escape_html(hypothesis)}</div>
                                </div>
        """

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-flask"></i> A/B тестирование — научный метод оптимизации</div>
        <div class="explanation-text">
            <p>Каждая рекомендация должна быть проверена через <strong>A/B тест</strong>. Принципы:</p>
            <ul>
                <li><strong>Одна переменная</strong> за раз — изменяйте только заголовок ИЛИ только CTA, но не оба</li>
                <li><strong>Статистическая значимость</strong> — минимум 100 конверсий на вариант</li>
                <li><strong>Сегментация</strong> — одна и та же кнопка может работать по-разному для разных сегментов</li>
                <li><strong>Минимальный срок</strong> — 2 недели, чтобы исключить day-of-week эффект</li>
            </ul>
            <p><strong>Формула значимости:</strong> p-value < 0.05 (95% доверительный интервал)</p>
            <p><strong>Шаблон гипотезы:</strong> 'Если мы [изменим X], тогда [метрика Y] [улучшится/увеличится], потому что [причина Z].'</p>
        </div>
    </div>
    """

    return f"""
{explanation}
                            <div class="ab-tests-list">
                                {tests_html}
                            </div>
    """


def collect_all_fixes(sections):
    """Собирает ВСЕ фиксы из всех секций для секции 'Приоритизированные исправления'."""
    all_fixes = []

    for section_key, section_data in sections.items():
        fixes = section_data.get("fixes", [])
        for fix in fixes:
            fix_copy = fix.copy()
            fix_copy["section"] = section_key
            all_fixes.append(fix_copy)

    return all_fixes


def generate_fixes_section(prioritized_fixes, sections):
    """Генерация секции приоритизированных фиксов — ВСЕ фиксы из анализа."""
    all_fixes = collect_all_fixes(sections)

    quick_wins = []
    medium_term = []
    strategic = []

    for fix in all_fixes:
        priority = fix.get("priority", "MEDIUM").upper()
        section = fix.get("section", "")
        text = fix.get("text", "")
        impact = fix.get("impact", "")

        if not text:
            continue

        fix_item = {
            "text": f"[{section.upper()}] {text}",
            "impact": impact
        }

        if priority == "HIGH" or priority == "CRITICAL":
            quick_wins.append(fix_item)
        elif priority == "MEDIUM":
            medium_term.append(fix_item)
        else:
            strategic.append(fix_item)

    def format_fixes(fixes, priority, icon_class, priority_label):
        if not fixes:
            return ""
        html = f'<div class="priority-section">'
        html += f'<h4 class="priority-title {priority}"><i class="fa-solid {icon_class}"></i> {priority_label}</h4>'
        html += '<div class="priority-items">'
        for i, fix in enumerate(fixes, 1):
            text = fix.get("text", "")
            impact = fix.get("impact", "")
            html += f"""
                                    <div class="priority-item {priority}">
                                        <div class="priority-item-header">
                                            <span class="priority-num">{i}</span>
                                            <h5>{escape_html(text)}</h5>
                                        </div>
                                        <p class="priority-impact"><i class="fa-solid fa-bullseye"></i> {escape_html(impact) if impact else 'Ожидаемый эффект не указан'}</p>
                                    </div>
            """
        html += '</div></div>'
        return html

    explanation = """
    <div class="section-explanation">
        <div class="explanation-title"><i class="fa-solid fa-list-check"></i> Приоритизация исправлений — матрица Эйзенхауэра</div>
        <div class="explanation-text">
            <p>Все обнаруженные проблемы распределяются по <strong>3 категориям</strong> в зависимости от усилия и влияния:</p>
            <ul>
                <li><strong>Быстрые победы (эта неделя)</strong> — высокое влияние, низкое усилие. Реализуйте в первую очередь.</li>
                <li><strong>Среднесрочные (этот месяц)</strong> — высокое влияние, высокое усилие. Планируйте и выполняйте последовательно.</li>
                <li><strong>Стратегические (этот квартал)</strong> — среднее влияние, высокое усилие. Инвестируйте, когда ресурсы позволяют.</li>
            </ul>
            <p><strong>Формула приоритизации:</strong> Priority = (Impact × 0.6 + Ease × 0.4) / Effort</p>
            <p><strong>Принцип:</strong> Сосредоточьтесь на быстрых победах — они дают максимальный ROI на усилия и помогают убедить стейкхолдеров в ценности CRO.</p>
        </div>
    </div>
    """

    fixes_html = explanation
    fixes_html += format_fixes(quick_wins, "high", "fa-bolt", "Быстрые победы (эта неделя)")
    fixes_html += format_fixes(medium_term, "medium", "fa-calendar-week", "Среднесрочные (этот месяц)")
    fixes_html += format_fixes(strategic, "low", "fa-chart-line", "Стратегические (этот квартал)")

    if not quick_wins and not medium_term and not strategic:
        fixes_html += '<p class="no-data">— Значительных проблем не обнаружено. Страница в хорошем состоянии.</p>'

    return fixes_html


def generate_html_report(url, analysis, icp_description):
    """Генерация полного HTML отчёта."""
    scores = analysis.get("scores", {})
    sections = analysis.get("sections", {})
    metrics = analysis.get("metrics", {})
    copy_score = analysis.get("copy_score", {})
    form_audit = analysis.get("form_audit", {})
    ab_tests = analysis.get("ab_tests", [])
    prioritized_fixes = analysis.get("prioritized_fixes", {})

    timestamp = datetime.now().strftime("%d %m %Y, %H:%M:%S")
    parsed = urlparse(url)
    domain = parsed.netloc
    cro_score = metrics.get("cro_score", 0)

    metrics_section = generate_metrics_section(metrics)
    meclabs_section = generate_meclabs_section(metrics)
    lift_section = generate_lift_section(metrics)
    sections_table = generate_sections_table(sections)

    section_order = [
        ("hero", "03", "Hero-секция"),
        ("value_proposition", "04", "Ценностное предложение"),
        ("social_proof", "05", "Социальное доказательство"),
        ("features", "06", "Функции и выгоды"),
        ("objection_handling", "07", "Обработка возражений"),
        ("cta", "08", "Призыв к действию"),
        ("footer", "09", "Футер и элементы"),
    ]

    details_html = ""
    for section_key, section_num, section_title in section_order:
        details_html += generate_section_detail(section_key, section_num, section_title, sections)

    copy_section = generate_copy_section(copy_score, sections)
    form_audit_section = generate_form_audit(form_audit, sections)
    ab_tests_section = generate_ab_tests(ab_tests)
    fixes_section = generate_fixes_section(prioritized_fixes, sections)

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
            font-size: 16px;
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
            font-size: 15px;
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
            font-size: 14px;
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
            font-size: 13px;
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
            font-size: 12px;
            color: var(--tp-text);
            border-bottom: 1px solid var(--tp-gray-2);
        }}

        .scoring-block li:last-child {{
            border-bottom: none;
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
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: var(--tp-accent);
            margin-bottom: 20px;
            padding: 10px 25px;
            background-color: rgba(255, 107, 53, 0.1);
            border-radius: 30px;
        }}

        .tp-hero-title {{
            font-size: clamp(40px, 8vw, 80px);
            font-weight: 800;
            line-height: 1.1;
            color: var(--tp-primary);
            margin-bottom: 20px;
        }}

        .tp-hero-description {{
            font-size: 18px;
            color: var(--tp-text-light);
            margin-bottom: 10px;
            line-height: 1.8;
        }}

        .tp-hero-date {{
            font-size: 14px;
            color: var(--tp-secondary);
        }}

        .icp-badge {{
            display: inline-block;
            margin-top: 15px;
            padding: 8px 20px;
            background-color: var(--tp-bg);
            border-radius: 20px;
            font-size: 13px;
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
        .score-card.vpi {{ border-top: 4px solid var(--tp-accent); }}
        .score-card.ss {{ border-top: 4px solid #667eea; }}
        .score-card.tf {{ border-top: 4px solid var(--success); }}
        .score-card.rr {{ border-top: 4px solid var(--warning); }}

        .score-card-label {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--tp-text-light);
            margin-bottom: 10px;
        }}

        .score-card-value {{
            font-size: 42px;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 5px;
        }}

        .score-card.cro .score-card-value {{ color: var(--tp-primary); }}
        .score-card.vpi .score-card-value {{ color: var(--tp-accent); }}
        .score-card.ss .score-card-value {{ color: #667eea; }}
        .score-card.tf .score-card-value {{ color: var(--success); }}
        .score-card.rr .score-card-value {{ color: var(--warning); }}

        .score-card-max {{
            font-size: 12px;
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
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--tp-accent);
        }}

        .tooltip-desc {{
            font-size: 12px;
            line-height: 1.5;
            margin-bottom: 10px;
        }}

        .tooltip-formula, .tooltip-range {{
            font-size: 11px;
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
            font-size: 20px;
            font-weight: 700;
            color: var(--tp-primary);
            margin: 0;
        }}

        .section-score {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
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
            font-size: 14px;
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
            font-size: 11px;
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
            font-size: 14px;
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
            font-size: 11px;
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
            font-size: 11px;
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

        .meaning-section {{
            font-size: 13px;
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
            font-size: 14px;
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
            font-size: 13px;
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
            font-size: 18px;
            color: var(--tp-accent);
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 6px;
        }}

        /* Subsection title */
        .subsection-title {{
            font-size: 16px;
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
            font-size: 14px;
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
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .fix-item.priority-high .fix-priority {{ background-color: rgba(255, 107, 53, 0.1); color: var(--tp-accent); }}
        .fix-item.priority-medium .fix-priority {{ background-color: rgba(255, 179, 0, 0.1); color: var(--warning); }}
        .fix-item.priority-low .fix-priority {{ background-color: rgba(0, 200, 83, 0.1); color: var(--success); }}

        .fix-text {{
            flex: 1;
            font-size: 14px;
            color: var(--tp-text);
        }}

        .fix-impact {{
            font-size: 12px;
            color: var(--tp-text-light);
            margin-top: 5px;
        }}

        /* Findings box in copy section */
        .findings-box {{
            padding: 15px 20px;
            background: var(--tp-bg);
            border-radius: var(--tp-radius);
            margin-bottom: 20px;
        }}

        .findings-box .findings-list {{
            margin: 0;
            padding: 0;
        }}

        .findings-box .findings-list li {{
            border-bottom-color: var(--tp-gray-2);
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
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--tp-text-light);
            margin-bottom: 8px;
        }}

        .form-audit-value {{
            font-size: 24px;
            font-weight: 700;
            color: var(--tp-primary);
        }}

        .form-audit-note {{
            font-size: 12px;
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
            font-size: 14px;
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
            font-size: 14px;
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

        .ab-test-hypothesis {{
            flex: 1;
            font-size: 14px;
            color: var(--tp-text);
            line-height: 1.6;
        }}

        /* Priority fixes */
        .priority-section {{
            margin-bottom: 25px;
        }}

        .priority-section:last-child {{
            margin-bottom: 0;
        }}

        .priority-title {{
            font-size: 16px;
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
            font-size: 12px;
            border-radius: 50%;
        }}

        .priority-item h5 {{
            flex: 1;
            font-size: 14px;
            font-weight: 600;
            color: var(--tp-primary);
        }}

        .priority-impact {{
            font-size: 12px;
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
            font-size: 14px;
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
            <span>Как считается CRO Score?</span>
        </button>
        <div class="scoring-content" id="scoring_content">
            <div class="scoring-grid">
                <div class="scoring-block">
                    <h4>Метрики карточек (верх страницы)</h4>
                    <ul>
                        <li><strong>CRO Score</strong> — Общая оценка конверсии страницы (0-100)</li>
                        <li><strong>VPI</strong> — Индекс ценностного предложения (1-10)</li>
                        <li><strong>SS</strong> — Индекс сканируемости (% видимого контента за 5 сек)</li>
                        <li><strong>TF</strong> — Фактор доверия (кол-во триггеров)</li>
                        <li><strong>RR</strong> — Коэффициент резонанса (% закрытых болей ICP)</li>
                    </ul>
                </div>
                <div class="scoring-block">
                    <h4>Оценки разделов (03-09)</h4>
                    <ul>
                        <li><strong>03: Hero</strong> — 25% | Заголовок, CTA, визуал над сгибом</li>
                        <li><strong>04: Ценностное предложение</strong> — 20% | Ясность и конкретность УТП</li>
                        <li><strong>05: Социальное доказательство</strong> — 15% | Отзывы, кейсы, логотипы</li>
                        <li><strong>06: Функции и выгоды</strong> — 15% | Перевод фич в выгоды</li>
                        <li><strong>07: Обработка возражений</strong> — 10% | FAQ, гарантии</li>
                        <li><strong>08: Призыв к действию</strong> — 10% | CTA текст, размещение</li>
                        <li><strong>09: Футер</strong> — 5% | Финальный CTA, контакты</li>
                    </ul>
                </div>
                <div class="scoring-block">
                    <h4>Связь: Карточки → CRO Score</h4>
                    <ul>
                        <li>CRO Score = Σ (оценка раздела × вес раздела)</li>
                        <li>VPI коррелирует с Hero и Ценностным предложением</li>
                        <li>SS зависит от структуры всех разделов</li>
                        <li>TF сильно зависит от Социального доказательства</li>
                        <li>RR зависит от Ценностного, Функций и Возражений</li>
                    </ul>
                </div>
                <div class="scoring-block">
                    <h4>Итого</h4>
                    <ul>
                        <li>Карточки = Быстрая визуальная оценка</li>
                        <li>Разделы 1-13 = глубокий анализ каждого блока</li>
                        <li>Они дополняют друг друга</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Accordion Sections -->
    <section class="tp-sections">
        <div class="container">
            <div class="services-accordion">

                <!-- 01: MECLABS Formula -->
                <div class="services-accordion-item active">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;01</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-calculator"></i>
                            <h3>MECLABS Формула конверсии</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-minus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {meclabs_section}
                        </div>
                    </div>
                </div>

                <!-- 02: LIFT Framework -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;02</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-chart-simple"></i>
                            <h3>LIFT Framework</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {lift_section}
                        </div>
                    </div>
                </div>

                <!-- Детальные секции 03-09 -->
                {details_html}

                <!-- 10: Копирайтинг -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;10</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-pen-fancy"></i>
                            <h3>Оценка копирайтинга</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {copy_section}
                        </div>
                    </div>
                </div>

                <!-- 11: Аудит форм -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;11</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-wpforms"></i>
                            <h3>Аудит форм</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {form_audit_section}
                        </div>
                    </div>
                </div>

                <!-- 12: A/B Тесты -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;12</span>
                        <div class="services-accordion-title">
                            <i class="fa-solid fa-flask"></i>
                            <h3>A/B Тесты</h3>
                        </div>
                        <span class="services-accordion-toggle"><i class="fas fa-plus"></i></span>
                    </div>
                    <div class="services-accordion-content">
                        <div class="services-accordion-body">
                            {ab_tests_section}
                        </div>
                    </div>
                </div>

                <!-- 13: Приоритизированные фиксы -->
                <div class="services-accordion-item">
                    <div class="services-accordion-header">
                        <span class="services-accordion-number">&nbsp;13</span>
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
        print("Использование: python3 generate_landing_html.py --json <file.json> [output_dir]")
        print("Агент должен выполнить анализ по научной методике и передать JSON.")
        sys.exit(1)

    url = sys.argv[1]
    json_data = None

    if url == "--json" and len(sys.argv) > 2:
        json_file = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else os.getcwd()
        print(f"Загрузка данных из JSON: {json_file}")
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        url = json_data.get("url", "unknown")
        icp_description = json_data.get("icp", "generic problem-aware audience")
        analysis = json_data.get("analysis", json_data)
    else:
        print("Ошибка: Используйте --json для передачи данных анализа.")
        print("Агент должен выполнить анализ по научной методике и передать JSON.")
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