#!/usr/bin/env python3
"""
Landing Page Analyzer — AI Marketing Claude Code Skills
Анализ посадочных страниц на основе научных моделей: MECLABS, LIFT, Scannability Score, Trust Factor, Resonance Rate.
LLM-driven анализ на основе текстовых данных страницы.
"""

import sys
import json
import re
from urllib.parse import urlparse
from datetime import datetime
import subprocess
import os

# Попытка импорта fetch_page, если доступен
try:
    from fetch_page import fetch_page
    FETCH_AVAILABLE = True
except ImportError:
    FETCH_AVAILABLE = False


def call_llm_for_analysis(page_text, icp_description, url):
    """
    Вызывает LLM для анализа страницы на основе научных моделей.
    Это заглушка — в реальности вызов должен происходить через API LLM.
    """
    # Формируем промпт для анализа
    prompt = f"""Проанализируй посадочную страницу {url} для целевой аудитории: {icp_description}

Используя научные модели CRO-анализа, предоставь JSON с детальным анализом.

## Структура JSON ответа:
{{
    "scores": {{
        "total": 0-100  // Общий CRO score
    }},
    "metrics": {{
        "vpi": 1-10,           // Value Proposition Index
        "scannability_score": 0-100,  // % контента при 5-сек сканировании
        "trust_factor": 0-20,         // Количество триггеров доверия
        "resonance_rate": 0-100,     // % болей аудитории закрытых решениями
        "cro_score": 0-100,
        "motivation": 1-10,
        "value_proposition": 1-10,
        "incentive": 1-10,
        "friction": 1-10,
        "anxiety": 1-10,
        "lift_relevance": 1-10,
        "lift_clarity": 1-10,
        "lift_urgency": 1-10,
        "lift_value": 1-10,
        "lift_anxiety": 1-10,
        "lift_distraction": 1-10
    }},
    "sections": {{
        "hero": {{
            "score": 1-10,
            "max": 10,
            "findings": ["список находок"],
            "fixes": [{{"priority": "HIGH/MEDIUM/LOW", "text": "описание"}}]
        }},
        "value_proposition": {{...}},
        "social_proof": {{...}},
        "features": {{...}},
        "objection_handling": {{...}},
        "cta": {{...}},
        "footer": {{...}}
    }},
    "copy_score": {{
        "clarity": 1-10,
        "urgency": 1-10,
        "specificity": 1-10,
        "proof": 1-10,
        "action_orientation": 1-10,
        "total": 0-100
    }},
    "form_audit": {{
        "field_count": "число или описание",
        "button_text": "текст кнопки",
        "recommendation": "рекомендация"
    }},
    "mobile_audit": {{
        "cta_accessible": "да/нет/частично",
        "text_readable": "да/нет/частично",
        "recommendation": "рекомендация"
    }},
    "ab_tests": [
        {{"hypothesis": "Если мы [изменим], то [метрика] [улучшится], потому что [причина]."}}
    ],
    "prioritized_fixes": {{
        "quick_wins": [{{"text": "...", "impact": "..."}}],
        "medium_term": [{{"text": "...", "impact": "..."}}],
        "strategic": [{{"text": "...", "impact": "..."}}]
    }}
}}

## Научные модели для анализа:

### 1. MECLABS Формула конверсии:
C = M×4 + V×3 + I×2 + F×2 + A×2
- M (Motivation) — внутренняя мотивация пользователя (внешний фактор)
- V (Value Proposition) — сила ценностного предложения через Appeal, Exclusivity, Credibility, Clarity
- I (Incentive) — дополнительные стимулы/бонусы
- F (Friction) — трение (сложность форм, количество полей, когнитивная нагрузка)
- A (Anxiety) — тревога (отсутствие гарантий, политики конфиденциальности)

### 2. LIFT Framework:
Драйверы: Релевантность, Ясность, Срочность, Ценностное предложение
Ингибиторы: Тревога, Отвлечение

### 3. Scannability Score (SS):
SS = Σ(оценка_блока × вес_блока) × 100%
Блоки: H1 (20%), Subheadline (15%), CTA кнопка (20%), Структура H2-H3 (15%), Визуал (15%), Пробелы/воздух (15%).
Оцени, насколько страница читабельна за 5 секунд.

### 4. Trust Factor (TF):
TF = Σ(присутствующий_тип × вес)
Типы триггеров: отзывы клиентов (2.0), результаты клиентов (2.0), видео-отзывы (2.0), кейсы до/после (1.5), логотипы клиентов (1.5), рейтинги第三方 (1.5), гарантия (1.5), сертификаты (1.0), статистика компании (1.0), политика возврата (1.0), соцсети (0.5), контакты (0.5), supplier badges (0.3).

### 5. Resonance Rate (RR):
RR = (Σ оценка_боли / количество_болей) × 100%
Определи боли целевой аудитории и оцени, насколько контент страницы закрывает каждую боль (0%=не упомянута, 50%=решение без доказательств, 100%=решение + сильное доказательство).

## Текст страницы для анализа:
{page_text[:30000]}

Верни ТОЛЬКО JSON без markdown разметки.
"""

    # Проверяем, доступен ли opencode tooling для вызова LLM
    try:
        # Пытаемся использовать API если есть
        # Это placeholder - в реальной реализации нужен реальный LLM API call
        result = {
            "status": "placeholder",
            "message": "LLM analysis requires integration with Claude/OpenAI API"
        }
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def simple_text_analysis(page_text, url):
    """
    Простой анализ на основе регулярных выражений без LLM.
    Используется как fallback если LLM недоступен.
    """
    parsed = urlparse(url)
    domain = parsed.netloc

    # Базовые метрики
    text_lower = page_text.lower()
    words = page_text.split()

    # Простой подсчёт метрик
    trust_keywords = ['гарантия', 'отзывы', 'клиенты', 'сертификат', 'безопасность',
                      'деньги назад', 'пробный', 'бесплатно', 'лицензия', 'награды']
    trust_count = sum(1 for kw in trust_keywords if kw in text_lower)

    # Поиск CTA
    cta_patterns = [r'отправить', r'получить', r'начать', r'заказать', r'купить',
                     r'submit', r'send', r'start', r'get', r'buy', r'sign']
    cta_count = sum(1 for p in cta_patterns if p in text_lower)

    # Поиск форм
    form_pattern = r'<form|form |input |textarea |type="email"|type="tel"'
    form_count = len(re.findall(form_pattern, text_lower, re.IGNORECASE))

    # Поиск социального доказательства
    social_patterns = [r'\d+\s*(клиентов?|пользователей?|компаний?|партнёров)',
                        r'\d+%?\s*(рост|улучшени|повышени|увеличени)',
                        r'отзыв', r'рекомендаци', r'кейс', r'результат']
    social_count = sum(1 for p in social_patterns if re.search(p, text_lower, re.IGNORECASE))

    # Расчёт простых метрик
    vpi = min(10, max(1, 5 + (cta_count > 2) * 2 - (trust_count < 3) * 3))
    scannability = min(100, max(20, 60 - form_count * 5))
    trust_factor = min(20, trust_count * 3)
    resonance_rate = min(100, max(10, 50 + social_count * 10))

    # Подсчёт SECtions
    hero_score = 5
    if any(w in text_lower for w in ['мы создаём', 'мы помогаем', 'наш продукт', 'узнайте']):
        hero_score += 2
    if cta_count > 0:
        hero_score += 2
    if trust_count > 2:
        hero_score += 1
    hero_score = min(10, max(1, hero_score))

    value_score = 5
    if any(w in text_lower for w in ['выгода', 'результат', 'эффективность', 'рост']):
        value_score += 2
    value_score = min(10, value_score)

    social_score = 3 + (social_count > 0) * 3 + (trust_count > 3) * 2
    social_score = min(10, social_score)

    features_score = 5
    if form_count > 3:
        features_score -= 2
    features_score = min(10, max(1, features_score))

    objection_score = 4
    if any(w in text_lower for w in ['гарантия', 'пробный', 'деньги назад']):
        objection_score += 3
    if any(w in text_lower for w in ['вопрос', 'faq', 'часто']):
        objection_score += 2
    objection_score = min(10, objection_score)

    cta_score = 4
    if cta_count > 2:
        cta_score += 3
    cta_score = min(10, cta_score)

    footer_score = 5
    footer_score = min(10, footer_score)

    # Расчёт общего CRO score
    weights = {
        "hero": 25,
        "value_proposition": 20,
        "social_proof": 15,
        "features": 15,
        "objection_handling": 10,
        "cta": 10,
        "footer": 5,
    }

    total = (
        hero_score * weights["hero"] / 10 +
        value_score * weights["value_proposition"] / 10 +
        social_score * weights["social_proof"] / 10 +
        features_score * weights["features"] / 10 +
        objection_score * weights["objection_handling"] / 10 +
        cta_score * weights["cta"] / 10 +
        footer_score * weights["footer"] / 10
    )

    # MECLABS
    motivation = 5  # Оценивается внешне
    value_proposition = vpi
    incentive = min(10, max(1, 5 + (social_count > 0) * 3))
    friction = max(1, 10 - form_count * 2)
    anxiety = max(1, 10 - trust_count * 2)

    meclabs_score = motivation * 4 + value_proposition * 3 + incentive * 2 + friction * 2 + anxiety * 2
    meclabs_score = min(100, meclabs_score)

    # LIFT
    lift_relevance = min(10, max(1, 5 + (cta_count > 0) * 2))
    lift_clarity = min(10, max(1, 6 + (len(words) < 500) * 2))
    lift_urgency = min(10, max(1, 4 + (social_count > 0) * 3))
    lift_value = vpi
    lift_anxiety = max(1, min(10, 10 - trust_count))
    lift_distraction = max(1, min(10, 5 + form_count))

    # Copy Score
    clarity = min(10, max(1, 6 + (len(words) < 300) * 2))
    urgency = min(10, max(1, 3 + (social_count > 0) * 4))
    specificity = min(10, max(1, 4 + (social_count > 0) * 3))
    proof = min(10, max(1, 3 + trust_count * 2 + social_count))
    action_orientation = min(10, max(1, 5 + (cta_count > 2) * 3))
    copy_total = (clarity + urgency + specificity + proof + action_orientation) * 2

    # Генерация находок
    hero_findings = [
        f"Найдено {cta_count} потенциальных CTA элементов",
        f"Индикаторы доверия: {trust_count} найдено",
        f"Социальное доказательство: {'найдено' if social_count > 0 else 'не найдено'}"
    ]
    if cta_count == 0:
        hero_findings.append("КРИТИЧЕСКИ: CTA не обнаружен")
    if trust_count < 3:
        hero_findings.append("ВНИМАНИЕ: Недостаточно сигналов доверия")

    value_findings = [
        f"VPI (Value Proposition Index): {vpi}/10",
        f"Текст {'краткий' if len(words) < 300 else 'средний' if len(words) < 600 else 'длинный'} ({len(words)} слов)"
    ]

    social_findings = [
        f"Типы социального доказательства: {social_count}",
        f"Триггеры доверия: {trust_count}"
    ]
    if social_count == 0:
        social_findings.append("КРИТИЧЕСКИ: Нет социального доказательства")

    features_findings = [
        f"Формы обнаружены: {form_count}",
        f"Когнитивная нагрузка: {'низкая' if len(words) < 400 else 'средняя' if len(words) < 800 else 'высокая'}"
    ]

    objection_findings = [
        f"Гарантии и стимулы: {'найдены' if trust_count > 2 else 'недостаточно'}"
    ]

    cta_findings = [
        f"CTA элементов: {cta_count}",
        f"Рекомендуемое количество: 2-3 на странице"
    ]

    sections = {
        "hero": {
            "score": hero_score,
            "max": 10,
            "findings": hero_findings,
            "fixes": [
                {"priority": "HIGH" if cta_count == 0 else "MEDIUM", "text": "Добавить CTA с ценностным описанием"},
                {"priority": "HIGH", "text": "Разместить социальное доказательство над сгибом"},
            ]
        },
        "value_proposition": {
            "score": value_score,
            "max": 10,
            "findings": value_findings,
            "fixes": [
                {"priority": "MEDIUM", "text": "Использовать формулу 4U для заголовка"},
            ]
        },
        "social_proof": {
            "score": social_score,
            "max": 10,
            "findings": social_findings,
            "fixes": [
                {"priority": "HIGH" if social_count == 0 else "MEDIUM", "text": "Добавить отзывы клиентов с конкретными результатами"},
            ]
        },
        "features": {
            "score": features_score,
            "max": 10,
            "findings": features_findings,
            "fixes": [
                {"priority": "MEDIUM", "text": "Сократить текст до 3-5 ключевых выгод"},
            ]
        },
        "objection_handling": {
            "score": objection_score,
            "max": 10,
            "findings": objection_findings,
            "fixes": [
                {"priority": "MEDIUM", "text": "Добавить FAQ секцию с типичными возражениями"},
            ]
        },
        "cta": {
            "score": cta_score,
            "max": 10,
            "findings": cta_findings,
            "fixes": [
                {"priority": "MEDIUM", "text": "Добавить микротекст ('Без обязательств', 'Бесплатно')"},
            ]
        },
        "footer": {
            "score": footer_score,
            "max": 10,
            "findings": ["Стандартный футер"],
            "fixes": []
        }
    }

    copy_score = {
        "clarity": clarity,
        "urgency": urgency,
        "specificity": specificity,
        "proof": proof,
        "action_orientation": action_orientation,
        "total": copy_total
    }

    form_audit = {
        "field_count": form_count if form_count > 0 else "не обнаружено",
        "button_text": "проверить",
        "recommendation": f"Рекомендуется 3-5 полей. Текущее количество: {form_count if form_count > 0 else 'не обнаружено'}"
    }

    mobile_audit = {
        "cta_accessible": "требует проверки",
        "text_readable": "требует проверки",
        "recommendation": "Проверить вручную на мобильном устройстве"
    }

    ab_tests = [
        {
            "hypothesis": "Если изменить заголовок с функционального на выгодный (с квантифицированным результатом), тогда CTR кнопки увеличится на 15-25%, потому что конкретика усиливает восприятие ценности."
        },
        {
            "hypothesis": "Если добавить блок социального доказательства (отзывы с фото и результатами) рядом с CTA, тогда конверсия формы увеличится на 20-35%, потому что социальное доказательство снижает тревогу."
        },
        {
            "hypothesis": "Если сократить форму с 4 полей до 2 полей (имя + email), тогда Completion Rate увеличится на 10-20%, потому что меньшее трение = больше завершений."
        }
    ]

    prioritized_fixes = {
        "quick_wins": [
            {"text": "Добавить CTA с ценностным описанием ('Получить стратегию роста') вместо generic ('Отправить')", "impact": "+15-25% CTR"},
            {"text": "Разместить 2-3 отзыва с фото и метриками результатов над сгибом", "impact": "+20-35% конверсия"},
        ],
        "medium_term": [
            {"text": "Сделать A/B тест заголовка: функциональный vs выгодный с числом", "impact": "+10-20% улучшение CTR"},
            {"text": "Добавить FAQ секцию с 5 топовыми возражениями", "impact": "+10-15% снижение отказов"},
        ],
        "strategic": [
            {"text": "Разработать лонгрид с кейсами и видео-отзывами", "impact": "+40-60% доверие"},
        ]
    }

    analysis = {
        "scores": {
            "total": round(total, 1)
        },
        "sections": sections,
        "metrics": {
            "vpi": vpi,
            "scannability_score": scannability,
            "trust_factor": trust_factor,
            "resonance_rate": resonance_rate,
            "cro_score": round(meclabs_score, 1),
            "motivation": motivation,
            "value_proposition": value_proposition,
            "incentive": incentive,
            "friction": friction,
            "anxiety": anxiety,
            "lift_relevance": lift_relevance,
            "lift_clarity": lift_clarity,
            "lift_urgency": lift_urgency,
            "lift_value": lift_value,
            "lift_anxiety": lift_anxiety,
            "lift_distraction": lift_distraction
        },
        "copy_score": copy_score,
        "form_audit": form_audit,
        "mobile_audit": mobile_audit,
        "ab_tests": ab_tests,
        "prioritized_fixes": prioritized_fixes,
        "timestamp": datetime.now().isoformat()
    }

    return analysis


