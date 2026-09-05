# SEO / AEO / GEO: запуск проекта с нуля до топа выдачи

*Переработка Playbook V2 (247 статей SearchEngineLand) в формат: целевая система → конкретные шаги. Все техники верифицируемы по URL из V2.*

---

## ЧАСТЬ I. КАК ДОЛЖНО РАБОТАТЬ (целевая модель системы)

### 1. Четыре канала видимости — кормим каждый отдельно

Система не «делает SEO». Она одновременно работает на четыре независимых рынка отбора:

| Канал | Механизм отбора | Что ест |
|---|---|---|
| Google organic | Краулинг → индекс → ранжирование page по запросу | Полная страница, CWV, links, freshness |
| ChatGPT instant (90% free) | Собственный индекс `labrador` | **Только title + ~200 символов после H1.** Страницу не открывает |
| ChatGPT thinking (paid) | Live opens через ChatGPT-User | Полную страницу (открытая цитируется в 74%, неоткрытая — 7%) |
| Perplexity / Gemini / AI Overviews | Свои корпуса, overlap 8–10% между движками | Пассажи + консенсус третьих сторон |

Следствие: один и тот же контент должен выживать в трёх форматах потребления — полный HTML, 200-символьный snippet, извлечённый пассаж. Всё остальное — вторично.

### 2. Единица контента — пассаж, не страница

- Median цитируемого AI Mode пассажа — 117 слов, многосоставный абзац.
- Один сильный пассаж цитировался 661 раз по 483 разным запросам.
- 85% цитируемых пассажей полностью самодостаточны — без «как сказано выше».
- 48% переиспользуемых пассажей начинаются с явного вопроса.

Следствие: страница = набор атомарных, самодостаточных пассажей. Каждый H2-блок — ответ, который можно вырезать и процитировать без потери смысла. Не нужна тонна thin pages — нужен один сильный параграф на кластер запросов.

### 3. Moat — только проприетарные данные

AI тривиально пересобирает generic-контент из чужих источников. Единственное, что модель вынуждена атрибутировать вам — то, чего нет ни у кого:

- собственные исследования и датасеты;
- названные индексы/фреймворки (бренд в названии — «X Index», «X Framework»);
- first-person опыт, lived details, цифры из своей практики.

### 4. Authority выбирается по третьим сторонам

- 85% бренд-упоминаний в AI — из third-party контента, не с вашего сайта.
- Корреляция brand mentions с AI Overview ≈ 0.664 vs 0.218 у backlinks.
- UGC-площадки (Reddit, YouTube, Quora, LinkedIn) — 17.1% цитируемых доменов, в 4× больше паблишеров.
- AI ищет консенсус: co-occurrence вашего бренда рядом с отраслевыми терминами.

Следствие: owned сайт задаёт messaging, но выбор AI делает по earned signals. Контент на сайте — необходимое условие, не достаточное.

### 5. Две петли работы

**Петля производства (weekly):**
prompt research → кластер → brief → outline (human gate) → draft → 3-агентная вычитка (editor / fact-checker / anti-AI-tells) → публикация → IndexNow.

**Петля измерения (weekly/monthly):**
money-query прогон по 3 движкам → GSC AI reports → striking-distance (позиции 5–20) → refresh-календарь → обновление → повторный прогон.

### 6. Конверсия: LLM-трафик ≠ search-трафик

LLM referral конвертирует в 20% (на 61% выше paid search). Но пользователь пришёл валидировать рекомендацию AI, а не заполнять форму. Landing для LLM-трафика: глубина, доказательства, нюансы — не stripped-down PPC-страница с агрессивным CTA.

### 7. Anti-slop — структурное требование

AI-текст имеет детектируемый шаблон (97% accuracy классификаторов). Google пенализирует не AI, а unoriginal content. Требование к каждому материалу: unique (точка зрения) + specific (конкретный случай) + authentic (first-hand).

---

## ЧАСТЬ II. ЧТО НАДО СДЕЛАТЬ (фазы от нуля)

### Фаза 0. Выбор поля — до домена (дни 1–7)

Цель: найти категорию, где можно стать owner.

