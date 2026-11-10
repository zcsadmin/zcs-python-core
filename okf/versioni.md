---
type: Version History
title: "Storia delle versioni"
description: "Tag di zcs-python-core dal 2025: data, cosa cambia nel codice, modifiche non retrocompatibili e vincoli noti dal codice."
resource: https://github.com/zcsadmin/zcs-python-core/tags
tags: [versioni, tag, release]
status: stable
generated: { by: claude-code/claude-sonnet-5-5, at: 2026-11-10T17:05:00Z }
verified: { by: human:gferro, at: 2026-11-10T17:26:03Z }
sources:
  - { id: git, resource: "git log e git diff tra i tag della repo, letti il 2026-11-10", title: "Storia dei tag" }
  - { id: rel, resource: "gh release list e gh api repos/zcsadmin/zcs-python-core/releases, 2026-11-10", title: "Release GitHub e stato pre-release" }
  - { id: publish, resource: ../.github/workflows/publish-tag.yaml, title: "Workflow dei tag", last_modified: 2026-07-23T09:21:16Z }
  - { id: qa, resource: ../app/src/zcs/core/session/qa_info.py, title: "QaInfo", last_modified: 2025-12-11T13:51:36Z }
---

# Storia delle versioni

La data è quella del commit del tag (`git log -1 --format=%cs <tag>`). "Cosa cambia" è letto dalle differenze nel codice (`app/src`) tra un tag e il precedente. La colonna "vincoli noti dal codice" riporta **solo ciò che il codice dice**: nessuna deduzione dai numeri AP nei messaggi di commit.[^git]

| Tag | Data | Commit | Cosa cambia | Vincoli noti dal codice |
|---|---|---|---|---|
| 0.3.0 | 27/06/2025 | `ec0be53` | `EndpointFilter` | nessuno |
| 0.4.0-rc1, rc2 | 13/10/2025 | `1769345`, `4d5f91d` | rc di 0.4.0 (contenuto non confrontato: da verificare) | — |
| 0.4.0 | 15/10/2025 | `38eed47` | prima versione di `RequestState` e `request_context`; formato JSON con `op_code`, `request_id`, tempi | nessuno |
| 0.4.1 | 23/10/2025 | `3be72f5` | dati aggiuntivi nel formato JSON del logger | nessuno |
| 0.5.0 | 02/12/2025 | `f3145a2` | `AuthInfo` | nessuno |
| 0.5.1 | 02/12/2025 | `48e0b4e` | `setAuthInfo` | nessuno |
| 0.6.0 | 04/12/2025 | `5be26dd` | `FolliaModule` | nessuno |
| 0.7.0 | 10/12/2025 | `10ce223` | `QaInfo` (con `datasource_id`) | nessuno |
| 0.7.1 | 10/12/2025 | `b72e3e4` | `doc_type` | nessuno |
| 0.8.0 | 19/12/2025 | `1adfd72` | `size`, `total_pages`; **`QaInfo.datasource_id` rinominato `datasource_ids` (lista)** | **Non retrocompatibile nel codice**: chi costruisce `QaInfo(datasource_id=...)` o legge `.datasource_id` si rompe. Il commit (`60b5fae`, "change datasource ids") non ha `!`.[^qa] |
| 0.9.0 | 23/12/2025 | `83e97e3` | `job_id`, `file_id` | nessuno |
| 0.10.0 | 21/01/2026 | `b522578` | `attempts` | nessuno |
| 0.10.1 | 10/02/2026 | `05b0df8` | `custom_data` | nessuno |
| 0.10.2-rc1, rc2 | 03/04/2026 | `f3a3690`, `fcb1247` | rc1: contenuto non confrontato (da verificare); rc2: il commit è «ci: create release on tag» (il workflow crea la release sul tag) | — |
| 0.10.2 | 07/04/2026 | `1d359f2` | `logger.py`: protezione per i log OpenTelemetry | nessuno |
| 0.11.0-rc1 | 12/05/2026 | `c6c2a6f` | rc della telemetria | — |
| 0.11.0 | 13/05/2026 | `865d042` | **telemetria**: `ZcsTelemetry`, `setup_logging`, `set_trace_attributes`, `TelemetrySettings` | `requirements.txt` aggiunge `pydantic_settings`; i moduli `telemetry` e `settings` lo importano |
| 0.11.1 | 13/05/2026 | `3438808` | `RequestState.channel` (`getChannel`, `setChannel`) | nessuno |
| **0.11.2** | 13/05/2026 (commit); release GitHub del 23/07/2026 | `3438808` | **stesso commit di 0.11.1**: stesso codice | non contiene `label_names` (vedi sotto) |
| 0.11.2-rc1, rc2 | 23/07/2026 | `c7bbaa3` | `counter_create(..., label_names=None)` e contatore Prometheus con etichette | — |
| 0.11.3 | 23/07/2026 | `3f3eb95` | merge del fix delle etichette, `build` 1.5.0, `pytest` 9.1.1, `pydantic_settings` 2.14.2, `prometheus_client` 0.25.0 | `prometheus_client` entra nei requisiti di sviluppo |
| 0.11.4 | 23/07/2026 | `8d0cda4` | solo `publish-tag.yaml` (controllo pre-release); nessun cambio in `app/src` | nessuno |

## Note

- **Esiste un tag `0.11.2` finale.** Punta allo stesso commit di `0.11.1` (`3438808`) e **non contiene** il fix delle etichette (`494d4d8`), che è invece in `0.11.2-rc1`, `0.11.2-rc2` e `0.11.3`. Il workflow del tag `0.11.2` è terminato con successo il 23/07/2026 e la release GitHub risulta pre-release.[^rel] Per l'ordine delle versioni `0.11.2` è maggiore di `0.11.2-rc2`, ma ha meno codice.
- **Nessun commit** con `!` dopo il tipo, `BREAKING` o `BREAKING CHANGE` nel messaggio (ricerca su tutta la storia con `git log --grep`). L'unica modifica non retrocompatibile letta nel codice è la rinomina di `datasource_id` in 0.8.0.
- Le rc 0.10.2 e 0.11.0 hanno data diversa dal tag finale; le rc 0.11.2 sono state create dopo il tag `0.11.2` (stesso giorno).
- Non c'è `CHANGELOG`: la storia sta nei commit e nelle release generate automaticamente dal workflow.[^publish]
- Per i tag, lo stato pre-release delle release GitHub è in [rilascio](operativita/rilascio.md).

[^git]: Date e commit da `git log -1 --format=%cs <tag>^{commit}`; differenze da `git diff --stat` e `git show`.
[^qa]: `qa_info.py` r.11 al tag corrente; differenza in `git show 60b5fae`.
[^rel]: `gh api repos/zcsadmin/zcs-python-core/releases/tags/0.11.2` e `gh run list --workflow=publish-tag.yaml`.
[^publish]: `publish-tag.yaml`, step "Create GitHub Release" con `generate_release_notes: true`.
