# rents_scraper (Scrapy)

Scrapy project for Ejari Rent Transaction Details only.

- Endpoint: `EJARI_URL` env (`POST`, Rent Transaction Details)
- Body: `P_FROM_DATE/P_TO_DATE (MM/DD/YYYY), P_DATE_TYPE, P_TAKE/P_SKIP (strings), P_SORT`
- Paginated, no auth.

## Usage

```bash
cd rents_scraper
uv run scrapy crawl rents -a from_date=09/12/2026 -a to_date=09/13/2026 -O ../output/rents.jsonl
```

Spider: `rents_scraper/rents_scraper/spiders/rents.py` (lowercased response fields).
Prefer `lib/extract/ejari_rents_downloader.py` for pipeline use.
