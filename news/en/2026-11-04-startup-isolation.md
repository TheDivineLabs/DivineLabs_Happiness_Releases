[Русский](../2026-11-04-startup-isolation.md) · English

# Keep the application open after a browser crash

2026-11-04 · 0.2.10-dev

A change is prepared for Client and ClientPlus: web pages run separately from the main application window. A page crash leaves the window open, allowing the game to be reloaded.

An isolated native Flash test verified a deliberate renderer crash and a successful reload. Email sign-in and character loading were also verified in the diagnostic build.

The builds are available locally for testing. The public installer and portable download have not been updated yet.
