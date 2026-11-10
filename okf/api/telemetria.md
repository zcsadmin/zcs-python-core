---
type: API Reference
title: "Telemetria: ZcsTelemetry, setup_logging, set_trace_attributes"
description: "Cosa offre zcs.core.telemetry: inizializzazione con OTLP o Alloy, contatori, strumentazione FastAPI, log verso Loki e attributi delle tracce."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/app/src/zcs/core/telemetry/zcs_telemetry.py
tags: [telemetria, opentelemetry, prometheus, loki, alloy, grafana]
status: stable
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-10T17:05:00Z }
verified: { by: human:gferro, at: 2026-11-10T17:26:03Z }
sources:
  - { id: tel, resource: ../../app/src/zcs/core/telemetry/zcs_telemetry.py, title: "ZcsTelemetry", last_modified: 2026-07-23T09:06:44Z }
  - { id: log, resource: ../../app/src/zcs/core/telemetry/logging.py, title: "setup_logging e LokiContextFilter", last_modified: 2026-05-12T08:23:34Z }
  - { id: attrs, resource: ../../app/src/zcs/core/telemetry/set_trace_attributes.py, title: "set_trace_attributes", last_modified: 2026-05-12T08:23:34Z }
  - { id: sett, resource: ../../app/src/zcs/core/settings/telemetry_settings.py, title: "TelemetrySettings", last_modified: 2026-05-12T08:23:34Z }
  - { id: test, resource: ../../app/tests/zcs/core/telemetry/telemetry_test.py, title: "Test della telemetria", last_modified: 2026-07-23T09:06:44Z }
---

# Telemetria (`zcs.core.telemetry`)

Esporta `ZcsTelemetry`, `setup_logging` e `set_trace_attributes`. Le impostazioni stanno in `zcs.core.settings.telemetry_settings` (vedi [configurazione](../operativita/configurazione.md)). Il modulo esiste dal tag 0.11.0.

## ZcsTelemetry

`ZcsTelemetry(telemetry_settings, logger, service_name="zcs-app", service_version="0.0.0", service_environment="undefined")`. Il costruttore chiama subito `_initialize_telemetry`.[^tel]

**Quando si attiva** (r.125-232):

| Condizione | Effetto |
|---|---|
| né OTLP né Alloy configurati | avviso nel log e telemetria **non** inizializzata (r.132) |
| pacchetti `opentelemetry-*` mancanti | avviso e telemetria non inizializzata (r.258-271) |
| OTLP configurato (`has_otlp_config`) | metriche (`/v1/metrics`, esportate a intervallo) e tracce (`/v1/traces`) verso `grafana_otlp_url` con intestazione Basic (r.149-184) |
| Alloy configurato (`has_alloy_config`) | metriche tramite endpoint Prometheus `/metrics` (nessun esportatore OTLP delle metriche), tracce e log verso Alloy in gRPC, con un handler di log aggiunto al logger `root` (r.186-226) |
| entrambi | si attivano tutti e due i rami |

La telemetria risulta attiva (`is_telemetry_enabled()`) se almeno un ramo è partito (r.229-230). `get_meter()` e `get_tracer()` restituiscono `None` e avvisano se non è attiva.

**Metodi**

| Metodo | Cosa fa |
|---|---|
| `instrument_fastapi_app(app)` | strumenta l'app FastAPI con OpenTelemetry e `prometheus_fastapi_instrumentator` ed espone `/metrics` (r.37-57). Non fa nulla se la telemetria non è attiva o se i pacchetti mancano; una stessa app si strumenta una volta sola. |
| `counter_create(name, unit, description, label_names=None)` | crea il contatore su ogni meter OTLP e, con Alloy, un `Counter` Prometheus con nome sicuro (`.` e `-` diventano `_`) e le etichette date (r.74-94) |
| `counter_add(name, data=None)` | incrementa. `data` può essere un dizionario di etichette, con `value` numerico opzionale come quantità (r.96-123) |

Comportamenti d'errore di `counter_add` e `counter_create`: [comportamenti](../comportamenti.md).

## setup_logging

`setup_logging(logging_context: ZcsLogging, app_name, app_version, app_environment)` aggiunge al logger `zcsapp` un handler Loki in coda (`LokiQueueHandler`) **solo se** `has_loki_config`; altrimenti scrive un avviso (r.56-76).[^log] Tag fissi dello stream: `service`, `env`, `version`. Il filtro `LokiContextFilter` aggiunge tag dinamici dal contesto: i campi e le condizioni sono in [comportamenti](../comportamenti.md).

## set_trace_attributes

`set_trace_attributes(request_state=None, *, app_name, app_environment, app_version, extra_attributes)` scrive sullo span corrente gli attributi dell'app e quelli del contesto (`request_op_code`, `request_request_id`, `request_follia_module`, `auth_*`).[^attrs] Non fa nulla se OpenTelemetry non è installato, se lo span non è valido o se il valore è `None`; usa `request_context.get()` se non riceve lo stato. Con contesto assente scrive solo gli attributi dell'app e quelli extra.

## Test

I test esistenti coprono le impostazioni e la creazione di contatori con etichette in modalità Alloy.[^test]

[^tel]: `zcs_telemetry.py`.
[^log]: `telemetry/logging.py`.
[^attrs]: `set_trace_attributes.py` r.17-66.
[^test]: `telemetry_test.py`.
