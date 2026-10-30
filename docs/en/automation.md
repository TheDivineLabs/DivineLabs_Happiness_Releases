[Русский](../automation.md) · English

# How this repository is updated

Maintainers publish approved news and prepared-build metadata from their workstation after pushing the main source branch. Existing GitHub authentication is used; this public repository has no credentials to read the private application repository.

The local publisher exports only the dedicated public feed from the pushed commit. Uncommitted drafts and application source are excluded. It generates the pages and creates a commit only when content changes. Failed synchronization can be retried without a new source commit.

GitHub Actions reads the already public feed to check the generator and refresh real download links on release events, manual dispatch and a schedule of roughly 15 minutes. Scheduled runs can be delayed or disabled after prolonged inactivity.

Neither news synchronization nor this public workflow builds the application, uploads EXE/ZIP files or creates binary releases. Client files require a separate owner-authorized publication; Plus remains unpublished.

No separate server or paid translation API is used. English news translations are kept with the approved public feed and tied to the exact Russian text. Missing or outdated translations link to the current Russian article. Both language versions use the same release metadata and download links.
