---
type: Deployment
title: "Rilascio e prove in locale"
description: "Come si pubblica zcs-python-core: workflow della PR e del tag, cosa non parte con un push su main, stato pre-release delle release lette, bug dell'identificativo, prove in locale."
resource: https://github.com/zcsadmin/zcs-python-core/blob/main/.github/workflows/publish-tag.yaml
tags: [rilascio, workflow, artifact-registry, tag, test]
generated: { by: claude-code/claude-sonnet-5-5 }
sources:
  - { id: publish, resource: ../../.github/workflows/publish-tag.yaml, title: "Pubblicazione sul tag", last_modified: 2026-07-23T09:21:16Z }
  - { id: pr, resource: ../../.github/workflows/pr_build-and-test.yaml, title: "Build e test sulle PR", last_modified: 2026-07-23T09:06:44Z }
  - { id: docker, resource: ../../.build/dockerfiles/Dockerfile, title: "Immagini dev e dist", last_modified: 2026-07-23T09:06:44Z }
  - { id: run, resource: ../../run.sh, title: "Script di sviluppo", last_modified: 2024-11-21T15:07:01Z }
  - { id: local, resource: ../../docs/LOCAL_DEVELOPMENT.md, title: "Sviluppo locale", last_modified: 2025-06-27T08:46:03Z }
  - { id: rel, resource: "gh release list e gh api .../releases/tags/<tag>, 2026-11-10", title: "Stato pre-release delle release" }
---

# Rilascio

## Workflow

| Workflow | Quando parte | Cosa fa |
|---|---|---|
| `pr_build-and-test.yaml` | PR verso `main` | costruisce l'immagine `dist` e lancia `pytest` al suo interno.[^pr] Nessun filtro sui percorsi: parte anche per PR di sola documentazione. |
| `publish-tag.yaml` | push di qualunque tag (`'*'`) | autentica su Google Cloud, scrive il nome del tag in `pyproject.toml`, costruisce la wheel, la carica su Artifact Registry (repository `python`, europe-west1) con `twine`, poi crea la release GitHub con note generate.[^publish] |

- **Un push su `main` non lancia nessun workflow**: non costruisce, non pubblica, non fa deploy. Non esiste `paths-ignore` e non serve, perché non c'è un trigger `push` su branch. Un push di sola documentazione non ripubblica nulla.
- **Un tag pubblica sempre**: anche una rc (`X.Y.Z-rcN`) viene caricata nel registro, perché il filtro è `'*'`.
- Non esistono ambienti sandbox, develop o produzione per la libreria: i servizi la scelgono con la riga `zcs-python-core==<versione>` nei propri requisiti.

## Formato dei tag

`X.Y.Z` senza `v`; le rc sono `X.Y.Z-rcN`. Vedi [versioni](../versioni.md).

## Stato pre-release delle release GitHub

Lettura del 10/11/2026 con `gh release list` e `gh api`:[^rel]

| Release | `prerelease` |
|---|---|
| 0.11.4 | **no** (è la "Latest") |
| 0.11.3 | sì |
| 0.11.2 | sì |
| 0.11.2-rc2, 0.11.2-rc1 | sì |
| 0.11.1 | sì |
| 0.11.0, 0.11.0-rc1 | sì |
| 0.10.2, 0.10.2-rc2 | sì |
| 0.10.1 e precedenti (fino a 0.7.1) | no |

### Identificativo dello step: r.64 contro r.77

Nel workflow `publish-tag.yaml` lo step ha `id: check-prerelease` (r.64, con il trattino), ma la release legge `steps.check_prerelease.outputs.prerelease` (r.77, con il trattino basso).[^publish] I due nomi sono diversi.

- **Letto**: `0.11.4` è il primo tag costruito con questo workflow (commit `8d0cda4`) e la sua release **non** è marcata pre-release.
- **Dedotto**: l'uscita `prerelease` è vuota perché lo step non si chiama come scritto a r.77; la release risulta quindi "non pre-release" qualunque sia il nome del tag.
- **Letto (file ai tag)**: ai tag `0.11.2-rc1`, `0.11.2-rc2`, `0.11.2` e `0.11.3` il workflow aveva `id: check_prerelease` (corretto) ma il filtro `^X.Y.Z-N$`, che non riconosce né `-rcN` né `X.Y.Z`: l'uscita è sempre `prerelease=true`. Per questo `0.11.2` e `0.11.3`, versioni finali, risultano pre-release.
- **Dedotto**: una nuova rc, creata con il workflow attuale, risulterebbe **non** pre-release. Non c'è ancora una rc creata con questo workflow.

Le release servono a leggere le note generate; i servizi scelgono la versione dai requisiti, non dallo stato della release.

## Prove in locale

Dal [README del repo](../../README.md) e da `docs/LOCAL_DEVELOPMENT.md`:[^local]

| Comando | Cosa fa |
|---|---|
| `./run.sh -t` | lancia `pytest` nel container di sviluppo (installa i requisiti, costruisce e installa la libreria in modalità editabile) |
| `./run.sh -i` | costruisce l'immagine `dist` e lancia `pytest` al suo interno, come la PR |
| `./run.sh -s` | apre una shell nel container |
| `./run.sh -v`, `-h` | più dettagli, aiuto |

Le immagini partono da `zcscompany/python:3.13-dev` e `zcscompany/python:3.13-dist`.[^docker]

[^pr]: `pr_build-and-test.yaml` r.1-26.
[^publish]: `publish-tag.yaml`, r.64 (`id: check-prerelease`) e r.77 (`steps.check_prerelease`).
[^rel]: Lettura del 10/11/2026.
[^local]: `docs/LOCAL_DEVELOPMENT.md`; opzioni in `run.sh` (`getopts stvih`).
[^docker]: `Dockerfile`, stage `dev` e `dist`.