- [ ] **Прогнать 20–30 buyer-промптов** через ChatGPT, Perplexity, Gemini: «лучшие X для Y», «как выбрать X», «X vs Z». Зафиксировать, кто цитируется и почему.
- [ ] **Проверить owner-статус категории**: только 15.2% категорий имеют владельца, 53.7% — открытое поле. Наибольший объём AI-спроса — в категориях без owner.
- [ ] **Keyword research параллельно с prompt research**: для каждого топика два числа — keyword volume (Google) и prompt volume (AI). Разрыв определяет формат: keyword-strong → SEO-страница; prompt-strong → AI-цитируемый контент; strong-both → флагманский pillar.
- [ ] **Query fan-out**: 40+ подзапросов на топик. Tier 1 = H2, Tier 2 = подзаголовки.
- [ ] **Reddit mining как keyword-источник**: реальные формулировки клиентов («какая коляска проходит через турникет метро», а не «рама 49 см»).
- [ ] **Entity-решение**: имя бренда, 1–3 core associations («size-inclusive activewear for new moms», не «high quality»), домен.

**Выход фазы:** topical map (кластеры × подзапросы) + список цитируемых конкурентов + brand associations.

### Фаза 1. Технический фундамент (недели 1–2)

Цель: сайт полностью читаем всеми AI-краулерами. Без этого весь остальной контент невидим.

- [ ] **SSR — весь критичный контент в исходном HTML.** AI-боты не исполняют JS. Next.js — SSR/SSG по умолчанию, никакого CSR на money-страницах.
- [ ] **Все внутренние ссылки в raw HTML.** Эксперимент 41 день: GPTBot, ClaudeBot, PerplexityBot нашли 0 JS-injected страниц. Восстановление после фикса медленное.
- [ ] **Размер страницы < 4 MB** — превышение = полный отказ модели (HTTP 400), не обрезка.
- [ ] **robots.txt**: GPTBot, ClaudeBot, PerplexityBot, Claude-SearchBot, OAI-SearchBot — разрешены. Проверить устаревшие блоки.
- [ ] **robots.txt + noindex не конфликтуют**: noindex должен быть виден краулеру (Anthropic ошиблась — Google проиндексировал приватные чаты Claude).
- [ ] **Sitemap.xml** — backup-канал дискавери. + **IndexNow** для мгновенной сигнализации об обновлениях.
- [ ] **Bing Webmaster Tools — обязательная индексация.** ChatGPT web search опирается на Bing-корпус; `labrador` — отдельный индекс OpenAI, нужны оба.
- [ ] **Canonical domain audit**: один домен, 301 с вариантов, консистентный NAP. Split identity = AI не может определить доверенный источник.
- [ ] **Schema JSON-LD в server-side HTML**: Organization (homepage, `sameAs` → LinkedIn, Wikidata), Article (author, dates), BreadcrumbList, FAQPage. JSON-LD стрипается при Markdown-конверсии — дублировать ключевые факты в alt и видимый текст.
- [ ] **Core Web Vitals**: WebP/AVIF, lazy loading below-fold, удаление неиспользуемого JS.
- [ ] **Верификация**: GSC + Bing + IndexNow key. GSC AI performance reports включены (с июня 2026).

**Выход фазы:** 100% страниц читаемы как raw HTML, индексируемы Bing, < 4 MB, schema валидна.

### Фаза 2. Архитектура контента (недели 2–4)

Цель: каждая страница спроектирована под извлечение пассажей.

- [ ] **Topic clusters**: 1 pillar + 3–5 кластерных страниц. Topical authority — сильнейший предиктор AI-цитирования (r=0.41), сильнее DA и backlinks.
- [ ] **Карта покрытия**: все entities класса × все attributes × все query templates («how to X», «best X for Y», «X vs Y»). Authority прикрепляется к query format (WikiHow-эффект).
- [ ] **Шаблон страницы (жёсткий)**:
  - H1 → **первые 200 символов = ключевая мысль** (grounding-бюджет ChatGPT instant; никаких дат, breadcrumbs, оглавлений между H1 и сутью);
  - H2 = вопрос (48% переиспользуемых пассажей начинаются с вопроса);
  - ответ 40–60 слов в первых строках блока (80% цитируемых пассажей — ответ в первом предложении);
  - сущность названа явно в пассаже («X работает для Y», не «оно работает»);
  - **claim first → evidence second**;
  - HTML-таблицы для сравнений (цитируются в AI Overviews чаще любого формата);
  - детали после ответа.
- [ ] **Page independence test** перед каждой новой страницей: GSC-проверка на каннибализацию + SERP overlap top-10 обоих запросов. Overlap высокий → расширять существующую.
- [ ] **Двусторонние внутренние ссылки** внутри кластера, описательные anchor'ы.
- [ ] **LLM-landing ≠ PPC-landing**: для страниц, принимающих AI-трафик — глубина и верификация, не aggressive CTA.

**Выход фазы:** шаблон-контракт страницы + кластерная карта + внутренний линкграф.

### Фаза 3. Производство контента (недели 3–10)

