from zcs.core.settings.telemetry_settings import TelemetrySettings


def test_telemetry_settings_otlp_and_loki_flags() -> None:
    settings = TelemetrySettings(
        grafana_otlp_url="https://example.com",
        grafana_loki_url="https://loki.example.com",
        grafana_cloud_api_key="token",
    )

    assert settings.has_otlp_config
    assert settings.has_loki_config
