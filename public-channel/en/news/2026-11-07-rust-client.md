---
title: Rust Client 0.1.0: VK sign-in and manual play
date: 2026-11-07
version: 0.1.0-rust
source_sha256: 07eb54f83e0994cb257360ec0055a44f3aa0cb98af331884ac4084c1af5ae816
---

The first portable Happiness client written in Rust. The owner verified VK sign-in, manual play, appearance and logo positioning when resizing the window. The existing CEF and native Flash runtimes remain in use; sound stays muted.

**[Rust Client 0.1.0: downloads and checksums](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/releases/tag/rust-v0.1.0)**

- [Portable with bundled WebView2](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/releases/download/rust-v0.1.0/DivineLabs.Happiness.Rust.Client.Bundled.portable.zip).
- [Portable using system WebView2](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/releases/download/rust-v0.1.0/DivineLabs.Happiness.Rust.Client.SystemWebView2.portable.zip). VK sign-in requires an installed Microsoft Edge WebView2 Runtime.

Rust Client stores its profile in Data beside the launcher. Its channel is separate from Delphi: existing installations and automatic updates are not switched to Rust.

This version includes a responsive game window, a separate VK sign-in window, a draggable DivineLabs mark and visible startup errors. Reload, VK sign-in and logs are available in the Windows system menu (Alt+Space).

ClientPlus automation, installer, updates, tray, themes and the fullscreen hotkey have not been ported to Rust. Dev is distributed separately for development, without public downloads. Rust ClientPlus and ClientPlus Dev are not ready yet.

No comparative FPS, CPU or memory results are published. Rust 0.1.0 is a preview release for manual play.
