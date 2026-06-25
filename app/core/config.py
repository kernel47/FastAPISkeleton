from functools import lru_cache
from typing import List

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    app_name: str = "netbackup-proxy-api"
    app_env: str = "local"
    app_debug: bool = False
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = ["http://localhost:8000"]
    log_level: str = "INFO"

    referential_base_url: str = "https://referential.example.local"
    referential_token: str = ""
    referential_token_header: str = "Authorization"
    referential_token_prefix: str = "Bearer"
    referential_master_servers_path: str = "/api/netbackup/master-servers"
    referential_master_server_path: str = "/api/netbackup/master-servers/{hostname}"

    netbackup_login_path: str = "/netbackup/login"
    netbackup_policies_path: str = "/netbackup/config/policies"
    netbackup_policy_detail_path: str = "/netbackup/config/policies/{policy_name}"
    netbackup_jobs_path: str = "/netbackup/admin/jobs"
    netbackup_job_detail_path: str = "/netbackup/admin/jobs/{job_id}"
    netbackup_images_path: str = "/netbackup/catalog/images"
    netbackup_image_detail_path: str = "/netbackup/catalog/images/{image_id}"
    netbackup_token_header: str = "Authorization"
    netbackup_token_prefix: str = "Bearer"
    netbackup_default_page_size: int = 100

    http_timeout_seconds: int = 30
    http_verify_tls: bool = True

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