Цель: 10–15 материалов первого кластера + 1 proprietary asset.

- [ ] **Три трека**:
  - Commodity (глоссарии, FAQ) — AI-генерация + human QA;
  - Hybrid (сравнения, гайды) — AI draft + обязательная human-редактура;
  - Expertise (исследования, кейсы) — эксперт пишет, AI ассистирует.
- [ ] **Proprietary asset #1**: исследование/датасет/индекс **с брендом в названии** («[Brand] Index 2026»). AI вынужден атрибутировать named-исследование. В тексте: «[Brand] Study показала, что 40%…» — привязка бренда к факту в самом предложении (анти-ghost-citation: 40% цитат не называют бренд).
- [ ] **Pipeline с гейтами**: brief → strategist-агент (Pass/Revise/Kill) → outline → **human gate** → draft → 3 раздельных агента (Editor, adversarial Fact-checker, anti-AI-tells) → human → публикация. Максимум 2 круга ревизий, дальше эскалация.
- [ ] **E-E-A-T**: named-автор с верифицируемыми credentials, byline-страница, «Last updated» на каждой странице (76.4% top-cited страниц ChatGPT обновлены за 30 дней).
- [ ] **Anti-slop-контроль**: varying structure между материалами, минимум один lived detail / first-person факт на страницу, никаких шаблонных морализаторских концовок.
- [ ] **/en/ folder** для cornerstone-страниц, если основной язык не английский: ChatGPT-User берёт /en/ версию в 65–79% случаев (over-indexing 2.6×) — один из немногих content-side hacks расширения AI footprint.
- [ ] **Expert quotes**: 2–3 цитаты признанных экспертов на pillar-материал.

**Выход фазы:** первый полный кластер live + proprietary asset опубликован.

### Фаза 4. Third-party footprint (недели 4–12, затем постоянно)

Цель: earned signals — 85% того, что решает AI.

- [ ] **Reddit**: определить 3–5 субреддитов (критерии: relevance, ваши ответы уместны, активность, правила, value без промо). Нативное участие с disclosure аффиляции. Кейс Kumon: 5 месяцев → ChatGPT visibility с 5% до 18%.
- [ ] **YouTube**: long-form сравнения/туториалы/честные обзоры — 94% AI-цитируемых видео long-form; 40% имеют <1,000 views (мид-сайз нишевые каналы побеждают мега-инфлюенсеров).
- [ ] **Founder-led PR**: подкасты, co-marketing, комьюнити — создаёт entity association, который AI кодирует как факт.
- [ ] **Отзывы на агрегаторах**: G2, Capterra, Trustpilot (B2B). Нет в правильной категории Gartner → исключены из vendor shortlist в AI-ответах.
- [ ] **BOFU-сравнения на своём сайте**: «[Мы] vs [Конкурент]», «Альтернативы [Конкуренту]» — narrative control.
- [ ] **Social topical map**: каждой SEO-категории — соответствующий social-stream. Social контент индексируется и попадает в AI Overview source panels.
- [ ] **НЕ делать**: покупку ссылок, PBN, «LLM visibility campaigns» от бывших линкбилдеров (те же paid mentions на low-quality сайтах — AI их фильтрует), AI-спам Reddit (23M blocked spam views).
- [ ] **Linkable assets**: бесплатный инструмент / шаблон / статистика → пассивное привлечение ссылок → внутренние ссылки с asset на commercial страницы.

**Выход фазы:** присутствие на 5+ third-party площадках, первые earned mentions.

### Фаза 5. Измерение (с недели 0, непрерывный цикл)

Цель: решения по данным, не по ощущениям.

- [ ] **56-дневный GSC baseline** зафиксировать ДО любых изменений (достаточно узко для сезона, достаточно надёжно).
- [ ] **Money-query set**: 15–20 промптов, которые покупатели задают перед покупкой. Еженедельный автоматический прогон через ChatGPT, Perplexity, Gemini (91% цитат появляются только в одном движке — мониторинг одного = misleading; каждый движок — отдельный замер, 3–5 повторов из-за grounding drift ~60%).
- [ ] **Трекать 4 категории, не одну метрику**: cited+mentioned / cited-only (ghost) / mentioned-only / neither. Position, sentiment, citations URL.
- [ ] **GA4**: фильтр AI-referrer (chat.openai.com, perplexity.ai, google.com AI Mode) → session-scoped; custom dimension на `#:~:text=` фрагмент (самый надёжный маркер AI Overview трафика). Помнить: 22.4% AI Overview сессий атрибутируются как Direct.
- [ ] **Server logs**: UA ChatGPT-User — thinking-mode opens не несут utm_source, в GA4 их нет. Скрейп ≠ клик (Clarity Scrape-to-Referral ratio).
- [ ] **GSC AI performance reports** — impressions в AI Overviews / AI Mode по страницам.
- [ ] **Striking-distance workflow (monthly)**: запросы позиций 5–20 с impressions → приоритет обновления. Тегирование секций Keep/Fix/Remove/Add. Факт-чек всех цифр. **Никогда не менять** работающий URL slug / meta title / схему — расширять.
- [ ] **Prompt mapping по funnel**: visibility по стадиям (discovery / comparison / branded) — «70% в branded, 10% в discovery» информативнее общего score.
- [ ] **Branded demand как dark-funnel proxy**: рост branded clicks в GSC, совпадающий с ростом AI visibility.
- [ ] **GSC Platform properties**: верифицировать YouTube/TikTok/Instagram аккаунты — first-party данные по кликам с social.

