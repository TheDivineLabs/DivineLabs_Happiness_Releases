# Public Happiness showcase

- This repository contains documentation, public media and publication automation only. Never add application source, private build logs, account data, keys or runtime binaries to Git.
- Binary distribution belongs in GitHub Releases and requires an explicit owner request. Plus stays unpublished until its subscription system and release are approved.
- Generated README, NEWS, data/current.json, news articles, LICENSE and hero assets come from the dedicated public feed. Change public text in the source feed, then sync.
- Do not publish FPS/CPU/memory improvement claims without comparable measurements. EXE size is disk size, not runtime performance.
- The scheduled workflow reads only the committed public-channel in this public repo, using its own GITHUB_TOKEN. Never add access credentials or checkout for the private source repo. Do not add pull_request_target; only trusted maintainers may edit workflows.

- Keep Russian/English navigation, release links and factual claims consistent. English news lives in the source public feed under en/news, with a source_sha256 binding. Use explicit Russian fallback for missing/stale translations. LICENSE remains the actual license; translated explanations are summaries.
