---
type: Process
title: "Ciclo di vita del contesto della richiesta"
description: "Come il contesto (RequestState in request_context) nasce, viene compilato e letto dal logger e dalla telemetria: cosa fa la libreria e cosa fa ogni servizio."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/app/src/zcs/core/session/request_context.py
tags: [contesto, request-state, middleware, tracciamento]
status: stable
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-10T17:05:00Z }
verified: { by: human:gferro, at: 2026-11-10T17:26:03Z }
sources:
  - { id: ctx, resource: ../../app/src/zcs/core/session/request_context.py, title: "request_context", last_modified: 2025-10-15T08:50:58Z }
  - { id: state, resource: ../../app/src/zcs/core/session/request_state.py, title: "RequestState", last_modified: 2026-05-13T15:29:36Z }
  - { id: logger, resource: ../../app/src/zcs/core/logger/logger.py, title: "Lettura del contesto nel logger", last_modified: 2026-04-03T07:58:22Z }
  - { id: tlog, resource: ../../app/src/zcs/core/telemetry/logging.py, title: "Lettura del contesto per Loki", last_modified: 2026-05-12T08:23:34Z }
  - { id: attrs, resource: ../../app/src/zcs/core/telemetry/set_trace_attributes.py, title: "Lettura del contesto per le tracce", last_modified: 2026-05-12T08:23:34Z }
---

# Ciclo di vita del contesto della richiesta

La libreria **definisce** il contenitore del contesto ma **non lo imposta mai**: nessuna funzione di `zcs.core` chiama `request_context.set`. Lo fanno i servizi, nello stesso modo.[^ctx] Lo schema qui sotto è quello letto nel middleware di aip-data-ingestor-webservice e di aip-generative-ai-webservice (origin/main del 10/11/2026); gli altri consumatori sono in [consumatori](../consumatori.md) e non sono stati letti riga per riga.

## Passi

| # | Chi | Cosa |
|---|---|---|
| 1 | servizio (middleware HTTP o consumer di messaggi) | crea `RequestState(op_code=..., prefix='<SERVIZIO>')`. L'`op_code` può arrivare dalla query (`op_code`) oppure viene generato. |
| 2 | servizio | `request_context.set(request_state)` |
| 3 | servizio | decodifica il JWT dell'intestazione `Authorization`, compila `AuthInfo` (`tenant_id`, `user_id`, `client_id`, e dove serve `company_id`), `setAuthInfo`, `setFolliaModule`, `setCustomData` |
| 4 | servizio | chiama `set_trace_attributes(request_state)` per copiare il contesto sullo span |
| 5 | libreria (logger) | a ogni log legge `request_context.get()`, aggiunge `op_code`, `request_id`, tempo dall'ultimo log e dall'inizio, e **aggiorna il checkpoint**[^logger] |
| 6 | libreria (telemetria) | `LokiContextFilter` legge il contesto per i tag Loki, `set_trace_attributes` per gli attributi della traccia[^tlog][^attrs] |
| 7 | servizio | a fine richiesta calcola il tempo totale da `getRequestStartNs()` |

## Cosa non c'è

- **Nessun `reset`**: nei middleware letti il `set` non è seguito da un `request_context.reset(token)`.
- **Richieste che saltano il contesto**: i middleware letti non impostano il contesto per `/health` e `/metrics`. Chi legge `request_context.get()` in quelle rotte riceve `None`.
- **Thread**: un thread nuovo parte con un contesto vuoto, a meno che chi lo crea non copi il contesto. Nei consumer che creano thread non è stato verificato (da verificare).

## Dove cambia da servizio a servizio

Alcuni servizi usano `RequestState` direttamente, altri una sottoclasse (`AppCustomRequestState`, `TeseoMcpRequestState`) con campi propri. I campi aggiuntivi non sono noti alla libreria.

[^ctx]: `request_context.py`: solo la definizione del `ContextVar`.
[^logger]: `logger.py` r.60-69 e r.103-110.
[^tlog]: `telemetry/logging.py` r.25-48.
[^attrs]: `set_trace_attributes.py` r.46-66.
