---
type: Configuration
title: "Configurazione della telemetria"
description: "Variabili d'ambiente di TelemetrySettings (solo nomi e predefiniti), file letto, campi non usati; il resto della libreria non legge variabili."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/app/src/zcs/core/settings/telemetry_settings.py
tags: [configurazione, telemetria, variabili-ambiente]
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: sett, resource: ../../app/src/zcs/core/settings/telemetry_settings.py, title: "TelemetrySettings", last_modified: 2026-05-12T08:23:34Z }
  - { id: tel, resource: ../../app/src/zcs/core/telemetry/zcs_telemetry.py, title: "Uso delle impostazioni", last_modified: 2026-07-23T09:06:44Z }
---

# Configurazione

L'unico punto in cui la libreria legge configurazione è `TelemetrySettings` (`pydantic_settings.BaseSettings`).[^sett] Nel codice non ci sono letture di `os.environ` o `getenv`. `ZcsLogging` e `ZcsTelemetry` ricevono i loro parametri dal chiamante, non dall'ambiente. Qui solo **nomi e predefiniti**, mai valori.

## Come si legge

- Le variabili si chiamano come i campi, senza distinzione tra maiuscole e minuscole (comportamento standard di `pydantic_settings`, dedotto): per esempio `GRAFANA_LOKI_URL`.
- In più legge il file **`settings/telemetry-settings.env`**, con percorso **relativo alla cartella da cui parte il processo** (`env_file`, r.6); i campi sconosciuti sono ignorati (`extra='ignore'`).
- `telemetry_settings = TelemetrySettings()` è creata all'**import** del modulo (r.36): il file e le variabili si leggono una volta sola, all'avvio.

## Campi

| Campo | Predefinito | A cosa serve | Dove è usato |
|---|---|---|---|
| `grafana_loki_url` | vuoto | indirizzo di Loki; se manca niente handler Loki | `has_loki_config`, `setup_logging` |
| `grafana_loki_instance_id` | vuoto | utente dell'autenticazione verso Loki | `setup_logging` |
| `grafana_otlp_url` | vuoto | base degli indirizzi OTLP (`/v1/metrics`, `/v1/traces`) | `has_otlp_config`, `ZcsTelemetry` |
| `grafana_otlp_instance_id` | vuoto | utente dell'intestazione Basic verso OTLP | `ZcsTelemetry._build_basic_auth_header` |
| `grafana_cloud_api_key` | vuoto | credenziale di Grafana Cloud, usata per OTLP e Loki (segreto) | `has_otlp_config`, `has_loki_config`, autenticazione |
| `metrics_export_interval_millis` | `60000` | intervallo di esportazione delle metriche OTLP | `ZcsTelemetry` r.159 |
| `alloy_host` | vuoto | host di Alloy | `has_alloy_config`, indirizzo gRPC di tracce e log |
| `alloy_insecure` | `False` | connessione gRPC senza TLS | esportatori verso Alloy |
| `alloy_port` | `4317` | porta gRPC di Alloy | `has_alloy_config`, indirizzo gRPC |
| `alloy_metrics_port` | `4318` | **non usato**: letto solo da `_build_alloy_metrics_endpoint`, che nessuno chiama | — |

## Condizioni derivate

| Proprietà | Vera quando |
|---|---|
| `has_otlp_config` | `grafana_otlp_url` e `grafana_cloud_api_key` valorizzati |
| `has_loki_config` | `grafana_loki_url` e `grafana_cloud_api_key` valorizzati |
| `has_alloy_config` | `alloy_host` e `alloy_port` valorizzati (con `alloy_port` predefinito 4317, basta `alloy_host`) |

La telemetria si attiva se è vera `has_otlp_config` o `has_alloy_config` (vedi [telemetria](../api/telemetria.md)).

## Non configurabile da ambiente

Livello dei log, modo cloud o console e filtri degli endpoint sono parametri dei costruttori ([logger](../api/logger.md)); nome, versione e ambiente del servizio per la telemetria sono parametri di `ZcsTelemetry` e di `setup_logging`.

[^sett]: `telemetry_settings.py` r.4-36.
