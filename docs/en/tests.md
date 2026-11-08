[Русский](../tests.md) · [Home](../../README.en.md)

# How we test Client

| Check | What it covers |
| --- | --- |
| Package integrity | Packaged files match the release checksums. |
| Installer | The embedded application package passes integrity checks. |
| Isolated game scene | We check startup, input, reload and affected settings. |
| Live combat | We separately check rendering, response and behavior under load. |

See [release notes](../../NEWS.en.md) for results and known limitations. Performance comparisons require matched scenes and settings.

When reporting a problem, include your Client and Windows versions, installer variant and reproduction steps. [Report a problem](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/issues/new/choose)

## Release 0.3.0

Both portable packages and both embedded installer packages passed integrity checks. Each release file is checked against its SHA-256.