**Выход фазы:** автоматический weekly-дашборд (prompt-прогоны + GSC + GA4) и monthly refresh-календарь.

### Фаза 6. Local + Images + Agents (если применимо к модели бизнеса)

- [ ] **Local**: GBP с specific primary category (+36% top-10 presence vs generic), completeness 5/5 (avg rank лучше на ~19 позиций, top-10 rate ×3), адрес через Geocoding API, products/inventory в GBP. Hub-and-spoke гео-страницы — не по странице на каждый город.
- [ ] **Images**: оригинальные (не сток), OCR-читаемые упаковки/тексты, alt с фактом из инфографики — image = doorway для visual search (20B Google Lens searches/month; патент Google: image-first matching источника).
- [ ] **Accessibility tree**: money pages читаемы через ARIA (AI-агенты читают accessibility tree, не DOM) — agent readiness audit; ARIA-снапшоты в CI против регрессий шаблонов.
- [ ] **MCP + agents**: Semrush/Ahrefs/GSC MCP-серверы для research-цепочек; MCP-эндпоинт вашего сервиса, если продукт — инструмент (готовность к agentic-буду, где AI-агенты покупают напрямую).

---

## ЧАСТЬ III. СИСТЕМА ЭКСПЛУАТАЦИИ (как работает без ручного управления)

### Сквозная автоматизация (что должно работать само через месяц)

1. **Prompt-runner cron (weekly)**: скрипт гоняет money-query set по ChatGPT API + Perplexity API + Gemini API, парсит позиции/упоминания/цитаты, пишет в GSheet/дашборд. API ≠ продукт ChatGPT (Jaccard 0.23–0.27) — поэтому ежеквартально ручной прогон через сами продукты для калибровки.
2. **GSC + GA4 collector (weekly)**: AI reports, striking-distance экспорт, branded clicks → единый дашборд.
3. **Refresh-календарь (monthly)**: 76.4% top-cited обновлены за 30 дней — каждый материал имеет дату refresh; cron напоминает о материалах старше 30 дней на money-позициях.
4. **Trend-monitor (weekly)**: emerging categories мониторить по proper nouns (regulations, ISO standards, job titles) — buyer-вопросы emerging categories не имеют search volume, но formal vocabulary растёт 30–90× за год. Публикация на стадии роста, не пика.
5. **CI-гейты**: на каждый деплой — проверка «контент в raw HTML», ARIA-снапшот diff, размер страницы < 4 MB, ссылки не JS-injected.

### Критерии успеха (по слоям)

| Слой | Метрика | Горизонт |
|---|---|---|
| AI access | Краул GPTBot/ChatGPT-User в логах | месяц 1–2 |
| AI visibility | Mention rate в money-query set, 3 движка | месяц 2–4 |
| AI referral | GA4 AI-sessions + `#:~:text=` | месяц 3–6 |
| Dark funnel | Branded clicks GSC ↑ | месяц 3–6 |
| Pipeline | AI-referred конверсии (базовая ставка: 20%) | месяц 6+ |

### Три правила приоритизации

1. **Технический фундамент раньше контента** — JS-only страница = пустая страница для AI, сколько ни вкладывай в текст.
2. **Proprietary data раньше объёма** — 10 generic статей проигрывают одному named-исследованию.
3. **Third-party раньше линкбилдинга** — mentions (r=0.664) > backlinks (r=0.218); покупные mentions AI фильтрует.

---

*Blueprint построен на Playbook V2 (140+ техник, 97 статей, все с верифицируемыми URL). Уровень уверенности: высокий по всем количественным утверждениям — цифры из опубликованных исследований, ссылки в V2.*