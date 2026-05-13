from pydantic_settings import BaseSettings, SettingsConfigDict


class TelemetrySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='settings/telemetry-settings.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    grafana_loki_url: str = ""
    grafana_loki_instance_id: str = ""
    grafana_otlp_url: str = ""
    grafana_otlp_instance_id: str = ""
    grafana_cloud_api_key: str = ""
    metrics_export_interval_millis: int = 60_000

    alloy_host: str = ""
    alloy_insecure: bool = False
    alloy_port: int = 4317
    alloy_metrics_port: int = 4318

    @property
    def has_otlp_config(self) -> bool:
        return bool(self.grafana_otlp_url and self.grafana_cloud_api_key)

    @property
    def has_loki_config(self) -> bool:
        return bool(self.grafana_loki_url and self.grafana_cloud_api_key)

    @property
    def has_alloy_config(self) -> bool:
        return bool(self.alloy_host and self.alloy_port)


telemetry_settings = TelemetrySettings()
