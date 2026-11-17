# REVIEW.md — zcs-python-core

> Prima versione scritta da `setup-repo` il 2026-11-17, non ancora controllata da chi conosce il servizio:
> `/pre-pr` propone di correggerla quando sbaglia. Chi la controlla toglie questa riga.

Regole da controllare in review su questo repo. Le usa /pre-pr insieme a /code-review e /security-review;
le regole comuni del laboratorio non si ripetono qui.

## Sempre

1. Un import nuovo di una libreria di terze parti in `app/src` è protetto da `try/except ImportError` con avviso e
   degradazione, come gli import OpenTelemetry e `prometheus_client`; altrimenti la PR lo segnala come dipendenza
   nuova per i consumatori (`okf/libreria.md` §Dipendenze, `okf/questioni-aperte.md` §11).
2. Niente codice nuovo a livello di modulo con effetti globali (istanze lette dall'ambiente, `logging.set*`,
   modifiche al root logger) oltre a quelli già esistenti (`okf/comportamenti.md` §Importazioni con effetti).
3. Il codice che legge `request_context.get()` gestisce il valore `None` (contesto assente)
   (`okf/comportamenti.md` §Contesto assente, `session/request_context.py:3`).
4. I metodi nuovi di `ZcsTelemetry` usati dai servizi a ogni richiesta non fanno salire eccezioni non documentate al
   chiamante; se lo fanno (come `counter_add`), la scheda lo dice (`okf/comportamenti.md` §Contatori,
   `okf/questioni-aperte.md` §3).
5. Un campo nuovo di `RequestState` segue lo schema esistente: parametro opzionale con predefinito in fondo al
   costruttore, attributo privato, coppia `getX`/`setX` (`session/request_state.py`).
6. Una variabile d'ambiente nuova si legge solo tramite `TelemetrySettings` (o un'altra classe `BaseSettings` in
   `zcs.core.settings`), mai con `os.environ`/`getenv` sparsi nel codice (`okf/operativita/configurazione.md`).
7. Ogni modifica a un comportamento pubblico ha un test in `app/tests/zcs/core/` (`okf/questioni-aperte.md` §14).
8. Le schede `okf/` toccate dal cambio (API, comportamenti, configurazione, versioni) sono aggiornate nella stessa PR.

## Sicurezza

9. Nessun dato personale nuovo (email, nome, codice fiscale, contenuto delle richieste) nei tag Loki, nei campi
   del JSON del logger o negli attributi delle tracce; `auth_user_mail` esistente non si estende ad altri campi
   (`okf/questioni-aperte.md` §1, `telemetry/logging.py:28-38`).
10. Credenziali (`grafana_cloud_api_key` e simili) mai nei log, nei messaggi d'errore o negli avvisi, nemmeno
    in parte (`okf/operativita/configurazione.md`).
11. Core non decodifica né valida token: niente decodifica JWT nella libreria senza verifica della firma; `AuthInfo`
    resta un contenitore (`okf/questioni-aperte.md` §2).
12. Nessun valore predefinito non vuoto per indirizzi o credenziali in `TelemetrySettings`
    (`settings/telemetry_settings.py`).

## Compatibilità e rilascio

13. Nessuna rinomina o rimozione di classi, metodi, parametri o campi pubblici (`zcs.core.*`) senza `!` nel commit;
    meglio aggiungere il nome nuovo e tenere il vecchio (precedente `datasource_id` in 0.8.0, `okf/versioni.md`).
14. Nessun cambio di tipo di un campo pubblico (es. valore singolo → lista) senza `!` (`okf/versioni.md`, 0.8.0).
15. I nomi dei campi del JSON del logger (`op_code`, `request_id`, `delta_ns`, `total_ns`, `error_code`, ...)
    non cambiano senza `!`: sono il formato dei log di tutti i consumatori (`okf/api/logger.md`, `logger.py:60-69`).
16. I nomi dei tag Loki e degli attributi delle tracce non cambiano senza `!` (`telemetry/logging.py`,
    `okf/api/telemetria.md`).
17. Un nuovo parametro di funzione o costruttore pubblico è opzionale con predefinito che mantiene il comportamento
    di prima.
18. `app/pyproject.toml`: `version` resta `0.dev0` (la scrive il workflow dal tag, `publish-tag.yaml`).
19. Le modifiche a `publish-tag.yaml` non cambiano il filtro `'*'` sui tag né il registro di destinazione senza dirlo
    nella PR (`okf/operativita/rilascio.md`).

## Da non segnalare

- `pyproject.toml` senza `dependencies`, README superato, `delta_ns`/`total_ns` in secondi, `log_level` annotato
  `str`, lista mutabile in `EndpointFilter`, `alloy_metrics_port` inutilizzato, id dello step `check-prerelease`:
  debito noto in `okf/questioni-aperte.md` (§6, §11-13), da segnalare solo se la PR lo peggiora.
- Getter e setter in camelCase (`getAuthInfo`, `setChannel`) in `RequestState`: convenzione esistente, non va
  convertita in snake_case.
- Nove versioni diverse di core in produzione (`okf/consumatori.md`): non è un problema della PR.
- La PR verso `main` che fa partire `pr_build-and-test.yaml` anche per sola documentazione: voluto, non c'è deploy.
