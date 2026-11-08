[English](en/2026-11-07-rust-client.md)

# Rust Client 0.1.0: вход через ВК и ручная игра

2026-11-07 · 0.1.0-rust

Первый portable-клиент Happiness на Rust. Игровые CEF и нативный Flash сохранены, звук выключен.

**[Rust Client 0.1.0: файлы и контрольные суммы](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/releases/tag/rust-v0.1.0)**

- [Portable со встроенным WebView2](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/releases/download/rust-v0.1.0/DivineLabs.Happiness.Rust.Client.Bundled.portable.zip).
- [Portable с системным WebView2](https://github.com/TheDivineLabs/DivineLabs_Happiness_Releases/releases/download/rust-v0.1.0/DivineLabs.Happiness.Rust.Client.SystemWebView2.portable.zip). Для входа через ВК нужен установленный Microsoft Edge WebView2 Runtime.

Rust Client хранит профиль в папке Data рядом с запускатором. Его канал отделён от Delphi: существующие установки и автообновления не переключаются на Rust.

В этой версии есть адаптивное окно игры, отдельное окно входа ВК, перемещаемый знак DivineLabs и сообщения об ошибках запуска. Команды обновления игры, входа ВК и открытия журналов доступны через системное меню окна (Alt+Space).

Автоматизация ClientPlus, установщик, автообновление, трей, темы и полноэкранная горячая клавиша пока не перенесены на Rust. Dev выпускается отдельно для разработки, без публичных файлов. Rust ClientPlus и ClientPlus Dev ещё не готовы.

Сравнительные показатели FPS, CPU и памяти не опубликованы. Rust 0.1.0 выпускается как предварительная версия для ручной игры.
