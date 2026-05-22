/**
 * Market RU plugin for OpenCode.ai
 *
 * AI Marketing Suite - Russian version
 * Auto-registers skills directory via config hook.
 */

import path from 'path';
import fs from 'fs';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const extractAndStripFrontmatter = (content) => {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { frontmatter: {}, content };
  const frontmatterStr = match[1];
  const body = match[2];
  const frontmatter = {};
  for (const line of frontmatterStr.split('\n')) {
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0) {
      const key = line.slice(0, colonIdx).trim();
      const value = line.slice(colonIdx + 1).trim().replace(/^["']|["']$/g, '');
      frontmatter[key] = value;
    }
  }
  return { frontmatter, content: body };
};

export const MarketRuPlugin = async ({ client, directory }) => {
  const homeDir = os.homedir();
  const marketSkillsDir = path.resolve(__dirname, '../../skills');
  const envConfigDir = process.env.OPENCODE_CONFIG_DIR;
  const configDir = envConfigDir || path.join(homeDir, '.config/opencode');

  const getBootstrapContent = () => {
    const skillPath = path.join(marketSkillsDir, 'market-ru', 'SKILL.md');
    if (!fs.existsSync(skillPath)) return null;
    const fullContent = fs.readFileSync(skillPath, 'utf8');
    const { content } = extractAndStripFrontmatter(fullContent);
    return `<MARKET_RU_PLUGINS>
Маркетинговый плагин на русском языке активен.

**Доступные команды:**
- /market-ru audit <url> - Полный маркетинговый аудит
- /market-ru quick <url> - Быстрый анализ
- /market-ru copy <url> - Копирайтинг
- /market-ru seo <url> - SEO-аудит
- /market-ru competitors <url> - Конкурентный анализ
- /market-ru-landing <url> - CRO лендингов (через оркестратор)
- /market-ru-landing <url> - CRO лендингов (standalone)
- /market-ru funnel <url> - Анализ воронки
- /market-ru emails <topic> - Email-последовательности
- /market-ru social <topic> - Контент-календарь
- /market-ru ads <url> - Рекламные кампании
- /market-ru brand <url> - Анализ бренда
- /market-ru launch <product> - Playbook запуска
- /market-ru proposal <client> - Клиентское предложение
- /market-ru report <url> - Маркетинговый отчёт
- /market-ru report-pdf <url> - PDF-отчёт

${content}
</MARKET_RU_PLUGINS>`;
  };

  return {
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(marketSkillsDir)) {
        config.skills.paths.push(marketSkillsDir);
      }
    },
    'experimental.chat.messages.transform': async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (!bootstrap || !output.messages.length) return;
      const firstUser = output.messages.find(m => m.info.role === 'user');
      if (!firstUser || !firstUser.parts.length) return;
      if (firstUser.parts.some(p => p.type === 'text' && p.text.includes('MARKET_RU_PLUGINS'))) return;
      const ref = firstUser.parts[0];
      firstUser.parts.unshift({ ...ref, type: 'text', text: bootstrap });
    }
  };
};