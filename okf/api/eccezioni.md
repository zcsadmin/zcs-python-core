---
type: API Reference
title: "Eccezioni: ZcsException"
description: "ZcsException: parametri, codice di errore casuale, serializzazione con get_as_dict e legame con il logger."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/app/src/zcs/core/exception/exception.py
tags: [eccezioni, zcs-exception, error-code]
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: exc, resource: ../../app/src/zcs/core/exception/exception.py, title: "ZcsException", last_modified: 2025-10-15T08:50:58Z }
  - { id: logger, resource: ../../app/src/zcs/core/logger/logger.py, title: "Uso del codice di errore nel logger", last_modified: 2026-04-03T07:58:22Z }
---

# Eccezioni (`zcs.core.exception`)

Esporta `ZcsException`, l'eccezione usata dai servizi Follia per errori da mostrare all'utente.

## Costruttore

`ZcsException(user_message="Unknown error.", error_source="Unspecified", status_code=500, internal_message=None)`.[^exc]

| Campo | Getter | Note |
|---|---|---|
| `user_message` | `get_user_message()` | Testo passato anche a `Exception.__init__` |
| `error_source` | `get_error_source()` | Chi ha generato l'errore |
| `status_code` | `get_status_code()` | Predefinito 500 |
| `internal_message` | `get_internal_message()` | Dettaglio non pensato per l'utente |
| codice errore | `get_error_code()` | 5 caratteri casuali tra maiuscole e cifre, generati a ogni istanza (r.18) |

- `get_as_dict()` restituisce `error_code`, `user_message`, `internal_message`, `error_source`, `status_code` e **`traceback`** (testo completo). Chi lo inoltra a un client deve scegliere cosa mostrare: `internal_message` e `traceback` non sono pensati per l'esterno.
- `str(exc)` ha la forma `<codice> - <sorgente> - <messaggio interno> - <messaggio utente>`.
- Il codice è casuale, non derivato dall'errore: due errori uguali hanno codici diversi.

## Legame con il logger

Il logger legge il codice dell'eccezione e lo scrive nell'etichetta `error_code` del log JSON.[^logger] Dettagli in [logger](logger.md).

[^exc]: `exception.py` r.7-46.
[^logger]: `logger.py` r.12-32, funzione `record_factory`.
