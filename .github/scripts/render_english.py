"""English product documentation; downloads come from the same release metadata."""
import re


def render_english(put, meta, client, news, translations, hero_svg):
    links = meta['links']; build = meta['build']; base = 'https://github.com/' + meta['repository']
    put('assets/hero.en.svg', hero_svg.replace('Клиент MusicWars для Windows.', 'MusicWars client for Windows.').replace('УСТАНОВЩИК EXE  ·  PORTABLE ZIP', 'EXE SETUP  ·  PORTABLE ZIP').replace('Версия ', 'Version '))
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
    put('NEWS.en.md', '[Русский](NEWS.md) · English\n\n# Happiness news\n\nRelease notes and update history.\n\n' + '\n\n'.join(lines) + '\n')
    if client:
        downloads = f"**[EXE installer]({client['installer']['url']})** · **[Portable ZIP]({client['portable']['url']})**\n\nPublished version: **{client['tag']}**. [Release notes and checksums]({client['page']})."
        if client.get('systemWebView2'):
            system = client['systemWebView2']
            downloads = f"""| Variant | Installer | Portable | VK sign-in |
| --- | --- | --- | --- |
| With bundled WebView2 | [EXE]({client['installer']['url']}) | [ZIP]({client['portable']['url']}) | Runtime included |
| Without bundled WebView2 | [EXE]({system['installer']['url']}) | [ZIP]({system['portable']['url']}) | Installed system WebView2 Runtime required |

Version: **{client['tag']}**. [Release notes and checksums]({client['page']}). Both variants include CEF and Flash for the game."""
    else:
        downloads = f"Public downloads are not available yet. Prepared build: **{build['version']}**."
    put('README.en.md', f'''[Русский](README.md) · **English**

<img src="assets/hero.en.svg" width="100%" alt="DivineLabs Happiness Client" />

# DivineLabs Happiness Client

A free MusicWars client for Windows with VK sign-in, graphics settings, screenshots and game metrics.

[Download](#download) · [Settings](docs/en/settings.md) · [What's new](NEWS.en.md) · [Testing](docs/en/tests.md) · [Support](#support)

## Download

{downloads}

## Features

- **Play.** Resizable game view, VK sign-in, Flash quality and a shortcut to reload the game.
- **Screenshots.** Capture the window, the game or a selected area. Assign shortcuts or show controls by the logo.
- **Metrics.** Move the panel and choose CPU, memory, Flash cadence and available connection metrics.
- **Maintenance.** Per-session logs, startup error messages and update checks in installed copies.

Client is for manual play. Client+ is developed separately.

## Recent updates

{latest}

[Release history](NEWS.en.md)

## Support

[DivineLabs Discord]({links['discord']}) · [Author on Telegram]({links['author']}) · [Report a bug]({base}/issues/new/choose)

Independent client. MusicWars and game assets belong to their respective rights holders. [Terms](LICENSE).
''')
    selected = re.match(r'^v?(\d+)\.(\d+)\.(\d+)', client['tag'] if client else build['version'])
    bundled = bool(selected and tuple(map(int, selected.groups())) >= (0, 2, 9))
    runtime = ('The VK sign-in component is included in the installer and portable archive. A separate WebView2 installation is not needed. You may need to sign in again when switching to the bundled component.' if bundled else 'VK sign-in requires an installed Microsoft Edge WebView2 Runtime.')
    if client and client.get('systemWebView2'):
        runtime = 'Two variants are available: with and without bundled WebView2. The latter requires an installed Microsoft Edge WebView2 Runtime for VK sign-in. Both include CEF and Flash for the game. Switching sign-in modes may require signing in again.'
    put('docs/en/getting-started.md', f'''[Русский](../getting-started.md) · English

# Getting started

{'Download Client from the main page or Releases.' if client else 'Public downloads have not been published yet.'}

1. Choose the EXE installer or the portable ZIP.
2. Update Client 0.3 and newer from the menu. Use a separate folder when moving from a previous release.
3. Extract the complete portable archive and run `DivineLabs_Happiness_Client.exe` from its root.
4. Settings, sign-in profiles and screenshots are stored in `Data`.

{runtime} Sound is disabled.

[Settings](settings.md) · [Release history](../../NEWS.en.md) · [Testing](tests.md)
''')
    sizes = meta['sizeComparison']
    put('docs/en/performance.md', f'''[Русский](../performance.md) · English

# Performance and measurements

Recorded main EXE sizes for version {sizes['version']}:

| | Client | Plus |
| --- | --- | --- |
| Main EXE | {sizes['clientExeBytes']/1048576:.2f} MiB | {sizes['plusExeBytes']/1048576:.2f} MiB |

The editions contain different modules. File size is not a measure of FPS, CPU usage or RAM usage. Browser components add to the total download and installation size.

The Client → Metrics panel can display memory, CPU and Flash readings.

Flash cadence measures frame events. Displayed FPS requires a separate measurement.

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
