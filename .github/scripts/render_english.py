"""English product documentation; downloads come from the same release metadata."""
import re


def render_english(put, meta, client, news, translations, hero_svg):
    links = meta['links']; build = meta['build']; base = 'https://github.com/' + meta['repository']
    put('assets/hero.en.svg', hero_svg.replace('Клиент MusicWars для Windows.', 'MusicWars client for Windows.').replace('УСТАНОВЩИК EXE  ·  PORTABLE ZIP', 'EXE SETUP  ·  PORTABLE ZIP'))
    lines = []
    for original in news:
        name = original['file']; translated = translations.get(name)
        if translated:
            title = translated['title']; target = 'news/en/' + name
            put(target, f"[Русский](../{name}) · English\n\n# {title}\n\n{translated['date']} · {translated['version']}\n\n{translated['body']}\n")
        else:
            title = 'Update ' + original['version'] + ' (Russian)'; target = 'news/' + name
            put('news/en/' + name, f"[Русский](../{name}) · [English news](../../NEWS.en.md)\n\n# Translation unavailable\n\n[Read the current Russian article](../{name}).\n")
        lines.append(f"- **{original['date']} · {original['version']}** - [{title}]({target})")
    latest = '\n\n'.join(lines[:3])
    put('NEWS.en.md', '[Русский](NEWS.md) · English\n\n# Happiness news\n\nCompleted changes and prepared builds. A news entry does not mean its downloads have been published.\n\n' + '\n\n'.join(lines) + '\n')
    if client:
        downloads = f"**[EXE installer]({client['installer']['url']})** · **[Portable ZIP]({client['portable']['url']})**\n\nPublished version: **{client['tag']}**. [Release notes and checksums]({client['page']})."
    else:
        downloads = f"Public downloads are not available yet. Prepared build: **{build['version']} Preview**."
    put('README.en.md', f'''[Русский](README.md) · **English**

<img src="assets/hero.en.svg" width="100%" alt="DivineLabs Happiness - MusicWars client for Windows" />

# DivineLabs Happiness

MusicWars client for Windows. Available as an installer and a portable archive.

**[Download](#download)** · **[News](NEWS.en.md)** · **[Getting started](docs/en/getting-started.md)** · **[Support](#support)**

## Download

{downloads}

Preview release. Full gameplay testing is still in progress.

## Features

- Resizable game window, fullscreen mode and keyboard shortcuts.
- A side panel opened with the movable DivineLabs logo.
- Four themes: Orbit, Signal, Paper and Control.
- Game screenshots without the client's overlay controls.
- Minimize to the system tray.
- Local recording of technical performance data.
- Open email links inside the client.

## Client and Plus

Client is a standalone game client. Plus includes additional gameplay modules and has not been published. Subscriptions are not available yet.

## Performance

The main EXE of prepared version {build['version']} is **{build['clientExeBytes']/1048576:.2f} MiB**. Browser components are included separately in the installer and portable archive.

Comparative FPS, CPU and memory benchmarks have not been published. [File sizes and measurements](docs/en/performance.md).

## Recent updates

{latest}

[All news](NEWS.en.md)

## Support

**[DivineLabs Discord]({links['discord']})** · **[Author on Telegram]({links['author']})** · **[GitHub]({links['github']})**

[Report an issue]({base}/issues/new/choose) with your app version, Windows version and steps to reproduce it. Reports in Russian or English are welcome.

## License

Happiness uses [proprietary terms](LICENSE). Personal use and testing of official builds are permitted. Redistribution and resale of original project materials require the rights holder's permission. [English summary](docs/en/license.md).

This repository contains product documentation, news and releases. Application source code is not published here.

Independent, unofficial project. MusicWars and game assets belong to their respective rights holders.
''')
    selected = re.match(r'^v?(\d+)\.(\d+)\.(\d+)', client['tag'] if client else build['version'])
    bundled = bool(selected and tuple(map(int, selected.groups())) >= (0, 2, 9))
    runtime = ('The VK sign-in component is included in the installer and portable archive. A separate WebView2 installation is not needed. You may need to sign in again when switching to the bundled component.' if bundled else 'VK sign-in requires an installed Microsoft Edge WebView2 Runtime. The owner verified sign-in in Client 0.2.8.')
    put('docs/en/getting-started.md', f'''[Русский](../getting-started.md) · English

# Getting started

{'Download Client from the main page or Releases.' if client else 'Public downloads have not been published yet.'}

1. Choose the EXE installer or the portable ZIP.
2. Update installed copies in the same folder. Keep the entire `Data` folder when moving or updating a portable copy.
3. Extract the complete portable archive and run `DivineLabs.Happiness.exe` from its root.
4. Settings, sign-in profiles and screenshots are stored in `Data`.

{runtime} Sound is disabled.

Uninstalling preserves user data by default. Full removal is a separate option. Installation, upgrade and removal were tested on disposable installations; later package checks verify the packaged files and installer integrity.

This is a preview. Report problems through Issues or Discord, including steps to reproduce them.
''')
    sizes = meta['sizeComparison']
    put('docs/en/performance.md', f'''[Русский](../performance.md) · English

# Performance and measurements

Recorded main EXE sizes for version {sizes['version']}:

| | Client | Plus |
| --- | --- | --- |
| Main EXE | {sizes['clientExeBytes']/1048576:.2f} MiB | {sizes['plusExeBytes']/1048576:.2f} MiB |

The editions contain different modules. File size is not a measure of FPS, CPU usage or RAM usage. Browser components add to the total download and installation size.

The app can record technical measurements for 60 seconds. Recording is disabled by default. Reports are saved locally under `Data/Diagnostics/Performance` and are not uploaded automatically.

Reports include CPU usage, memory and available Flash frame intervals. Game logic events are not equivalent to displayed frames; they are not reported as visible FPS.

Comparable browser benchmarks and graphics optimization results have not been published. Comparisons need the same scene, window size and cache state, a warm-up period and repeated runs.
''')
    put('docs/en/license.md', '''[Русский](../license.md) · English

# License summary

**DivineLabs Happiness Proprietary License** (`LicenseRef-DivineLabs-Happiness-Proprietary`) is the project's custom proprietary license, not MIT or an open-source license.

Lawful recipients of official builds may install and run them for personal use and testing. Exclusive rights to the project's original materials remain with their rights holder, DivineLabs / TheDivineLabs.

Without separate written permission, publishing or distributing the project's own source code or builds, resale, sublicensing, inclusion in other products and distribution of modified original project components are prohibited.

Receiving a build or repository access does not transfer exclusive rights. Third-party components and game assets retain their own owners and terms. Mandatory legal rights and previously valid permissions remain unaffected.

This page is an English summary. See the complete Russian [LICENSE](../../LICENSE) for the actual terms and their scope.
''')
    put('docs/en/automation.md', '''[Русский](../automation.md) · English

# How this repository is updated

Maintainers publish approved news and prepared-build metadata from their workstation after pushing the main source branch. Existing GitHub authentication is used; this public repository has no credentials to read the private application repository.

The local publisher exports only the dedicated public feed from the pushed commit. Uncommitted drafts and application source are excluded. It generates the pages and creates a commit only when content changes. Failed synchronization can be retried without a new source commit.

GitHub Actions reads the already public feed to check the generator and refresh real download links on release events, manual dispatch and a schedule of roughly 15 minutes. Scheduled runs can be delayed or disabled after prolonged inactivity.

Neither news synchronization nor this public workflow builds the application, uploads EXE/ZIP files or creates binary releases. Client files require a separate owner-authorized publication; Plus remains unpublished.

No separate server or paid translation API is used. English news translations are kept with the approved public feed and tied to the exact Russian text. Missing or outdated translations link to the current Russian article. Both language versions use the same release metadata and download links.
''')
