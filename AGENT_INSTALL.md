# AGENT_INSTALL.md — Инструкция для AI-агента по установке скилла

## Общая информация

Этот файл содержит инструкции для AI-агента по установке `market-ru-landing` скилла.
Агент должен прочитать этот файл и выполнить установку **полностью автоматически**.

---

## Автоматическая установка (рекомендуется)

### Шаг 1: Определить платформу

Агент должен определить, работает ли он в **OpenCode** или **Claude Code**:

```python
import os
import subprocess

def detect_platform():
    # Claude Code detection
    if os.path.isdir(os.path.expanduser("~/.claude")):
        return "claude"

    # OpenCode detection
    opencode_config = os.path.expanduser("~/.config/opencode/opencode.json")
    if os.path.isfile(opencode_config):
        return "opencode"

    # Try command detection
    result = subprocess.run(["which", "claude"], capture_output=True)
    if result.returncode == 0:
        return "claude"

    result = subprocess.run(["which", "opencode"], capture_output=True)
    if result.returncode == 0:
        return "opencode"

    return "unknown"
```

### Шаг 2: Для обеих платформ — установить через npm

```bash
npm install -g market-ru-landing
```

### Шаг 3: Для OpenCode — автоматически добавить plugin в opencode.json

**КРИТИЧЕСКИ ВАЖНО:** Агент должен САМ модифицировать `opencode.json` после `npm install`.

```python
import json
import os
import subprocess

def install_for_opencode():
    # 1. Install npm package
    subprocess.run(["npm", "install", "-g", "market-ru-landing"], check=True)

    # 2. Find npm global root
    result = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True)
    npm_root = result.stdout.strip()
    skill_name = "market-ru-landing"
    plugin_path = os.path.join(npm_root, skill_name, ".opencode", "plugins", f"{skill_name}.js")

    # 3. Read opencode.json
    opencode_json_path = os.path.expanduser("~/.config/opencode/opencode.json")
    with open(opencode_json_path, "r") as f:
        config = json.load(f)

    # 4. Check if plugin already exists
    plugin_list = config.get("plugin", [])
    if plugin_path not in plugin_list:
        config["plugin"] = plugin_list + [plugin_path]

        # 5. Write back
        with open(opencode_json_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"Added plugin to opencode.json: {plugin_path}")
    else:
        print("Plugin already exists in opencode.json")

    return True
```

### Шаг 4: Для Claude Code — проверить установку

```python
def install_for_claude():
    # Use install.sh
    subprocess.run([
        "bash", "-c",
        "curl -fsSL https://raw.githubusercontent.com/Valdiss-Valdiss/ai-marketing-ru-landing/main/install.sh | bash"
    ], check=True)

    # Verify installation
    skill_path = os.path.expanduser(f"~/.claude/skills/{skill_name}/SKILL.md")
    return os.path.isfile(skill_path)
```

---

## Определение путей

| Платформа | npm global root | Skills directory | Plugin path |
|-----------|-----------------|------------------|-------------|
| OpenCode | `npm root -g` → `.../node_modules/market-ru-landing` | via plugin | `.../market-ru-landing/.opencode/plugins/market-ru-landing.js` |
| Claude Code | `npm root -g` | `~/.claude/skills/` | N/A |

---

## Проверка установки

После установки агент должен проверить:

1. **OpenCode:**
   - `npm list -g market-ru-landing` — пакет установлен
   - Plugin path добавлен в `~/.config/opencode/opencode.json`
   - Скилл доступен через `/market-ru-landing`

2. **Claude Code:**
   - Файл `~/.claude/skills/market-ru-landing/SKILL.md` существует
   - Команда `/market-ru-landing` доступна

---

## Python (обязательно для генерации отчётов)

Агент должен проверить доступность Python:

```python
def check_python():
    result = subprocess.run(["python3", "--version"], capture_output=True)
    if result.returncode == 0:
        return True  # Python доступен - используй скрипты
    return False  # Python недоступен - fallback режим
```

**Важно:**
- Если Python установлен → агент ОБЯЗАН использовать скрипты генерации отчётов
- Fallback-режим (без скриптов) только при отсутствии Python

---

## Ключевые замечания для агента

1. **НЕ ожидай ручных действий от пользователя** — агент делает ВСЁ сам
2. **Для OpenCode:** После `npm install -g` агент ОБЯЗАТЕЛЬНО должен модифицировать `opencode.json`
3. **Проверяй результат** каждого шага и сообщай пользователю об успехе/ошибке
4. **Путь к plugin:** `npm root -g` + `/market-ru-landing/.opencode/plugins/market-ru-landing.js`

---

## Удаление (если нужно)

### OpenCode:
1. `npm uninstall -g market-ru-landing`
2. Удалить plugin path из `opencode.json`

### Claude Code:
```bash
rm -rf ~/.claude/skills/market-ru-landing
rm -f ~/.claude/agents/market-ru-landing.md
```

---

## Отчёт после установки

После успешной установки агент должен сообщить:
- Платформа (OpenCode или Claude Code)
- Куда установлено (путь)
- Какие файлы скопированы
- Plugin добавлен в opencode.json (для OpenCode)
- Как проверить работоспособность