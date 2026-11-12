---
type: API Reference
title: "Sessione: RequestState e contesto della richiesta"
description: "Classi e funzioni di zcs.core.session: RequestState, request_context, AuthInfo, QaInfo, FolliaModule, con campi, valori predefiniti e chi li imposta."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/app/src/zcs/core/session/request_state.py
tags: [sessione, request-state, contextvar, auth-info]
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: state, resource: ../../app/src/zcs/core/session/request_state.py, title: "RequestState", last_modified: 2026-05-13T15:29:36Z }
  - { id: ctx, resource: ../../app/src/zcs/core/session/request_context.py, title: "request_context", last_modified: 2025-10-15T08:50:58Z }
  - { id: auth, resource: ../../app/src/zcs/core/session/auth_info.py, title: "AuthInfo", last_modified: 2025-12-02T13:54:27Z }
  - { id: qa, resource: ../../app/src/zcs/core/session/qa_info.py, title: "QaInfo", last_modified: 2025-12-11T13:51:36Z }
  - { id: module, resource: ../../app/src/zcs/core/session/follia_module.py, title: "FolliaModule", last_modified: 2025-12-04T13:26:01Z }
---

# Sessione (`zcs.core.session`)

Il modulo esporta `request_context`, `RequestState`, `AuthInfo`, `FolliaModule` e `QaInfo`.

## request_context

Un `contextvars.ContextVar` chiamato `"request_state"` con **`default=None`**.[^ctx] Non ha funzioni di supporto: chi usa la libreria chiama `request_context.set(...)` e `request_context.get()`. Cosa succede se il contesto non è stato impostato: vedi [comportamenti](../comportamenti.md), voce "Contesto assente".

## RequestState

Costruttore (tutti i parametri sono opzionali):[^state]

| Parametro | Predefinito | Note |
|---|---|---|
| `request_id` | generato | Se assente: `uuid4`, con prefisso `<prefix>_` se dato `prefix` (`generate_op_code`, r.236) |
| `prefix` | `None` | Usato solo per generare l'id |
| `op_code` | uguale a `request_id` | r.31 |
| `auth_info`, `follia_module`, `qa_info` | `None` | Oggetti descritti sotto |
| `doc_type`, `size`, `total_pages`, `job_id`, `file_id`, `channel` | `None` | |
| `attempts` | `0` | |
| `custom_data` | `{}` | Anche se si passa `None` o un dizionario vuoto (r.43) |

- Alla creazione registra due istanti con `time.perf_counter_ns()`: inizio richiesta e checkpoint (r.32-33).
- Gli attributi sono privati (`self.__x`): si leggono e scrivono con `getX`/`setX`. Le sottoclassi dei servizi devono passare dai getter, non dagli attributi.
- `getRequestId`, `getOpCode`, `getRequestStartNs`, `getCheckpointNs` hanno getter; solo il checkpoint ha il setter (`setCheckpointNs`), usato dal logger a ogni riga. `request_id` e `op_code` non hanno setter.
- Non ci sono controlli sui valori né sincronizzazione tra thread.

## AuthInfo

`@dataclass` con cinque campi, tutti `None` di default: `client_id`, `tenant_id`, `company_id`, `user_id`, `user_email`.[^auth] **Non verifica niente**: chi la compila (di solito il middleware del servizio) decide da dove prendere i valori, vedi [flusso](../flussi/ciclo-di-vita-contesto-richiesta.md).

## QaInfo

`@dataclass` con `agent_id`, `session_id`, `datasource_ids` (lista) e `interaction_id`, tutti `None` di default.[^qa] Dal tag 0.8.0 il campo si chiama `datasource_ids`; prima era `datasource_id` (vedi [versioni](../versioni.md)).

## FolliaModule

`StrEnum` con due valori: `VIRTUAL_ASSISTANT = "virtual_assistant"` e `DATA_EXTRACTION = "data_extraction"`.[^module] La docstring dice "Data class", ma è una enumerazione.

[^ctx]: `request_context.py` r.3.
[^state]: `request_state.py`, costruttore r.12-44.
[^auth]: `auth_info.py` r.5-13.
[^qa]: `qa_info.py` r.5-12.
[^module]: `follia_module.py` r.4-8.
