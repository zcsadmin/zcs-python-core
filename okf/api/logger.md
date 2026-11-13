---
type: API Reference
title: "Logger: ZcsLogging e filtro degli endpoint"
description: "ZcsLogging, i due formatter (JSON per Cloud Logging e console) e EndpointFilter: parametri, formato dei log e campi del contesto aggiunti."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/app/src/zcs/core/logger/logger.py
tags: [logger, cloud-logging, formatter, endpoint-filter]
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: logger, resource: ../../app/src/zcs/core/logger/logger.py, title: "ZcsLogging e formatter", last_modified: 2026-04-03T07:58:22Z }
  - { id: filter, resource: ../../app/src/zcs/core/logger/endpoint_filter.py, title: "EndpointFilter", last_modified: 2025-06-27T08:46:03Z }
---

# Logger (`zcs.core.logger`)

Esporta `ZcsLogging` e `EndpointFilter`.

## ZcsLogging

`ZcsLogging(enable_cloud_logging: bool = True, log_level = logging.INFO)`; `get_logger()` restituisce il logger chiamato `zcsapp`.[^logger] L'annotazione di `log_level` è `str`, ma il valore predefinito è un intero (`logging.INFO`).

| Modo | Formato | Quando |
|---|---|---|
| `enable_cloud_logging=True` (predefinito) | una riga JSON per record, con `severity`, `message`, `time`, `logging.googleapis.com/sourceLocation` e `logging.googleapis.com/labels` | servizi nel cluster |
| `enable_cloud_logging=False` | testo `LIVELLO data - messaggio`, con colori per livello; il logger `root` aggiunge `(file:riga)` | sviluppo locale |

Etichette del formato JSON: `logger_name` e `error_code` sempre; `op_code`, `request_id`, `delta_ns`, `total_ns` solo se nel `request_context` c'è un `RequestState` (r.60-69). Nel formato console il contesto diventa un prefisso `[OP_CODE:..][REQ_ID:..]` e un suffisso con i tempi (r.108-110).

`error_code` viene dal codice della `ZcsException` quando il record contiene un'eccezione di quel tipo, nel messaggio o allegata (r.15-27).

Gli effetti globali del costruttore, il significato dei tempi e il messaggio sostituito sono in [comportamenti](../comportamenti.md).

## EndpointFilter

`logging.Filter` che scarta i record il cui messaggio contiene `GET <endpoint>`.[^filter] Gli endpoint predefiniti sono `/health`, `/metrics` e `/info` (r.11). Il confronto è una ricerca di sottostringa nel messaggio già formattato. Il filtro non si applica da solo: il consumatore lo aggiunge al logger che stampa gli accessi.

[^logger]: `logger.py`, `ZcsLogging.__init__` r.117-150.
[^filter]: `endpoint_filter.py` r.8-26.