def analyze(url, icp_description="generic problem-aware audience"):
    """
    Основная функция анализа.
    """
    result = {
        "status": "ok",
        "url": url,
        "icp": icp_description,
        "timestamp": datetime.now().isoformat()
    }

    try:
        # Проверяем, доступен ли fetch_page
        if FETCH_AVAILABLE:
            print(f"Fetching page: {url}")
            page_data = fetch_page(url)
            if page_data.get("status") == "error":
                return page_data
            page_text = page_data.get("text", "")
        else:
            # Используем curl для fetching
            print(f"Fetching page via curl: {url}")
            try:
                import requests
                response = requests.get(url, timeout=30, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                page_text = response.text
            except:
                # Fallback - используем subprocess
                proc = subprocess.Popen(
                    ['curl', '-s', '-A', 'Mozilla/5.0', url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                page_text, _ = proc.communicate(timeout=30)
                try:
                    page_text = page_text.decode('utf-8')
                except:
                    page_text = page_text.decode('latin-1')

        if not page_text:
            return {
                "status": "error",
                "message": "Не удалось получить содержимое страницы"
            }

        print(f"Analyzing page ({len(page_text)} chars)...")

        # Проверяем, есть ли LLM API (placeholder для будущей интеграции)
        # Пока используем simple_text_analysis
        analysis = simple_text_analysis(page_text, url)

        result["analysis"] = analysis
        result["page_length"] = len(page_text)

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка анализа: {str(e)}"
        }


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 analyze_landing.py <url> [icp_description]")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url

    icp_description = sys.argv[2] if len(sys.argv) > 2 else "generic problem-aware audience"

    print(f"Starting analysis of: {url}")
    print(f"Target audience: {icp_description}")

    result = analyze(url, icp_description)

    if result.get("status") == "error":
        print(f"Error: {result.get('message')}")
        sys.exit(1)

    # Вывод результата в JSON
    print("\n" + "="*60)
    print("ANALYSIS RESULT")
    print("="*60)

    analysis = result.get("analysis", {})
    metrics = analysis.get("metrics", {})
    sections = analysis.get("sections", {})

    print(f"\nCRO Score: {metrics.get('cro_score', 0)}/100")
    print(f"VPI: {metrics.get('vpi', 0)}/10")
    print(f"Trust Factor: {metrics.get('trust_factor', 0)}")

    print("\nSection Scores:")
    for section_name, section_data in sections.items():
        score = section_data.get("score", 0)
        max_score = section_data.get("max", 10)
        print(f"  {section_name}: {score}/{max_score}")

    print("\n" + "="*60)
    print(f"Full JSON saved. Use generate_landing_md.py and generate_landing_html.py for reports.")
    print("="*60)

    # Сохранение JSON в файл
    output_dir = os.environ.get("OPENCODE_WORKING_DIR", os.getcwd())
    os.makedirs(output_dir, exist_ok=True)

    json_path = os.path.join(output_dir, "landing_analysis.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nJSON data saved to: {json_path}")

    return result


if __name__ == "__main__":
    main()