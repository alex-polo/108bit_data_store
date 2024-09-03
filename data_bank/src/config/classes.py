from dataclasses import dataclass

from selenium.webdriver.chrome.options import Options


@dataclass
class DatabaseConfig:
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


@dataclass
class CeleryConfig:
    LOGGING_CONFIG: str
    BROKER: str
    BACKEND: str
    SCHEDULER_TIME: int


@dataclass
class StorageConfig:
    use_cloud: bool
    use_local_directory: bool
    url_yandex_disk: str
    storage_folder: str


@dataclass
class UserConfig:
    username: str
    password: str
    resetting_user: bool
    is_superuser: bool
    is_news_bot: bool
    is_instruktor_bot: bool


@dataclass
class AdminUserConfig(UserConfig):
    pass


@dataclass
class NewsBotUserConfig(UserConfig):
    pass


@dataclass
class InstructorBotUserConfig(UserConfig):
    pass


@dataclass
class AuthConfig:
    auth_secret_key: str


@dataclass
class BrowserChromeConfig:
    options: Options
    load_strategy: str
    driver_path: str
    port: int
    timeout: int


@dataclass
class ServerConfig:
    version: str
    https: bool


@dataclass
class FormatPostParamsConfig:
    formatting_min_len_title: int
    formatting_len_title: int
    formatting_min_len_details: int
    formatting_len_details: int
    main_tag_news: str
    number_of_days_to_view_sites: int
    number_days_search_post: int
    post_matcher_ratio: int
    len_loaded_content: int
