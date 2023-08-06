from enum import Enum


__all__ = 'API_URL', 'Culture'

API_URL: str = 'https://www.delivery-auto.com/api/v4/Public/{command}'


class Culture(str, Enum):
    UA = 'uk-UA'
    US = 'en-US'
    RU = 'ru-RU'
