# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass


@dataclass
class RentsItem:
    annual_amount: float | None = None
    area_en: str | None = None
    registration_date: str | None = None
    usage_en: str | None = None
