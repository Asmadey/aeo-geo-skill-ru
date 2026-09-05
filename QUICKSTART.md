# Быстрый старт с AEO & GEO — за 5 минут

Превратите исходный контент в структурированные, готовые к цитированию материалы для поисковых AI-систем менее чем за 5 минут.

---

## Шаг 1: Подготовка поисковых AI-роботов и `llms.txt` (1 минута)

Перед созданием контента убедитесь, что поисковые AI-модели могут обойти и семантически понять ваш домен:
1. **Robots.txt:** Убедитесь, что краулеры `GPTBot`, `PerplexityBot` и `ClaudeBot` не заблокированы (см. [references/bot_access_and_monitoring.md](references/bot_access_and_monitoring.md)).
2. **llms.txt:** Сгенерируйте и опубликуйте семантическую карту в корне вашего сайта:
   ```bash
   python3 scripts/llms_txt_generator.py generate --template saas --name "MyBrand" --url "https://mybrand.com"
   python3 scripts/llms_txt_generator.py validate --file llms.txt
   ```

---

## Шаг 2: Проведение AEO & GEO аудита контента (1 минута)

Оцените готовность материала к извлечению пассажей и прямому ответу:

```bash
# Аудит локального файла статьи
python3 scripts/aeo_audit.py --input your_post.md --industry saas

# Или проверка встроенного образца
python3 scripts/aeo_audit.py --sample
```

**Ключевые проверяемые параметры:**
- **Бюджет ChatGPT Instant:** Содержат ли первые 200 знаков под H1 прямой фактографический ответ?
- **Самодостаточность заголовка для Labrador:** Представляет ли H1 собой информативное предложение (до 289 знаков)?
- **Выживаемость в кэше Markdown:** Насыщены ли атрибуты `alt` у изображений конкретными фактами?
- **Независимость пассажей:** Отсутствуют ли зависимые связки вроде *"как упоминалось выше"*?
- **Риск потери авторства (Ghost Citations):** Привязаны ли статистические показатели к бренду или исследованию?
- **Технический лимит:** Меньше ли сырой HTML-код 4 Мегабайт?

---

## Шаг 3: Исследование запросов и возврат Dark Funnel (1 минута)

Найдите точные формулировки поисковых промптов по воронке (ToFU, MoFU, BoFU), активирующие цитаты в AI:

```bash
python3 scripts/query_researcher.py --topic "Ваша Тема" --region US
```

---

## Шаг 4: Оптимизация структуры и привязка бренда (1 минута)

Запустите сбалансированную оптимизацию: перестройка пассажей, заголовок для Labrador, факты в картинках и привязка бренда:

```bash
python3 scripts/aeo_optimizer.py --input your_post.md --brand "MyBrand" --mode balanced --output your_post_aeo.md
```

Команда автоматически оптимизирует заголовок H1 (до 250 знаков), внедрит микроразметку Schema.org JSON-LD, маркеры источников `[1]`, обогатит alt-тексты картинок и заменит абстрактные фразы на брендированные утверждения.

---

## Шаг 5: Фиксация результатов в 4-статусном журнале (1 минута)

Ведите мониторинг по четырем состояниям (`both` — цитата+бренд, `ghost` — факт без бренда, `mention` — только бренд, `neither` — отсутствие):

```bash
python3 scripts/citation_tracker.py add \
  --url "https://yoursite.com/blog/article" \
  --llm perplexity \
  --query "что такое ваша тема" \
  --status both \
  --brand "MyBrand"

python3 scripts/citation_tracker.py report --url "https://yoursite.com/blog/article"
```

Если коэффициент **Ghost Citation Ratio** превышает 30%, обратитесь к руководству [references/anti_ghost_citation_guide.md](references/anti_ghost_citation_guide.md).

---

## Шаг 6: Построение матрицы обновления страниц Keep / Fix / Remove / Add

Запланируйте аудит и рефреш контента на домене без риска каннибализации и потери URL-истории:

```bash
python3 scripts/report_generator.py --project "МойПортал" --refresh-matrix
```
