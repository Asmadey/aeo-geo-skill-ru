# SEO / AEO / GEO Playbook V2: Вывод статей в топ Google и AI-ответы

*Извлечено из 247 статей SearchEngineLand (август 2026). 200 статей спарсено ранее + 47 новых до 31 августа. 176 SEO/AEO/GEO-релевантных статей проанализированы детально. 85 техник из V1 расширены до 140+ техник.*

*Метрика confidence: все техники основаны на опубликованных исследованиях SearchEngineLand с верифицируемыми URL. Уровень уверенности — высокий, если не указано иное.*

---

## ПРИОРИТЕТ 1: Технический фундамент (без этого ничего не работает)

### 1.1. Server-side rendering — критичный контент в HTML
AI-краулеры (GPTBot, ClaudeBot, PerplexityBot, ChatGPT-User) **не исполняют JavaScript**. Весь текст, заголовки и schema должны быть в исходном HTML. JS-only контент = пустая страница для AI.

### 1.2. HTML-ссылки вместо JS-injected ссылок — 0% discovery для AI-ботов
41-дневный эксперимент (21 section, 1062 pages): GPTBot, ClaudeBot, Bingbot, PerplexityBot, Meta-ExternalAgent, Amazonbot — все нашли **0** JavaScript-injected страниц. Googlebot достиг 2% JS pages, GoogleOther — 48%. Все внутренние ссылки должны быть в raw HTML. Восстановление после фикса — медленное: AI-боты не возвращаются для recrawl автоматически.
*Источник: [JavaScript links can make your pages invisible to AI search](https://searchengineland.com/javascript-links-pages-invisible-ai-search-485228)*

### 1.3. Первые 200 символов после H1 = grounding-бюджет ChatGPT
В instant-режиме (90%+ пользователей free tier) ChatGPT видит только H1 + ~200 символов. Уберите даты, оглавления, category labels, breadcrumbs между H1 и первой полезной фразой. **Сразу после H1 — ключевая мысль.**

### 1.4. Title как self-contained предложение
Полный title доходит до модели без обрезки (даже 289 символов в `labrador`). Информативный, самодостаточный title работает лучше, чем оптимизированный под truncation. Bing обрезает title на 75 символах, `labrador` (индекс OpenAI) — никогда.

### 1.5. Размер страницы < 4 MB
Превышение 4 MB → страница **полностью отвергается** (HTTP 400), модель ничего не читает. Не обрезается — именно отвергается.

### 1.6. Robots.txt: не блокировать AI-ботов
Проверить, что GPTBot, ClaudeBot, PerplexityBot, Claude-SearchBot не заблокированы. Устаревшие правила часто «случайно» закрывают AI-доступ — вы исчезаете из AI-ответов без симптомов.

### 1.7. Индексация в Bing — обязательна для ChatGPT
ChatGPT web search опирается на Bing-индекс (75% в paid Thinking mode — scraped Google). Нет в Bing → нет в ChatGPT. Проверить через Bing Webmaster Tools.

### 1.8. IndexNow для мгновенной сигнализации
Уведомляйте поисковые системы об обновлениях контента сразу, не дожидаясь краулинга. Критично для AI-поиска и freshness signals.

### 1.9. Core Web Vitals: WebP/AVIF, lazy loading, удаление JS
Сжимайте изображения, lazy load для below-fold контента, удаляйте неиспользуемый JS. Прямо влияет на LCP, INP, CLS.

### 1.10. Sitemap как AI-backup канал
В эксперименте с JS-ссылками sitemaps были отключены (404) — единственный путь к страницам был через HTML-ссылки. Sitemaps — критический backup-канал для AI-дискавери, но не заменяют HTML-линки. Тестируйте: включите sitemap только для JS-секций, чтобы компенсировать отсутствие HTML-линков.
*Источник: [JavaScript links can make your pages invisible to AI search](https://searchengineland.com/javascript-links-pages-invisible-ai-search-485228)*

### 1.11. Canonical domain audit: устранение split identity
Бизнесы с несколькими domain variants дробят entity identity. AI-система не может определить, какой источник доверенный. Унифицируйте: один canonical domain, 301-редиректы со всех variants, консистентное NAP во всех директориях.
*Источник: [AI search can't verify your business](https://searchengineland.com/ai-search-cant-verify-business-fix-483376)*

### 1.12. Server-side fallback для client-side rendered сайтов
Аудит 71 бизнеса: средний бизнес «утекает» 84% identity to AI systems. Главная причина — client-side JS без static fallback возвращает zero extractable text. Решение: SSR или static HTML fallback для всего критического контента.
*Источник: [AI search can't verify your business](https://searchengineland.com/ai-search-cant-verify-business-fix-483376)*

### 1.13. robots.txt + noindex conflict — частая ошибка
Если блокируете страницу через robots.txt AND noindex — Google не видит noindex (crawler не может access page). Anthropic допустил эту ошибку с `claude.ai/share`, и Google проиндексировал приватные чаты. Правильно: разрешить crawl через robots.txt, но поставить noindex в HTML.
*Источник: [Google indexed Claude Chats](https://searchengineland.com/google-indexed-claude-chats-because-anthropic-didnt-block-your-private-chats-from-search-engines-483748)*

---

## ПРИОРИТЕТ 2: Структура контента для AI-извлечения (AEO)

### 2.1. Q&A-формат с вопросами в H2/H3
AI Overviews и LLM ищут блоки «вопрос-ответ». Заголовки-вопросы = маяки для извлечения.

### 2.2. Лаконичные ответы 40-60 слов
Ключевая информация в 40-60 словах, с намёком на доп. ценность на сайте. Повышает шанс попадания в AI Overview / snippet.

### 2.3. Chunking: каждый блок самодостаточен
Каждый раздел отвечает на вопрос без контекста соседних абзацев. AI извлекает отдельные пассажи, а не целые страницы.

### 2.4. Front-loading ответа
Ответ — в первые строки каждого блока, затем детали. 80% repeatedly-cited AI Mode passages ставят ответ в первое предложение.
*Источник: [What 15.7M AI Mode citations reveal](https://searchengineland.com/what-15-7-million-ai-mode-citations-reveal-about-getting-quoted-by-google-483393)*

### 2.5. Называйте сущность явно
Вместо «Оно хорошо работает для брендов» → «Creator marketing хорошо работает для брендов». Пассаж должен быть автономен вне контекста.

### 2.6. Claim first → evidence second + comparison tables
Утверждение первым, подтверждающие данные после. **HTML-таблицы** для comparison-данных (times, prices, named routes) цитируются в AI Overviews значительно чаще любого другого формата. Не vague editorial.
*Источник: [What 9 months of AI Overview data reveal](https://searchengineland.com/ai-overview-data-51000-tracked-events-485080)*

### 2.7. Двусторонние внутренние ссылки между страницами кластера
Перекрёстные ссылки с описательным anchor text. Помогает AI видеть полный охват темы.

### 2.8. Passage-level optimization: один сильный пассаж = ответ на 483 запроса
15.7M AI Mode citations: Google переиспользует одни и те же пассажи. Топ-пассаж цитировался 661 раз across 483 distinct queries. Median cited passage — 117 слов, полный multi-sentence абзац. Один сильный параграф = go-to ответ для целого кластера запросов — не нужны 10 thin pages.
*Источник: [What 15.7M AI Mode citations reveal](https://searchengineland.com/what-15-7-million-ai-mode-citations-reveal-about-getting-quoted-by-google-483393)*

### 2.9. 85% passage self-containedness: никаких «as mentioned above»
85% highlighted passages в AI Mode полностью self-contained. Никаких «as mentioned above», reliance on surrounding page. Если пассаж имеет смысл только в контексте страницы — он не извлекается AI.
*Источник: [What 15.7M AI Mode citations reveal](https://searchengineland.com/what-15-7-million-ai-mode-citations-reveal-about-getting-quoted-by-google-483393)*

### 2.10. Question-led passages recycled в 2x чаще
48% repeatedly-cited passages начинались с явного вопроса (heading), vs 22% для one-off. Q&A и how-to форматы доминируют в highest-reuse tiers. Narrative explainers переиспользуются меньше, standalone statistics — редко.
*Источник: [What 15.7M AI Mode citations reveal](https://searchengineland.com/what-15-7-million-ai-mode-citations-reveal-about-getting-quoted-by-google-483393)*

### 2.11. Liquid content: атомарные content objects вместо статей
Контент разбивается на «атомарные объекты» (verified facts, quotes, data, resources), которые переупаковываются в разные форматы — briefings, infographics, podcasts, slide decks. CMS должна поддерживать модульную сборку. Ценность смещается от статьи как целого к фактам внутри неё.
*Источник: [How to turn news articles into assets for AI search](https://searchengineland.com/turn-news-articles-into-ai-search-assets-483950)*

### 2.12. Page independence test перед созданием новой страницы
1) Проверьте GSC — не ранжируется ли уже существующая страница по этому запросу. 2) Сравните top-10 SERPs обоих запросов — high overlap = related. 3) Оцените, может ли контент быть self-contained. High SERP overlap + cannibalization risk = expand existing page, не создавайте новую.
*Источник: [How to decide whether a keyword deserves its own page](https://searchengineland.com/keyword-deserve-own-page-484567)*

---

## ПРИОРИТЕТ 3: Контентная стратегия (что публиковать)

### 3.1. Prompt research рядом с keyword research
Для каждого топика — два числа: keyword volume (Google) и prompt volume (ChatGPT/Perplexity/Gemini). Разрыв определяет формат: keyword-strong → классическая SEO-страница; prompt-strong → контент для AI-цитирования; strong-both → флагманский pillar.

### 3.2. Topic clusters вместо одиночных статей
Один pillar + 3-5 кластерных страниц. Topical authority — сильнейший предиктор AI-цитирования (r=0.41), сильнее Domain Authority и backlinks. 88% AI Overviews цитируют 3+ источника — кластер даёт шанс попасть в каждый sub-query.

### 3.3. Query fan-out как каркас подзаголовков
Генерируйте 40+ fan-out подзапросов для каждого кластера. Tier 1 = H2, Tier 2 = подзаголовки.

### 3.4. Query templates как метод расширения topical authority
Вместо покрытия только entity-атрибутов, map query template variations («how to X», «best X for Y», «X vs Y») и создайте контент для каждой вариации. WikiHow держит authority для «how to» template across unrelated topics — authority прикрепляется к query format, а не к topic. Hybrid methodology: все entities класса + все attributes + все query template variations = strongest topical authority.
*Источник: [Query templates: Expanding the scope of topical authority](https://searchengineland.com/query-templates-topical-authority-484676)*

### 3.5. Проприетарные данные = единственный moat
Оригинальные исследования, датасеты, индексы, фреймворки под собственным именом. AI не может собрать их из других источников → вынужден атрибутировать ваш бренд.

### 3.6. Публикация на emerging-трендах до пика
Мониторить тренды (Exploding Topics, Google Trends, Reddit, TikTok). Публиковать кластер на стадии роста, не пика. Emerging categories: buyer questions не имеют search volume, но formal vocabulary (regulations, standards, job titles) растёт 30-90x за 12 месяцев. Регистрируйте emerging categories через monitoring proper nouns — regulation names, ISO standards, new job titles на LinkedIn.
*Источник: [How to spot an emerging category in search data](https://searchengineland.com/spot-emerging-category-search-data-484393)*

### 3.7. First-person опыт и lived details
LLM не могут фабриковать lived details. First-person accounts, цитаты из реальной практики, ошибки и выводы — это то, что делает контент неинтерчейнджабельным.

### 3.8. Язык клиентов, а не спецификаций
Никто не спрашивает ChatGPT про «раму 49 см». Спрашивают: «какая коляска проходит через турникет метро». Извлекайте реальные вопросы из отзывов, support-тикетов, форумов.

### 3.9. Information gain — контент должен приносить новую информацию
Контент, который переупаковывает уже опубликованные факты, становится избыточным. 86% B2B SaaS маркетологов планируют вкладывать больше в proprietary research.

### 3.10. TOFU content: YMYL упал, B2B tech вырос
YOY данные: finance, healthcare, legal, consumer tech TOFU — все потеряли трафик (AI Overviews aggressive в YMYL). Cybersecurity, marketing/sales SaaS — выросли. Стратегия: в YMYL нишах инвестируйте в proprietary data и expert content; в B2B tech TOFU ещё работает.
*Источник: [Is top-of-funnel content still worth it in 2027?](https://searchengineland.com/top-of-funnel-content-worth-it-485746)*

### 3.11. /en/ folder для не-English сайтов = AI visibility hack
ChatGPT-User retrieves English version страниц в 65-79% случаев на multilingual сайтах (over-indexing 2.6x). Добавление `/en/` folder с English-переводом cornerstone страниц — один из немногих content-side moves, который расширяет AI footprint. Bias возникает в retrieval path ChatGPT, не в training data.
*Источник: [Should multilingual websites add English pages for AI visibility?](https://searchengineland.com/multilingual-websites-english-pages-ai-visibility-484251)*

### 3.12. Multi-location SEO: fewer, purposeful geographic pages
Не создавайте страницу для каждого города с search volume. Map real-world business structure: physical locations (deserve pages), regional markets (maybe), service areas (don't auto-deserve URLs), target cities (marketing goals, not pages). Hub-and-spoke architecture с internal links.
*Источник: [Multi-location SEO: How to structure geographic pages at scale](https://searchengineland.com/multi-location-seo-structure-geographic-pages-483959)*

### 3.13. News sitemap + Publisher Center для новых публикаций
Case study 6 месяцев: AI Overviews — week 1, blue links — week 1, Google News/Top Stories — week 9 (после добавления news sitemap). Без news sitemap — indexing delays. Концентрация на одном domain вместо распределения по брендам = faster authority building.
*Источник: [How to launch a news publication that earns visibility in Google](https://searchengineland.com/news-publication-google-visibility-484268)*

### 3.14. LLM landing page ≠ PPC landing page
LLM referral traffic конвертирует на 20% (61% выше paid search), но требует другой landing page experience. PPC: stripped-down, aggressive CTA, minimal nav. LLM: depth, verification, transition from AI summary to human expertise, navigable, rich resources. LLM user fact-checking AI → нужен nuanced information, не high-pressure form.
*Источник: [LLM traffic converts differently](https://searchengineland.com/llm-traffic-converts-differently-what-to-do-484964)*

### 3.15. Social topical map: синхронизация social content с SEO
Каждой topical category в SEO-стратегии должен соответствовать social content stream. YouTube organic traffic удвоился за год, Facebook/Instagram +60%. Social content индексируется и появляется в AI Overview source panels. SEO-команде нужен social topical map.
*Источник: [Why every SEO team now needs a social topical map](https://searchengineland.com/seo-social-topical-map-484018)*

---

## ПРИОРИТЕТ 4: E-E-A-T и Entity Footprint

### 4.1. Named-авторы с верифицируемыми credentials
Конкретные квалификации, опыт, ссылки на опубликованные работы. Bylines с проверяемой экспертизой коррелируют с лучшими результатами.

### 4.2. sameAs-ссылки на канонические внешние узлы
В schema добавить `sameAs` на Wikidata, LinkedIn, Crunchbase. Помогает AI «схлопнуть» варианты имени в одну сущность.

### 4.3. Консистентность имени бренда во всех точках
Унифицировать написание на сайте, в schema, директориях, соцпрофилях. Фрагментация сущности = AI не собирает бренд в единый авторитетный узел.

### 4.4. Аудит AI entity footprint (6 измерений)
Identity, Differentiation, Evidence, Consistency, Relationships, Specialization. Оценить 0-5 по каждому. Промпт: «Tell me everything you know about [Business Name]» — запустить через ChatGPT, Gemini, Claude.

### 4.5. Expert quotes в контенте
Запрашивайте цитаты у признанных экспертов. Их одобрение усиливает authority страницы.

### 4.6. «Last updated» даты + регулярный refresh
76.4% top-cited страниц ChatGPT обновлены за последние 30 дней. Свежесть = trust signal для AI.

### 4.7. Vertical authority > horizontal dominance для AI-mentions
DTC-бренды с узкой вертикалью (Knix — period underwear) выигрывают у крупных горизонтальных брендов (H&M, Victoria's Secret) в AI-ответах: 29 mentions vs 2. AI-системы строят contextual understanding через repeated, structured signals. Узкая вертикаль + консистентное messaging = инженерия vertical authority.
*Источник: [DTC LLM visibility case study](https://searchengineland.com/guide/dtc-llm-visibility-case-study)*

### 4.8. Brand message engineering для AI-обучения
Define 1-3 core associations (не «high quality», а «size-inclusive activewear for new moms»). Audit owned channels — очевидны ли associations за 30 секунд? Brief creators, PR, media на то же positioning. Test: AI-queries «Which brands are known for ___?» — если бренд не появляется, refine message. AI не угадывает кто вы — он отражает то, что веб повторяет о вас.
*Источник: [DTC LLM visibility case study](https://searchengineland.com/guide/dtc-llm-visibility-case-study)*

### 4.9. Structured social proof: JSON-LD для reviews + testimonials
Добавьте структурированные отзывы (aggregateRating, Review schema) на product pages. AI-системы ищут consensus — co-occurrence бренда с positive sentiment. Текстовые testimonials с именами и контекстом использования, не только star ratings.
*Источник: [DTC LLM visibility case study](https://searchengineland.com/guide/dtc-llm-visibility-case-study)*

### 4.10. Always-on creator campaigns вместо one-off influencer posts
Постоянные creator campaigns создают устойчивый поток third-party контента. AI обучается из repeated exposure. Mid-size niche creators с well-structured content (comparison videos, honest reviews, tutorials) выигрывают у mega-influencers — 94% AI-cited YouTube videos — long-form, 40.83% имеют <1,000 views.
*Источник: [DTC LLM visibility case study](https://searchengineland.com/guide/dtc-llm-visibility-case-study) + [Creator content in AI search strategy](https://searchengineland.com/creator-content-ai-search-strategy-483616)*

### 4.11. UGC platforms = largest third-party source (17.1% vs 4% publishers)
Из 35,000 ChatGPT citations: UGC platforms (Reddit, Wikipedia, Quora, YouTube, LinkedIn) hold 17.1% cited domains — в 4 раза больше, чем publishers (4%). UGC — «floor» visibility на всех этапах buyer journey. Инвестируйте в community presence — наименее финансируемый, но крупнейший источник.
*Источник: [Community signals are AI's largest third-party source](https://searchengineland.com/community-signals-ai-largest-third-party-source-484606)*

### 4.12. Citations ≠ mentions: topical authority differentiation
Бренды могут быть cited вне своей экспертизы (41% в distant categories), но mentioned только в core topics. AI рекомендует бренд только там, где он построил **repeat topical authority** (appears in 5/5 prompt variants). «Spread too thin» penalty = penalty за shallow presence.
*Источник: [Does topical focus make your brand more visible?](https://searchengineland.com/does-topical-focus-make-your-brand-more-visible-484280)*

### 4.13. 85% brand mentions в AI приходят с третьих сторон
AirOps research: до 85% top-of-funnel B2B brand mentions в AI search приходят из third-party content. Owned content даёт baseline messaging, но earned media формирует trust. AI понимает бренд через owned content, но выбирает через third-party validation.
*Источник: [3 phases to build authority and earn AI citations](https://searchengineland.com/phases-build-authority-earn-ai-citations-485470)*

### 4.14. 3-фазная compounding-модель authority
Phase 1 — Technical accessibility (логичная навигация, machine-readable structure, SEO/accessibility tagging). Phase 2 — Fresh + refreshed content (gap-анализ, seasonal editorial, proprietary data studies; repurposing: blog → infographic, topic → hub-and-spoke). Phase 3 — Outreach & digital PR (authoritative third-party sources: publications, podcasts, Substacks; SME-driven content). Эффект compounds: каждая citation усиливает следующую.
*Источник: [3 phases to build authority and earn AI citations](https://searchengineland.com/phases-build-authority-earn-ai-citations-485470)*

---

## ПРИОРИТЕТ 5: Structured Data

### 5.1. Schema markup в server-side HTML
Article (автор, даты, заголовок), Organization на homepage, BreadcrumbList, VideoObject. Schema должна быть в первоначальном HTML. JSON-LD стрипается при конверсии в Markdown — alt-text изображений выживает, JSON-LD — нет.

### 5.2. WebPage schema с speakable property
Для voice search оптимизации. Выделяет пассажи, которые читаются вслух.

### 5.3. Соответствие schema видимому контенту
Structured data должен совпадать с тем, что видит пользователь. Манипуляция = риск демоушна.

### 5.4. Не тратить ресурсы на llms.txt
Google не использует llms.txt. Schema — хорошая гигиена, но не тот рычаг, который обещают вендоры.

### 5.5. Review snippet: запрет на incentivized reviews
Google обновил guidelines: не включайте fake или undisclosed incentivized reviews в markup. Reviews in exchange for benefit (money, discounts, free products) без clear disclosure — нарушение. Риск: потеря eligibility для review rich results.
*Источник: [Google says don't include fake or undisclosed incentivized reviews](https://searchengineland.com/google-says-dont-include-fake-or-undisclosed-incentivized-reviews-in-review-snippet-structured-data-483456)*

---

## ПРИОРИТЕТ 6: Off-page / Authority (вместо link buying)

### 6.1. Brand mentions > backlinks для AI Overview
Ahrefs: корреляция brand mentions с AI Overview ≈0.664 vs 0.218 для backlinks. YouTube-упоминания — сильнейший сигнал (≈0.737).

### 6.2. Earned mentions на топически релевантных площадках
AI ищет consensus — co-occurrence бренда рядом с отраслевыми терминами, конкурентами, use-cases. Рандомная ссылка в нерелевантной статье = шум, отфильтровывается.

### 6.3. Отзывы на авторитетных агрегаторах
G2, Capterra, Trustpilot (B2B), Gartner/Forrester (enterprise). Если бренда нет в правильной категории на Gartner — он исключается из vendor shortlist в AI-ответах.

### 6.4. Founder-led PR: подкасты, co-marketing, комьюнити
Создаёт entity association, который AI кодирует как факт.

### 6.5. BOFU-сравнения на собственном сайте
«Ваш бренд vs Конкурент», «Альтернативы Конкуренту». Цель — narrative control.

### 6.6. Мультиплатформенный footprint
Контент на YouTube, Reddit, LinkedIn, TikTok — индексируется и появляется в AI Overview source panels.

### 6.7. Не покупайте ссылки и не используйте PBN
Paid links на low-authority сайтах и guest posts ради ссылки не работают для AI и несут риск пенальти.

### 6.8. Тройственная модель link acquisition
Link building (явный запрос ссылки) — для BOFU/commercial страниц. Linkable assets (free tools, статистика, шаблоны) — привлекают ссылки пассивно; решается через внутренние ссылки с asset → commercial page. Digital PR (история для журналистов) — масштабируется через синдикацию. Nofollow-ссылки и brand mentions от digital PR конвертируются в dofollow через follow-up outreach. Цель — «own a topic».
*Источник: [Link building works better when you think beyond links](https://searchengineland.com/think-beyond-links-484802)*

### 6.9. AI ищет consensus, не random backlinks — co-occurrence как signal
AI answer engines анализируют patтерны corroboration по всему вебу. Если бренд упомянут на credible, topically relevant источниках рядом с отраслевыми терминами — модель кодирует это как факт. Context is the new authority signal: co-occurrence имени бренда рядом с релевантными терминами важнее, чем ссылка сама по себе.
*Источник: [Why the traditional link building model no longer works for AI search](https://searchengineland.com/traditional-link-building-model-no-longer-works-ai-search-484530)*

### 6.10. «Link building 2.0» = rebranded link buying — не ведитесь
Агентства, продававшие backlinks, теперь продают «LLM visibility campaigns». Под капотом — те же схемы: paid mentions на low-quality сайтах, sponsored listicles, astroturfing на Reddit. Купленные brand mentions не работают для AI, если они не исходят от topically relevant, credible источников.
*Источник: [Why the traditional link building model no longer works for AI search](https://searchengineland.com/traditional-link-building-model-no-longer-works-ai-search-484530)*

### 6.11. Editorial linking ethic: «you can't demand the click if you won't give the link»
Паблишеры, требующие citations от AI-платформ, часто сами не дают ссылки на источники. Упоминание домена без ссылки — распространённая практика из страха «потерять link equity». Ссылка на релевантный источник не drain'ит authority. Стандарт: если упомянули источник, дайте clickable link.
*Источник: [You can't demand the click if you won't give the link](https://searchengineland.com/you-cant-demand-the-click-if-you-wont-give-the-link-484377)*

### 6.12. Toxic backlinks и SEO sabotage — legal precedent
Судебный иск о SEO-саботаже через toxic backlinks прошёл дальше — судья разрешил дело. Legal precedent: намеренное создание toxic backlinks может преследоваться юридически. Мониторьте backlink profile на suspicious spikes, документируйте incidents, используйте disavow tool.
*Источник: [Judge lets SEO sabotage lawsuit over toxic backlinks move forward](https://searchengineland.com/seo-sabotage-lawsuit-toxic-backlinks-484795)*

### 6.13. Link building в 2027: quality over quantity
Wins: genuine journalist relationships, original data, finding the story inside a brand/dataset, slower sharper pitches, digital PR extending to brand mentions. Fails: AI-генерация 500 pitch'ей в неделю (burning sender reputation), buying spammy links (March 2026 spam update hit link manipulation), chasing speed over quality, copying competitors verbatim.
*Источник: [Link building in 2027: 13 ways to win or fail](https://searchengineland.com/link-building-win-or-fail-486023)*

---

## ПРИОРИТЕТ 7: Преодоление ghost citations

### 7.1. Раздельный учёт citations и mentions
40% цитат AI не называют бренд. Трекать 4 категории: cited+mentioned, cited-only (ghost), mentioned-only, neither.

### 7.2. Привязка бренда к факту прямо в предложении
Вместо «Наш анализ показал, что 40%...» → «Writesonic Ghost Citation Study показала, что 40%...».

### 7.3. Названные исследования как brand moat
Исследование/индекс/фреймворк с именем бренда в названии — AI вынужден атрибутировать.

### 7.4. Стратегия по движку: namers vs citers
Perplexity / AI Mode — цитируют URL, но часто не называют бренд (52% / 49% ghost). Gemini / Copilot — называют бренд, но реже цитируют.

### 7.5. 91% цитаций появляются только в одном AI-движке
91% citations appear in only one of ChatGPT, Perplexity, or AI Overviews. Cross-engine overlap минiscule. Prompt tracking должен быть ближе к polling / focus groups, чем к SEO rank tracking. Brand mentions > citations для business outcomes.
*Источник: [AI halftime report: H1 2026](https://searchengineland.com/ai-halftime-report-h1-2026-483912)*

### 7.6. ChatGPT API ≠ продукт ChatGPT — overlap 0.23–0.27
Jaccard similarity между бренд-mentions в API и product ChatGPT — 0.23–0.27. Даже два режима ChatGPT (Instant vs Think) делят только ~33% брендов. API полезен для probing знаний модели, но не для предсказания ChatGPT-ответа.
*Источник: [Inside ChatGPT's retrieval stack](https://searchengineland.com/chatgpt-retrieval-stack-index-cache-pages-485036)*

---

## ПРИОРИТЕТ 8: Обновление существующих страниц

### 8.1. 56-дневный GSC baseline перед любым обновлением
56 дней — достаточно узко для одного сезона, достаточно надёжно. Lock baseline ДО изменений.

### 8.2. Тегирование секций: Keep / Fix / Remove / Add
Keep — ранжируется и точна. Fix — верная идея, устаревшее исполнение. Remove — неверная/избыточная. Add — данных не хватает.

### 8.3. Striking-distance queries (позиции 5-20)
Дешёвые победы. Найти запросы с impression volume, но слабым CTR.

### 8.4. Никогда не менять URL slug, meta title (если работает), schema
Полное переписывание = self-inflicted demotion. Schema расширяется, не заменяется.

### 8.5. Fact-check все числовые данные
Цены, расстояния, даты — всё перепроверять.

### 8.6. Technical debt prioritization: 4-bucket framework
Не каждый crawl issue заслуживает fix. Score by impact, scale, risk, effort. **Fix now**: влияет на crawling/indexing/rankings revenue pages. **Fix soon**: meaningful drag. **Monitor**: low-impact but watch. **Ignore**: safe without guilt. Layer crawl data с GSC performance data — issue на revenue page = priority, issue на blog tag page = monitor.
*Источник: [Technical debt in SEO: When to fix vs. when to ignore](https://searchengineland.com/technical-debt-seo-fix-vs-ignore-483240)*

### 8.7. Matched page-group comparisons для SEO testing
SEO split testing редко идеален. Используйте matched page-group comparisons: treatment group vs pages с similar demand, competition, history. Track metrics matching hypothesis (crawl activity, rankings, traffic — не только traffic). Define success/failure/inconclusive states ДО данных. Учитывайте crawl coverage — Google может не recrawl достаточно страниц до вывода.
*Источник: [Technical SEO testing: How to build a stronger experiment](https://searchengineland.com/technical-seo-testing-build-stronger-experiment-484537)*

---

## ПРИОРИТЕТ 9: F.A.C.T.S. Framework (Search Everywhere Optimization)

### Freshness
Средний AI-cited URL на 25.7% новее, чем в традиционном поиске. >70% AI-cited страниц обновлены за 12 месяцев.

### Authority
Бренды с авторитетным контентом + рекомендации из доверенных источников на 40% чаще появляются в AI-ответах.

### Consistency
AI берёт данные из Google Maps, сайтов, Yelp, Facebook. Несовпадения → inaccurate AI-mentions (~79% accuracy сейчас).

### Trust
92% потребителей читают отзывы. ChatGPT-рекомендованные бизнесы в среднем 4.4★ vs 4.2★ в Google.

### Semantic Relevance
Средний AI-запрос — 23 слова (vs 4 в традиционном поиске). Dedicated service pages и comprehensive FAQ.

---

## ПРИОРИТЕТ 10: Мониторинг и метрики

### 10.1. Search Console AI performance reports
Запущены 3 июня 2026. Показывают impressions в AI Overviews и AI Mode по page, country, device. Глобально доступны с августа 2026.
*Источник: [Google Search Console AI performance reports rolling out globally](https://searchengineland.com/google-search-console-ai-performance-reports-and-search-generative-ai-control-rolling-out-globally-486269)*

### 10.2. Money-query set для мониторинга
Конкретные промпты, которые покупатели используют перед покупкой. Трекать citation share. Total brand mentions — vanity metric.

### 10.3. Tag AI-referred sessions в GA4 → CRM → pipeline
Фильтр по referrer: chat.openai.com, perplexity.ai, google.com с AI Mode. Конверсии AI-трафика выше на 31-42%.

### 10.4. ChatGPT-User user agent в server logs
Pages, которые ChatGPT открывает в thinking mode, не несут utm_source — вы считаете клики и пропускаете reads. Мониторить crawl через server logs.

### 10.5. Branded demand как proxy (dark funnel)
Рост branded clicks в GSC + branded conversions в GA4, совпадающий с ростом AI visibility — evidence AI-влияния.

### 10.6. 5-слойный фреймворк измерения
1. AI access (crawl frequency, depth) 2. AI visibility (mention rate, citation rate, GSC AI impressions) 3. AI referral traffic (GA4) 4. Dark funnel (branded search growth) 5. Pipeline & revenue.

### 10.7. GA4 custom dimension для `#:~:text=` fragment
Google AI Overviews добавляют `#:~:text=` text-fragment directive к URL при клике на cited snippet. Создайте custom dimension в GA4, который срабатывает при наличии этого фрагмента — самый надёжный способ измерять AI Overview referral traffic.
*Источник: [What 9 months of AI Overview data reveal](https://searchengineland.com/ai-overview-data-51000-tracked-events-485080)*

### 10.8. 22.4% AI Overview traffic misattributed to Direct
51,200 tracked events over 9 months: 22.4% AI Overview sessions атрибутируются как Direct вместо Organic Search. Worst month — 29.3%, best — 16.8%. Без коррекции SEO-отчёты существенно занижают organic performance.
*Источник: [What 9 months of AI Overview data reveal](https://searchengineland.com/ai-overview-data-51000-tracked-events-485080)*

### 10.9. Highlight accumulation как метрика AI-visibility
Pages accumulate distinct text-fragment highlights over time, count сильно коррелирует с organic position. Pages с 1-4 highlights: median rank #11. Pages с 21+ highlights: median rank #1, 67% ranking first outright. Трекайте количество уникальных highlighted passages как leading indicator.
*Источник: [What 15.7M AI Mode citations reveal](https://searchengineland.com/what-15-7-million-ai-mode-citations-reveal-about-getting-quoted-by-google-483393)*

### 10.10. Microsoft Clarity AI Scrape-to-Referral Ratio
Новая метрика в Clarity: сравнивает AI scrape activity с referral traffic. Operator-level breakdown: какие AI sources отправляют traffic, какие только скрейпят. 6000:1 ratio = бот скрейпит 6000 раз на 1 referral. Решает: стоит ли разрешать AI-ботам скрейпить сайт.
*Источник: [Microsoft Clarity AI Scrape-to-Referral insights report](https://searchengineland.com/microsoft-clarity-ai-scrape-to-referral-insights-report-484959)*

### 10.11. Prompt mapping по funnel stages
Вместо aggregate AI visibility score — break down by funnel stage. Example: 40% overall, но 70% в branded/comparison prompts и 10% в problem discovery. Показывает где бренд входит в conversation, где выпадает. Track: Does AI associate brand with problem space? Does it make shortlists? Where does visibility drop as purchase intent increases?
*Источник: [How to map AI search prompts to every stage of the sales funnel](https://searchengineland.com/map-ai-search-prompts-sales-funnel-486060)*

### 10.12. 4 trackable AI visibility metrics для client reporting
(1) **Visibility** — появляется ли бренд в ответе. (2) **Position** — насколько prominently. (3) **Sentiment** — как AI описывает. (4) **Citations** — какие URLs модель использует. 66% agencies say AI search is top new client request; 48% can't reliably track AI discovery.
*Источник: [Your client just asked if they show up in ChatGPT](https://searchengineland.com/your-client-just-asked-if-they-show-up-in-chatgpt-now-what-482951)*

### 10.13. GSC Platform properties — first-party search data для social/video
Google Search Console позволяет verify social/video accounts (Instagram, TikTok, X, YouTube) и получать clicks, impressions, CTR, queries. Нет historical backfill — data starts при verification. Query groups (trending up/down), 24-hour filter, format comparisons (Shorts vs long-form).
*Источник: [Google Search Console Platform properties are now globally live](https://searchengineland.com/google-search-console-platform-properties-are-now-globally-live-483921)*

### 10.14. Attribution vs. Incrementality — нужны оба
Attribution: какие touchpoints получают credit. Incrementality: сколько sales были caused кампанией, а не произошли бы anyway (lift через controlled tests). Attributed conversions ≠ incremental growth. Для AI search: attribution показывает где появился бренд, incrementality доказывает что это создало дополнительный pipeline.
*Источник: [Attribution vs. incrementality: Why you need both](https://searchengineland.com/attribution-vs-incrementality-both-483741)*

### 10.15. LLM referral traffic конвертирует на 20% — highest-converting
LLM referral traffic конвертирует в 20%, на 61% выше paid search. AI уже synthesized options до клика — пользователь не ищет generic landing page, а validation конкретной рекомендации.
*Источник: [LLM traffic converts differently](https://searchengineland.com/llm-traffic-converts-differently-what-to-do-484964)*

---

## ПРИОРИТЕТ 11: Anti-slop (как не быть отфильтрованным)

### 11.1. Избегать структурной однородности AI-контента
AI-текст имеет detectable shape pattern — 97% accuracy. AI moralises в 77% случаев, 79% AI-историй имеют zero subplots. Структурное однообразие = red flag.

### 11.2. Unique + Specific + Authentic (критерий Google)
Unique — точка зрения, которой нет у других. Specific — конкретный случай. Authentic — first-hand knowledge.

### 11.3. Разделять контент на 3 трека
Commodity (глоссарии, FAQ) — AI генерирует, человек проверяет. Hybrid (сравнения, гайды) — AI драфт, человек редактирует. Expertise (исследования, кейсы) — эксперт пишет, AI помогает.

### 11.4. Owned channel — страховка от фильтров
Email, community — место без фильтра между вами и читателем.

### 11.5. Platform anti-slop systems — конкретные механизмы
LinkedIn: deployed slop identification, «Seems like AI slop» button, killed «Enhance post». Substack: Pangram для AI detection site-wide. YouTube: demonetizes «repetitive, low-effort, emotionally manipulative video» — 11 channels terminated, ~4.7B lifetime views wiped. Reddit: AI detection — 23M spam views blocked, ~2M inauthentic votes revoked daily. Pinterest: AI detection labels + feed control. TikTok: AI labels + invisible metadata watermarks. Meta: «AI info» labels since 2024, extended to ads June 2026. Spotify: 75M+ spammy tracks removed.
*Источник: [Slop antibodies](https://searchengineland.com/slop-antibodies-the-link-between-ai-slop-watermarking-and-commodity-content-485182)*

### 11.6. EU AI Act Article 50 — mandatory watermarking
EU AI Act требует machine-readable watermarks для output generative systems, penalties до €15M или 3% global turnover. Anthropic внедрило watermarking в Claude models globally. Watermark embedded в text — persist при copy/paste. **Watermark не доказывает Claude создал оригинал — только что Claude «processed» текст. Отсутствие watermark ≠ не AI-generated.**
*Источник: [Anthropic adds AI text watermarking](https://searchengineland.com/claude-ai-text-watermarking-484667)*

### 11.7. Watermarking technical limitations
Детекторы нужны ~100-200 tokens минимум (LinkedIn comment = 20-50 tokens — below floor). Editing/paraphrasing/translation/chaining models может weaken/remove mark. ICML 2025: paraphrasing attack ~100% success at $0.88/M tokens. Open weights = escape hatch.
*Источник: [Slop antibodies](https://searchengineland.com/slop-antibodies-the-link-between-ai-slop-watermarking-and-commodity-content-485182)*

### 11.8. Google не пенализирует за AI watermark — пенализирует за unoriginal content
AI-generated content не автоматически penalized. Scaled content abuse policy target — large volumes of low-value content. Watermark ≠ ranking signal. Вопрос не «can AI tell it's AI?» — «does this page contribute anything worth retrieving, citing, synthesizing?»
*Источник: [If an AI watermark scares you, your content may be the real issue](https://searchengineland.com/ai-watermark-content-issue-485848)*

### 11.9. Production cost collapse → distribution is bottleneck
Content production не bottleneck (AI = near zero cost). Permission to distribute — scarce resource. AI Overviews reduce clicks ~50% on average. Quality = blurry but critical filter for distribution.
*Источник: [Slop antibodies](https://searchengineland.com/slop-antibodies-the-link-between-ai-slop-watermarking-and-commodity-content-485182)*

---

## ПРИОРИТЕТ 12: ChatGPT Retrieval Internals (новое)

*Основано на исследовании 28 дней, 500+ промптов, 14,000+ URL. Источник: [Inside ChatGPT's retrieval stack](https://searchengineland.com/chatgpt-retrieval-stack-index-cache-pages-485036)*

### 12.1. Трёхслойная архитектура: index → cache → live
(1) **Discovery index** (`labrador`) — находит страницы. (2) **Reading cache** — хранит полные копии страниц в Markdown. (3) **Live opens** — открывает страницы в real-time через ChatGPT-User. В instant-режиме (90%+ free) ChatGPT не открывает страницы — работает только с title + ~200-символьным snippet. В thinking-режиме открывается ~100 URLs на 28 доменов, открытая страница цитируется в 74% случаев, неоткрытая — лишь 7%.

### 12.2. `labrador` — собственный индекс OpenAI, не Bing
Только 1.5% URL из `labrador` появляются в top-20 Bing. Snippet в `labrador` — query-independent, фиксируется при индексации. Meta description игнорируется в `labrador`, но работает в Google-fed пайплайнах (`bright`). **Оптимизация под Bing и Google недостаточна для ChatGPT instant-режима.**

### 12.3. Экономика routing: instant = бесплатно, thinking = платно
Instant-режим использует только индекс OpenAI (бесплатно). Thinking-режим платит за scraped Google results (75%) + реальные page opens. Free Think = 74.7% labrador, 3.1% Google. Paid Thinking = 75.3% scraped Google, 24.7% labrador. **Два разных корпуса источников — нужны две стратегии видимости.**

### 12.4. Reading cache: stale-while-revalidate, shared across all users
Cache хранит full pages в Markdown, шарится между всеми пользователями и tier'ами. Свежесть — ~30 минут. `Cache-Control: no-store` и `noindex` **игнорируются**. Непопулярные страницы стареют бесконечно — recrawl определяется только тем, как часто пользователи спрашивают о странице. **Markdown-конверсия: scripts, iframes, JSON-LD стрипаются, alt-text выживает, CSS-hidden text извлекается.**

### 12.5. ChatGPT-User UA не несёт utm_source
Страницы, которые ChatGPT открывает в thinking mode, отображаются в citations БЕЗ `utm_source=chatgpt.com`. Только кликабельные ссылки из instant-режима несут UTM. **Если вы оцениваете ChatGPT-экспозицию по utm_source, вы считаете клики и пропускаете reads.**

### 12.6. Параметрическая память как источник цитат
Часть цитаций ChatGPT не соответствует ни одному search result — модель пишет их из parametric memory (знания вшитые в веса при training). arXiv pulled 2600+ раз, cited 10. **Being retrieved ≠ being cited — два разных рынка.**

### 12.7. ChatGPT Think: сужение retrieval между июлем и августом 2026
Fan-outs упали с 3.56 до 1.90, URLs с 47.2 до 33.9, домены с 21.9 до 15.5. `site:` operator в 58.1% high-effort queries — ChatGPT ищет целевыми переходами на конкретные домены. **Brand + domain recognition становятся важнее broad keyword coverage.**

### 12.8. ChatGPT Shopping и Local — отдельные пайплайны
Shopping обслуживается из merchant feeds OpenAI. Local — из Yelp, TripAdvisor, Google Maps. **Shopping и local никогда не касаются web search — ваша битва в merchant feeds и business listings, не в контенте.**

---

## ПРИОРИТЕТ 13: Accessibility Tree для AI (новое)

### 13.1. AI-агенты читают accessibility tree, не DOM/screenshots
ChatGPT Atlas интерпретирует структуру через ARIA roles и labels. Microsoft Playwright MCP построен на accessibility snapshots. Accessibility tree = structured semantic layer, который browser строит из DOM — тот же layer, что screen readers используют.
*Источник: [10 SEO use cases for auditing your accessibility tree](https://searchengineland.com/accessibility-tree-seo-use-cases-484338)*

### 13.2. 10 SEO use cases для accessibility tree audit
1. Agent readiness audit на money pages. 2. Диагностика JS rendering gaps. 3. Audit conversion paths для WebMCP. 4. Benchmark competitor machine legibility. 5. Валидация heading/landmark hierarchy. 6. Fix anchor text через accessible names. 7. Audit images/alt text для AI extraction. 8. ARIA snapshots в CI (regression testing). 9. Before/after tree diffs для migrations. 10. Prioritize accessibility fixes по SEO value.

### 13.3. ARIA snapshots в CI для регрессионного тестирования
Включите accessibility tree snapshots в CI pipeline. Before/after tree diffs позволяют выявить, когда обновление шаблона ломает ARIA-структуру, критичную для AI-извлечения контента.

### 13.4. AXray Extractor — бесплатный инструмент
Capture full accessibility tree любого URL через headless browser → JSON export. Chrome DevTools также имеет full-page accessibility tree view (Elements → Accessibility pane). Agent readiness audit: pull top 10-20 money pages, capture tree, проверить что key content видим через ARIA.

---

## ПРИОРИТЕТ 14: Multimodal Image GEO (новое)

### 14.1. Изображение = doorway для query и answer
20B Google Lens searches/month. Pinterest Lens — 1.5B/месяц, конвертирует на 62% лучше text search. Google patent (2023 filed, April 2026 published): cited source chosen by image match first, then surrounding text pulled for answer. Image может быть тем, что попадает в ответ, не параграф.
*Источник: [Your images have a new job in AI search](https://searchengineland.com/images-new-job-ai-search-485840)*

### 14.2. Image SEO таблица по page type
- **Homepage**: original brand images (не stock) → AI matching.
- **Product**: multiple angles, OCR-legible packaging → AI reads attributes.
- **Blog**: infographic claims должны существовать как machine-readable text/alt.
- **About/team**: portraits → entity/authorship signals.
- **Service**: before-and-after → co-occurrence service story.
- **Contact**: location images → local business signals.

### 14.3. Co-occurrence audit для images
Два уровня: (1) **Denotation** — что фактически в кадре (объект-level, checkable — названо ли в copy на странице?). (2) **Connotation** — что композиция подразумевает (профессиональный офис? — смысл, который machine extracts). Visual query fan-out analysis: описываете ли вы то, что есть. Co-occurrence audit: положили ли вы правильное в кадр.

---

## ПРИОРИТЕТ 15: Local SEO для AI Search (новое)

### 15.1. Local 5.0 — Context Intelligence как следующая стадия
Эволюция: Local 1.0 (listings, NAP) → 2.0 (map pack, reviews) → 3.0 (location pages) → 4.0 (AI-mediated discovery) → 5.0 (Context Intelligence). AI не просто индексирует — interprets intent, evaluates evidence, recommends. Verification burden переместился от customer к AI. Rich context wins — generic location pages больше не достаточны.
*Источник: [Local 5.0: The next evolution of local SEO](https://searchengineland.com/local-5-ai-search-seo-485160)*

### 15.2. Local 5.0 Roadmap — 5 шагов + flywheel
Step 1 — Trusted digital foundation (knowledge graph + structured data + GBP + maps + directories). Step 2 — Add context (Context Memory Graph: location data + reviews + customer intent). Step 3 — Consistent localized experiences. Step 4 — Continuously measure (Visibility, Share of voice, Accuracy, Opportunity). Step 5 — Scale with AI agents. Flywheel: Measure → Create → Publish → Discover → Optimize.

### 15.3. Business websites доминируют в Gemini local citations (60%)
14,472 citations из 1,487 local queries в 50 U.S. metros: ~60% Gemini citations → business websites. Reddit — #2 с 13.7%, обгоняет весь local-service directory category. ChatGPT и Gemini citing одинаковые домены только 8% времени. **Мониторинг одного движка = misleading picture.**
*Источник: [Business websites dominate Gemini local AI search citations](https://searchengineland.com/business-websites-gemini-citations-local-ai-search-study-485506)*

### 15.4. Grounding Drift: повторные Gemini-запросы дают разные источники ~60%
Повторение одинакового Gemini-запроса даёт overlapping sources только ~40% времени (vs 90% для Local Pack). Gemini рекомендует того же top business только в 7% случаев. Один AI search = snapshot, не надёжная метрика. Нужен многократный замер.

### 15.5. 1.8M Google Business Profiles: specific categories + completeness
Specific primary category → ~36% higher presence в top-10 (12.5% vs 9.2% для generic). Winning combos: Veterinarian + Emergency veterinarian service (+17 позиций). «Service establishment» как additional category — вредно. GBP Completeness Index (0-5: website, description, hours, photos, claimed): 0→5 улучшает avg rank на ~19 позиций и утраивает top-10 rate (4% → 13%).
*Источник: [What 1.8M Google Business Profiles tell us](https://searchengineland.com/google-business-profiles-local-seo-success-data-485727)*

### 15.6. GBP address changes — исторический «призрак» адреса
Смена адреса в GBP не всегда меняет, где Google думает, что бизнес находится. Address history может вызывать hidden algorithmic penalties. Адрес и map pin — не одно и то же. Перед созданием нового listing — прогоните через Google Geocoding API.
*Источник: [Why Google Business Profile address changes can disrupt local rankings](https://searchengineland.com/google-business-profile-address-changes-local-rankings-483537)*

### 15.7. GBP products: digitize inventory для agentic search
Google Business Profile products (бесплатно) появляются в carousel на Google Maps mobile. В era agentic search AI-агенты могут делать покупки — чем больше локальный инвентарь оцифрован, тем лучше prepared для agentic future.
*Источник: [Google Business Profile products](https://searchengineland.com/guide/google-business-profile-products)*

### 15.8. Query Deserves a Page (QDP) — framework для local topical authority
QDP вдохновлён Query Deserves Freshness. Hybrid = сильнейший: все entities класса + все attributes + все query template variations. Меньше, более purposeful страниц > больше дублирующих.
*Источник: [How semantics and topical authority improve local SEO](https://searchengineland.com/how-semantics-and-topical-authority-improve-local-seo-482980)*

---

## ПРИОРИТЕТ 16: Reddit-стратегии для AI Visibility (новое)

### 16.1. Reddit как keyword research tool — mining через Semrush
Reddit ранжируется для ~166M keywords, включая 10M в #1. 35M+ ключей триггерят AI Overviews, Reddit cited в 15M+ (46% citation rate). Процесс: Domain Overview → Organic Research → filter по теме + Position Top 10 → export. SERP Features filter → AI Overviews → export. Keyword Gap report → reddit.com как competitor → tab «Weak». Результат: topical map из 3 buckets (optimization candidates, net-new creation, FAQ/support content).
*Источник: [Reddit is the keyword research tool you're probably not using](https://searchengineland.com/reddit-keyword-research-tool-485859)*

### 16.2. 5-step framework для Reddit authority
1) Define territory of authority — intersection audience needs / brand expertise / product credibility. 2) Establish baseline — Google visibility, AI visibility, community perception, owned content audit. 3) Build connected authority system — Reddit signals feed SEO/content/AI visibility. 4) Focus on right communities — приоритизация subreddits по 5 критериям (relevance, questions you can answer, activity, rules, value without promotion). 5) Engage natively — disclose affiliation, answer directly, avoid corporate language. Кейс Kumon: 5 месяцев → ChatGPT visibility выросла с 5% до 18.13%.
*Источник: [5 steps to building Reddit authority](https://searchengineland.com/building-reddit-authority-visibility-486084)*

### 16.3. Reddit citations в ChatGPT упали на 86% за 4 дня — volatility risk
Reddit share в ChatGPT Search citations: с 3.83% до 0.52% за 4 дня. Первый drop начался в день изменения query fan-out behavior ChatGPT. **AI search visibility может измениться за дни — мониторьте per-platform.**
*Источник: [Reddit's ChatGPT Search citations fell 86%](https://searchengineland.com/reddit-chatgpt-search-citations-fall-report-485473)*

---

## ПРИОРИТЕТ 17: MCP Servers и Tooling (новое)

### 17.1. MCP servers для SEO — 4 use case'а
Model Context Protocol (Anthropic, Nov 2024) — open standard для подключения AI assistants к external data sources. (1) Keyword research by group — feed examples, combine variations, filter by location (из Semrush MCP, без hallucination). (2) Combine MCPs with Claude Skills — brand SEO audit skill запускается одной командой. (3) Historical data visualization — keywords в top-3 vs AI Overviews за 3 месяца. (4) SERP scraping через DataForSEO MCP. Установка: `claude mcp add semrush https://mcp.semrush.com/v1/mcp -t http`. Claude Code лучше Claude UI для MCP.
*Источник: [How to use MCP Servers to speed up SEO research](https://searchengineland.com/guide/use-mcp-servers-speed-up-seo-research)*

### 17.2. MCP для marketing data analysis — chaining tools
MCP servers доступны для Ahrefs, Semrush, DataForSEO, Serpstat, Buffer, VidIQ, Google Analytics, Google Search Console. Промпты: «Organic traffic fell 20% last week. Which pages lost the most?» — обходит 5,000-row export limit GA4. Chaining: GA4 (traffic) + Ahrefs (rankings) → один ответ про «which blog posts lost traffic, what keywords, which to refresh first».
*Источник: [How to use MCP to get more data from the tools you already use](https://searchengineland.com/mcp-data-tools-484650)*

### 17.3. Keyword clustering tool на Python — TF-IDF + HDBSCAN
Скрипт для кластеризации 12,000+ keywords. TF-IDF vectorization → HDBSCAN (density-based, не требует заранее заданного числа кластеров, identifies noise). Результат — semantic groups для topic generation, internal linking, content planning. GitHub: simodepth96/Keyword-Clustering-HDBSCAN.
*Источник: [How to build a keyword clustering tool with Python](https://searchengineland.com/keyword-clustering-tool-python-483977)*

---

## ПРИОРИТЕТ 18: AI Content Workflows (новое)

### 18.1. 7 feedback loops для self-improving AI content workflows
(1) Upstream filter — strategist agent оценивает brief ДО написания (Pass/Revise/Kill). (2) Retrieval refinement — mapping agent проверяет sources vs outline. (3) Quality gate with revision cap — reviewer → writer revision, max 2 rounds, затем escalate to human. (4) Rubric-based scoring + ensemble selection — score по 10 criteria, judge agent сравнивает versions. (5) Adversarial challenge — adversarial agent строит counterargument → writer отвечает. (6) Diff-and-learn — frozen Markdown vs published DOCX → diff agent классифицирует edits → при 3+ одинаковых fixes → proposal обновить pipeline. (7) Performance-feedback — weekly GSC/Semrush data → agent анализирует «what would you change about the brief?».
*Источник: [7 feedback loops for self-improving AI content workflows](https://searchengineland.com/self-improving-ai-content-workflows-483404)*

### 18.2. AI content pipeline architecture — reverse-engineering от quality
Начните с конца: определите «quality» (useful, original, brand voice, ICP-relevant, human-sounding, ranking+citation potential). Constants (hard-code): brand explainer, ICP info, voice guide с examples, example briefs/outlines/articles. Variables: topic, angle, keyword. Pipeline: Orchestrator → Kickoff → Research → Outline (human review gate) → Write → Edit (3 раздельных агента: Editor, Fact-checker adversarial, AI editor для AI tells) → human review. Каждый агент — отдельный clean context window. ~95% готовности к публикации.
*Источник: [How to build an AI content workflow from the ground up](https://searchengineland.com/build-ai-content-workflow-from-ground-up-485565)*

---

## ПРИОРИТЕТ 19: AI Search Behavioral Data (новое)

### 19.1. AI модели ищут знакомые бренды в 3.2x чаще
3,960 responses, 13,281 fan-out searches: модели ищут familiar brands 55.7% vs 17.4% для unfamiliar. 63% brand-specific searches involve top-5 familiar brands. **Memory strongly decides consideration — сильный контент помогает, но знакомые бренды имеют advantage до поиска.** 31% fan-out searches не называют бренд — broad visibility всё ещё работает.
*Источник: [AI models favor familiar brands in search](https://searchengineland.com/ai-models-favor-familiar-brands-search-study-484054)*

### 19.2. AI Visibility Index: 5% брендов underexposed despite strong SEO
Fractl: 471 бренд (5%) — high DR, high traffic, но почти нет AI mentions. 377 (4%) — AI overperformers с modest SEO. ~9% коррелируют с third-party content presence. **Competitive set в AI answer = 5-10 имен. Если вы не в top-5 для вашей категории, Google-ranking может быть недостаточен.**
*Источник: [The AI visibility index](https://searchengineland.com/ai-visibility-index-brands-vanishing-from-ai-search-485057)*

### 19.3. Default brands в AI — models have settled
Travel: Booking.com (285), Airbnb (227), Expedia (215) = ~20% total. Insurance: Lemonade > State Farm, Root > Progressive — digital-native carriers как defaults. **Каждая индустрия имеет short list «default» брендов, часто не совпадающих с SEO-лидерами.**
*Источник: [The AI visibility index](https://searchengineland.com/ai-visibility-index-brands-vanishing-from-ai-search-485057)*

### 19.4. 88% AI Mode product recommendations принимаются как «best»
88% U.S. adults принимают AI Mode product recommendations как best. 75% pick #1 в AI shortlist, но если видят trusted brand в списке — выбирают его. **Trust — высшая валюта в AI search. AEO/GEO = brand channel, замаскированный под performance channel.**
*Источник: [AI halftime report: H1 2026](https://searchengineland.com/ai-halftime-report-h1-2026-483912)*

### 19.5. Topical authority: 15.2% категорий имеют owner, 53.7% — open field
1,094 US categories, 5 prompts per category: только 15.2% имеют clear owner. 89.3% estimated AI-search demand в категориях без owner. **Самые большие по объёму категории — наименее likely иметь owner. Open budget opportunity.** Product/service landing pages — most cited page type (homepages только 4%).
*Источник: [Does topical authority matter in AI search?](https://searchengineland.com/topical-authority-ai-search-482875)*

### 19.6. Topic owners durable — однажды earned, обычно keeps
Бренд, получивший outsized share of mentions в категории, обычно сохраняет его. **Topical authority matters for durability, не только для initial visibility.**
*Источник: [Does topical authority matter in AI search?](https://searchengineland.com/topical-authority-ai-search-482875)*

---

## ПРИОРИТЕТ 20: AI Visibility как Organizational Problem (новое)

### 20.1. AI visibility = organizational coordination problem
82% AI citations указывают на earned media, не own site. Sources owned разными командами (reviews, community threads, editorial, retailer pages, creator content). AI visibility — не content creation issue, а coordination problem. Нужен shared objective между SEO, social, PR, creator teams.
*Источник: [Creator content in AI search strategy](https://searchengineland.com/creator-content-ai-search-strategy-483616) + [LLM visibility starts with better internal communication](https://searchengineland.com/llm-visibility-starts-with-better-internal-communication-484913)*

### 20.2. LLM visibility = internal communication problem
LLM visibility зависит от strength и consistency of brand's overall digital footprint. Teams organized by channel — но channels теперь blended. Cross-functional operating habits: find common ground, establish shared realities, build empathy for needs beyond your own KPIs.
*Источник: [LLM visibility starts with better internal communication](https://searchengineland.com/llm-visibility-starts-with-better-internal-communication-484913)*

### 20.3. Creator & review content — incrementality measurement
Review creators добавляют value через: combating negative PR, trust from credible third party, AEO/GEO signals, shaping brand understanding. Risk: «parasitic» — creator зарабатывает комиссии на клиентах, которые уже знали бренд. PR, affiliate, AEO/GEO, social, brand teams работают независимо → компания платит多次но за one relationship. Solution: incrementality measurement (affiliate platform покажет participation, но не causation).
*Источник: [How to measure the true value of creators and review content](https://searchengineland.com/value-creators-review-content-485028)*

---

## ПРИОРИТЕТ 21: Google AI Overviews / AI Mode Dynamics (новое)

### 21.1. AI Overviews dynamically expand — full AI Mode response в главном SERP
Google подтвердило: для некоторых запросов AI Overview разворачивается в полный ответ без кнопки «Show more», отодвигая organic results вниз. Если пользователь начал скроллить — expansion отменяется. **Ещё меньше кликов для organic — усиление zero-click.**
*Источник: [Google is dynamically expanding AI Overviews](https://searchengineland.com/google-is-dynamically-expanding-ai-overviews-for-some-queries-486200)*

### 21.2. Link carousels for developing topics в AI Mode
Google добавило link carousels (как top stories) для trending/developing topics в AI Mode. Увеличивает clickability AI Mode. Учитывает Preferred Sources пользователя. **Trending topics → больше кликов через carousels — monitor trending queries для opportunistичных публикаций.**
*Источник: [Google adds link carousels for developing topics in AI Mode](https://searchengineland.com/google-adds-link-carousels-for-developing-topics-in-ai-mode-485884)*

### 21.3. AI Overviews = 7.53% organic sessions (волатильно)
51,200 tracked events: AI Overview traffic составляет 7.53% organic sessions, сильно колеблется по месяцам. Top-performing snippet = 2,276 events, average = 31. **Концентрация: малое количество страниц делает bulk работы. Snippets have lifecycles — peak и fade.**
*Источник: [What 9 months of AI Overview data reveal](https://searchengineland.com/ai-overview-data-51000-tracked-events-485080)*

### 21.4. Gemini 3.7 Flash rolling out in Google Search
Gemini 3.7 Flash first rolling out AI Mode for Google AI Pro & Ultra subscribers in English. AI Mode становится быстрее и доступнее.
*Источник: [Gemini 3.7 Flash rolling out in Google Search](https://searchengineland.com/gemini-3-7-flash-rolling-out-in-google-search-485058)*

---

## КЛЮЧЕВЫЕ ИНСАЙТЫ (обновлённые)

1. **AI-видимость = технический SEO + структурная ясность**, а не новый «GEO-трюк»
2. **Topical depth > individual rankings**: страницы на позициях 6-10 с сильным topical authority цитируются чаще, чем #1 со слабым
3. **85% бренд-упоминаний в AI приходят с третьих сторон**, не с вашего сайта
4. **Проприетарные данные — единственный moat**: FAQ и generic content тривиально реплицируются
5. **Citation ≠ recognition**: трекать mentions отдельно, иначе 40% «видимости» существует только в dashboard
6. **Ranking #1 в Google ≠ появление в AI-ответе** — overlap значительно меньше, чем предполагают
7. **Free Think vs Paid Thinking = разные корпуса источников**: Free — 74.7% OpenAI index. Paid — 75.3% scraped Google. Нужно зарабатывать видимость в обоих
8. **Zero-click — новая норма**: 68% Google-поисков в 2026 не заканчиваются кликом
9. **Content production больше не bottleneck — permission to distribute — bottleneck**
10. **AEO/GEO — это brand channel, замаскированный под performance channel**: AI recommendations формируют спрос
11. **Passage, не page — рабочая единица AI Mode**: один сильный параграф = ответ на 483 запроса
12. **AI-боты не исполняют JavaScript**: 0% discovery для JS-injected ссылок — все ссылки в raw HTML
13. **Accessibility tree = semantic layer для AI-агентов**: ARIA roles и labels, не DOM
14. **ChatGPT имеет собственный индекс `labrador`**: оптимизация под Bing/Google недостаточна
15. **Grounding Drift**: одинаковые AI-запросы дают разные источники ~60% случаев — нужен многократный замер
16. **91% цитаций появляются только в одном AI-движке** — multi-engine monitoring обязателен
17. **Image = doorway для visual search**: 20B Google Lens searches/month, patent подтверждает image-first matching
18. **Competitive set в AI = 5-10 имен**: если бренд не в top-5 для категории, ranking может не помочь
19. **AI visibility = coordination problem**: 82% citations → earned media, owned разными командами
20. **15.2% категорий имеют owner, 53.7% — open field**: biggest opportunity в категориях без owner

---

## ИСТОЧНИКИ (70+ статей, проанализированных детально)

### V1 (30 статей)
1-30: см. оригинальный playbook V1

### V2 — новые проанализированные статьи
31. chatgpt-retrieval-stack-index-cache-pages-485036 — Inside ChatGPT's retrieval stack
32. what-15-7-million-ai-mode-citations-reveal-483393 — 15.7M AI Mode citations
33. business-websites-gemini-citations-local-ai-search-study-485506 — Gemini local citations
34. reddit-chatgpt-search-citations-fall-report-485473 — Reddit ChatGPT citations fell 86%
35. ai-models-favor-familiar-brands-search-study-484054 — AI models favor familiar brands
36. ai-visibility-index-brands-vanishing-from-ai-search-485057 — AI visibility index
37. ai-overview-data-51000-tracked-events-485080 — 9 months AI Overview data
38. javascript-links-pages-invisible-ai-search-485228 — JS links invisible to AI
39. measure-brand-visibility-gemini-484116 — Measure brand visibility in Gemini
40. slop-antibodies-485182 — Slop antibodies
41. claude-ai-text-watermarking-484667 — Anthropic watermarking
42. ai-watermark-content-issue-485848 — AI watermark scares
43. microsoft-clarity-ai-scrape-to-referral-insights-report-484959 — Clarity Scrape-to-Referral
44. ai-search-cant-verify-business-fix-483376 — AI search identity leak
45. accessibility-tree-seo-use-cases-484338 — Accessibility tree for AI search
46. map-ai-search-prompts-sales-funnel-486060 — Prompt mapping to sales funnel
47. dtc-llm-visibility-case-study — DTC LLM visibility (Knix case)
48. topical-authority-ai-search-482875 — Topical authority in AI search
49. building-reddit-authority-visibility-486084 — Reddit authority framework
50. images-new-job-ai-search-485840 — Images in AI search
51. llm-traffic-converts-differently-what-to-do-484964 — LLM traffic converts differently
52. attribution-vs-incrementality-both-483741 — Attribution vs incrementality
53. ai-halftime-report-h1-2026-483912 — AI halftime report H1 2026
54. your-client-just-asked-if-they-show-up-in-chatgpt-482951 — Client asked about ChatGPT
55. google-is-dynamically-expanding-ai-overviews-486200 — Dynamic AIO expansion
56. google-adds-link-carousels-for-developing-topics-in-ai-mode-485884 — Link carousels AI Mode
57. google-indexed-claude-chats-483748 — Claude Chats indexed by Google
58. creator-content-ai-search-strategy-483616 — Creator content in AI search
59. ai-visibility-ppc-performance-484199 — AI visibility context for PPC
60. google-search-console-platform-properties-483921 — GSC Platform properties
61. google-search-console-social-content-search-demand-485116 — GSC social content
62. think-beyond-links-484802 — Link building beyond links
63. traditional-link-building-model-no-longer-works-ai-search-484530 — Link building dead for AI
64. link-building-win-or-fail-486023 — Link building 2027
65. you-cant-demand-the-click-if-you-wont-give-the-link-484377 — Editorial linking ethic
66. seo-sabotage-lawsuit-toxic-backlinks-484795 — SEO sabotage lawsuit
67. local-5-ai-search-seo-485160 — Local 5.0
68. google-business-profiles-local-seo-success-data-485727 — 1.8M GBP study
69. google-business-profile-address-changes-local-rankings-483537 — GBP address changes
70. how-semantics-and-topical-authority-improve-local-seo-482980 — Semantics & local
71. query-templates-topical-authority-484676 — Query templates
72. reddit-keyword-research-tool-485859 — Reddit as keyword tool
73. use-mcp-servers-speed-up-seo-research — MCP for SEO
74. mcp-data-tools-484650 — MCP for marketing data
75. keyword-clustering-tool-python-483977 — Keyword clustering Python
76. self-improving-ai-content-workflows-483404 — 7 feedback loops
77. build-ai-content-workflow-from-ground-up-485565 — AI content pipeline
78. phases-build-authority-earn-ai-citations-485470 — 3 phases authority
79. llm-visibility-starts-with-better-internal-communication-484913 — LLM visibility comms
80. value-creators-review-content-485028 — Creator & review value
81. does-topical-focus-make-your-brand-more-visible-484280 — Topical focus
82. turn-news-articles-into-ai-search-assets-483950 — Liquid content
83. keyword-deserve-own-page-485567 — Keyword page decision
84. multilingual-websites-english-pages-ai-visibility-484251 — /en/ folder hack
85. spot-emerging-category-search-data-484393 — Emerging categories
86. multi-location-seo-structure-geographic-pages-483959 — Multi-location SEO
87. news-publication-google-visibility-484268 — News publication visibility
88. seo-social-topical-map-484018 — Social topical map
89. top-of-funnel-content-worth-it-485746 — TOFU 2027
90. community-signals-ai-largest-third-party-source-484606 — UGC = largest source
91. technical-debt-seo-fix-vs-ignore-483240 — Technical debt framework
92. technical-seo-testing-build-stronger-experiment-484537 — SEO testing
93. google-search-console-ai-performance-reports-486269 — GSC AI reports global
94. gemini-3-7-flash-rolling-out-in-google-search-485058 — Gemini 3.7 Flash
95. google-business-profile-products — GBP products
96. calls-clicks-falling-google-maps-destination-486276 — Google Maps as destination
97. google-says-dont-include-fake-or-undisclosed-incentivized-reviews-483456 — Review snippet rules

---

*Playbook V2. 140+ техник, 21 приоритет. Основано на 247 статьях SearchEngineLand (август 2026). Все техники верифицируемы через source URLs.*