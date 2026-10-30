"""Render approved public data. Never copy an application tree or execute source-repository code."""
import argparse, datetime, html, json, os, pathlib, re, urllib.request

REPOSITORY = "TheDivineLabs/DivineLabs_Happiness_Releases"
APP_EXTENSIONS = {".pas", ".dpr", ".dfm", ".inc", ".as", ".exe", ".dll", ".zip", ".res", ".dcu"}
PRIVATE = re.compile(r"W:[/\\]DEV|github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|https://github\.com/TheDivineLabs/DivineLabs_Happiness(?!_Releases)", re.I)

def safe_text(value):
    if PRIVATE.search(value) or re.search(r"(?m)^\s*(?:unit|program)\s+[A-Za-z_][\w.]*\s*;", value):
        raise ValueError("The approved feed contains private material or application source")
    return value

def checked_file(root, relative):
    p = root / relative
    if p.is_symlink() or not p.resolve().is_relative_to(root.resolve()): raise ValueError("Feed path escapes its root")
    if not p.is_file() or p.stat().st_size > 256 * 1024: raise ValueError("Missing or oversized public text")
    return p

def read_news(root):
    items = []
    for p in sorted((root / "news").glob("*.md")):
        if not re.fullmatch(r"[a-zA-Z0-9._-]+\.md", p.name): raise ValueError("Invalid news filename")
        text = safe_text(checked_file(root, "news/" + p.name).read_text(encoding="utf-8-sig"))
        if not text.startswith("---\n"): raise ValueError("News front matter is required")
        front, body = text[4:].split("\n---\n", 1)
        fields = dict(line.split(":", 1) for line in front.splitlines() if line.strip())
        fields = {k.strip(): v.strip() for k, v in fields.items()}
        if set(fields) != {"title", "date", "version"}: raise ValueError("Unknown news fields")
        datetime.date.fromisoformat(fields["date"])
        if len(fields["title"]) > 160 or any(c in fields["title"] for c in "[]<>\r\n"): raise ValueError("Invalid news title")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?", fields["version"]): raise ValueError("Invalid news version")
        items.append(dict(fields, file=p.name, body=body.strip()))
    return sorted(items, key=lambda x: (x["date"], tuple(int(v) for v in x["version"].split("-")[0].split("."))), reverse=True)

def published_client():
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "DivineLabs-Happiness-showcase", "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GITHUB_TOKEN"): headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request("https://api.github.com/repos/" + REPOSITORY + "/releases?per_page=100", headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response: releases = json.load(response)
    for release in releases:
        if release["draft"]: continue
        assets = {a["name"]: a for a in release["assets"] if a.get("state") == "uploaded"}
        names = ["DivineLabs.Happiness.Client.Setup.exe", "DivineLabs-Happiness-Client-portable.zip"]
        if not all(n in assets for n in names): continue
        result = {"tag": release["tag_name"], "page": release["html_url"], "preview": release["prerelease"]}
        for key, name in zip(["installer", "portable"], names):
            url = assets[name]["browser_download_url"]
            if not url.startswith("https://github.com/" + REPOSITORY + "/releases/download/"): raise ValueError("Unexpected download location")
            result[key] = {"name": name, "url": url, "bytes": assets[name]["size"], "digest": assets[name].get("digest")}
        return result
    return None

def hero(version):
    v = html.escape(version)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#111629"/><stop offset="1" stop-color="#20193e"/></linearGradient><linearGradient id="accent" x2="1" y2="1"><stop stop-color="#ba9cff"/><stop offset="1" stop-color="#7761ff"/></linearGradient><linearGradient id="window" x2="0" y2="1"><stop stop-color="#302a50"/><stop offset="1" stop-color="#181b30"/></linearGradient></defs>
<rect width="1280" height="420" rx="24" fill="url(#bg)"/><circle cx="1090" cy="210" r="300" fill="none" stroke="#403362" stroke-width="1"/><circle cx="1090" cy="210" r="230" fill="none" stroke="#403362"/><circle cx="1090" cy="210" r="165" fill="none" stroke="#4a3d71"/>
<g font-family="Segoe UI,Inter,Arial,sans-serif"><text x="64" y="75" fill="#b5a2ee" font-size="16" letter-spacing="5">DIVINELABS / MUSICWARS</text><text x="60" y="174" fill="#faf8ff" font-size="82" font-weight="700" letter-spacing="-2">Happiness</text><text x="65" y="225" fill="#c4c4db" font-size="23">Клиент MusicWars для Windows.</text>
<rect x="64" y="276" width="150" height="38" rx="19" fill="#292540" stroke="#645185"/><text x="89" y="301" fill="#ece5ff" font-size="15">Windows x64</text><rect x="226" y="276" width="160" height="38" rx="19" fill="#292540" stroke="#645185"/><text x="247" y="301" fill="#ece5ff" font-size="15">Preview {v}</text><text x="65" y="367" fill="#8e90aa" font-size="15">УСТАНОВЩИК EXE  ·  PORTABLE ZIP</text></g>
<g transform="translate(826 77)"><rect x="12" y="20" width="360" height="252" rx="22" fill="#0b1020" opacity=".35"/><rect width="360" height="252" rx="22" fill="url(#window)" stroke="#6b5a96"/><path d="M0 49h360" stroke="#55456f"/><circle cx="25" cy="25" r="5" fill="#b6a2e8"/><circle cx="43" cy="25" r="5" fill="#8f7fbb"/><circle cx="61" cy="25" r="5" fill="#665c89"/><rect x="24" y="74" width="312" height="144" rx="13" fill="#151a2c" stroke="#38324c"/>
<g transform="translate(127 82) scale(.72)"><rect width="144" height="144" rx="34" fill="url(#accent)"/><path d="M28 38C28 22 40 16 54 16H64C82 16 96 26 104 42H50C41 42 33 47 28 54ZM28 66C28 54 40 48 52 48H106C109 58 109 67 106 78H50C41 78 33 83 28 91ZM28 102C28 90 40 84 52 84H103C95 102 79 114 61 114H49C40 114 33 119 28 124Z" transform="translate(8 -2)" fill="white"/></g>
<rect x="240" y="192" width="102" height="85" rx="13" fill="#24223b" stroke="#8872b6"/><rect x="255" y="208" width="71" height="9" rx="4" fill="#9b83d8"/><rect x="255" y="228" width="48" height="7" rx="3" fill="#625574"/><rect x="255" y="245" width="61" height="7" rx="3" fill="#625574"/></g></svg>
'''

def render(root, out, fetch=False):
    root = root.resolve(); out = out.resolve()
    meta_text = safe_text(checked_file(root, "current.json").read_text(encoding="utf-8-sig")); meta = json.loads(meta_text)
    if set(meta) != {"schema", "product", "repository", "links", "build", "plus", "performance", "sizeComparison"}: raise ValueError("Unknown public metadata fields")
    if meta["product"] != "DivineLabs Happiness": raise ValueError("Unexpected product")
    if set(meta["build"]) != {"version", "date", "channel", "clientExeBytes", "plusExeBytes", "installerBytes", "portableBytes"}: raise ValueError("Unknown build fields")
    if meta["build"]["channel"] not in {"preview", "stable"}: raise ValueError("Unknown release channel")
    if set(meta["sizeComparison"]) != {"version", "clientExeBytes", "plusExeBytes"}: raise ValueError("Unknown comparison fields")
    if set(meta["performance"]) != {"fpsComparisonPublished", "cpuComparisonPublished"}: raise ValueError("Unknown performance fields")
    if meta["schema"] != 1 or meta["repository"] != REPOSITORY: raise ValueError("Wrong public channel")
    b = meta["build"]; version = b["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version): raise ValueError("Invalid current version")
    datetime.date.fromisoformat(b["date"])
    for key in ["clientExeBytes", "plusExeBytes", "installerBytes", "portableBytes"]:
        if not isinstance(b[key], int) or not 0 < b[key] < 300 * 1048576: raise ValueError("Invalid measured file size")
    if any(meta["performance"].values()): raise ValueError("Runtime improvement claims need a separately reviewed benchmark report")
    if meta["plus"] != {"status": "planned", "publicDownloads": False}: raise ValueError("Plus publication is not enabled")
    links = meta["links"]
    if links != {"author": "https://t.me/ps1xo_on1ks", "github": "https://github.com/TheDivineLabs", "discord": "https://discord.gg/vF47ExMQpn"}: raise ValueError("Unexpected public contacts")
    news = read_news(root); client = published_client() if fetch else None
    def put(name, value):
        destination = out / name
        if not destination.resolve().is_relative_to(out) or destination.is_symlink(): raise ValueError("Unsafe output path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = value if isinstance(value, bytes) else value.encode("utf-8")
        if not destination.exists() or destination.read_bytes() != data: destination.write_bytes(data)
    approved = {"current.json", "LICENSE", "assets/divinelabs.svg"} | {"news/" + n["file"] for n in news}
    for p in root.rglob("*"):
        if p.is_symlink(): raise ValueError("Symlinks are not allowed in the public feed")
        if p.is_file() and (p.suffix.lower() in APP_EXTENSIONS or p.relative_to(root).as_posix() not in approved): raise ValueError("Application files are forbidden in the public feed")
    logo = checked_file(root, "assets/divinelabs.svg").read_text(encoding="utf-8-sig")
    if any(word in logo.lower() for word in ["<script", "foreignobject", "javascript:", "<image", "<!entity"]): raise ValueError("Active SVG is forbidden")
    put("assets/divinelabs.svg", logo); put("assets/hero.svg", hero(version))
    put("LICENSE", safe_text(checked_file(root, "LICENSE").read_text(encoding="utf-8-sig")))
    news_lines = []
    for n in news:
        put("news/" + n["file"], "# " + n["title"] + "\n\n" + n["date"] + " · " + n["version"] + "\n\n" + n["body"] + "\n")
        news_lines.append("- **" + n["date"] + " · " + n["version"] + "** - [" + n["title"] + "](news/" + n["file"] + ")")
    for stale in (out / "news").glob("*.md"):
        if stale.name not in {n["file"] for n in news}:
            if stale.is_symlink() or not stale.resolve().is_relative_to(out): raise ValueError("Unsafe obsolete news path")
            stale.unlink()
    put("NEWS.md", "# Новости Happiness\n\nОписание готовых изменений и подготовленных сборок. Наличие записи не означает, что её файлы уже открыты для скачивания.\n\n" + "\n\n".join(news_lines) + "\n")
    public = dict(meta, distribution={"client": client, "plus": None}, news=[{k:v for k,v in n.items() if k != "body"} for n in news])
    put("data/current.json", json.dumps(public, ensure_ascii=False, indent=2) + "\n")
    base = "https://github.com/" + REPOSITORY
    if client:
        downloads = f"**[Установщик EXE]({client['installer']['url']})** &nbsp; · &nbsp; **[Portable ZIP]({client['portable']['url']})**\n\nПубличная версия: **{html.escape(client['tag'])}**. [Изменения и контрольные суммы]({client['page']})."
    else:
        downloads = "**Публичная загрузка пока не открыта.**\n\nПодготовленная сборка: **" + version + " Preview**. Здесь появятся установщик EXE, portable ZIP и контрольные суммы после публикации владельцем."
    latest = "\n\n".join(news_lines[:3]); exe = meta["sizeComparison"]["clientExeBytes"] / 1048576; plus = meta["sizeComparison"]["plusExeBytes"] / 1048576; comparison_version = meta["sizeComparison"]["version"]
    readme = f'''<div align="center">
<img src="assets/hero.svg" width="100%" alt="DivineLabs Happiness - клиент MusicWars для Windows" />
<br /><br />
<a href="#скачать"><img src="https://img.shields.io/badge/CLIENT-Windows_x64-8B6CEF?style=for-the-badge&amp;logo=windows&amp;logoColor=white" alt="Client для Windows" /></a>
<a href="NEWS.md"><img src="https://img.shields.io/badge/НОВОСТИ-обновления-222238?style=for-the-badge" alt="Новости" /></a>
<a href="{links['discord']}"><img src="https://img.shields.io/badge/DISCORD-DivineLabs-5865F2?style=for-the-badge&amp;logo=discord&amp;logoColor=white" alt="Discord DivineLabs" /></a>
<a href="{links['author']}"><img src="https://img.shields.io/badge/TELEGRAM-автор-229ED9?style=for-the-badge&amp;logo=telegram&amp;logoColor=white" alt="Автор в Telegram" /></a>
</div>

# DivineLabs Happiness

Клиент MusicWars для Windows. Доступен в виде установщика и portable-архива.

**[Скачать](#скачать)** · **[Что нового](NEWS.md)** · **[Начало работы](docs/getting-started.md)** · **[Поддержка](#поддержка)**

## Скачать

{downloads}

Предварительная версия. Полная игровая проверка ещё не завершена.

## Возможности

- Адаптивное окно игры, полноэкранный режим и горячие клавиши.
- Боковая панель по нажатию на перемещаемый логотип DivineLabs.
- Четыре темы: Orbit, Signal, Paper и Control.
- Скриншоты игры без элементов оболочки.
- Сворачивание в системный трей.
- Локальная запись технических показателей.
- Открытие ссылок из писем внутри клиента.

## Client и Plus

| | Client | Plus |
| --- | --- | --- |
| Игровое окно, темы, ссылки и скриншоты | Есть | Есть |
| Основное приложение | Самостоятельный клиент | Клиент с дополнительными игровыми модулями |
| Основной EXE · {comparison_version} | {exe:.2f} МиБ | {plus:.2f} МиБ |
| Публичный канал | {"Доступен" if client else "Подготавливается"} | После запуска подписок |

Plus пока не опубликован. Подписки ещё не запущены.

## Производительность

Основной EXE подготовленной версии {version} занимает **{b['clientExeBytes']/1048576:.2f} МиБ**. Компоненты браузера входят в установщик и portable отдельно от EXE.

Сравнительных замеров FPS, CPU и памяти пока нет. [Сведения о размерах и замерах](docs/performance.md).

## Сейчас в проекте

{latest}

[Все новости →](NEWS.md)

## Поддержка

**[Discord DivineLabs]({links['discord']})** · **[Автор в Telegram]({links['author']})** · **[GitHub автора]({links['github']})**

Нашли ошибку? [Откройте обращение]({base}/issues/new/choose): укажите версию, Windows и шаги повторения.

## Лицензия и происхождение

Happiness распространяется на [закрытых условиях](LICENSE). Разрешено личное использование официальной сборки и тестирование. Публикация, перепродажа и распространение собственного кода и сборок требуют разрешения правообладателя. [Краткое объяснение](docs/license.md).

Этот репозиторий содержит страницу продукта, новости и материалы выпусков. Исходный код приложения здесь не публикуется.

Независимый неофициальный проект. MusicWars и игровые материалы принадлежат их правообладателям.
'''
    put("README.md", readme)
    selected = re.match(r"^v?(\d+)\.(\d+)\.(\d+)", client["tag"] if client else version)
    bundled = bool(selected and tuple(map(int, selected.groups())) >= (0, 2, 9))
    runtime_note = ("Компонент входа через ВК включён в установщик и portable; отдельно устанавливать WebView2 не нужно. При переходе на встроенный движок может потребоваться повторный вход." if bundled else "Для входа через ВК нужен установленный Microsoft Edge WebView2 Runtime. Вход в Client 0.2.8 проверен владельцем.")
    put("docs/getting-started.md", "# Начало работы\n\n" + ("Скачайте Client по кнопкам на главной странице или в Releases." if client else "Публичные файлы пока не опубликованы. Когда канал откроется, кнопки появятся на главной странице и в Releases.") + """

1. Выберите Client Setup.exe для установки или portable ZIP для распаковки.
2. Обновляйте установленную копию в той же папке. Перед переносом portable сохраните всю папку Data.
3. Для portable распакуйте архив целиком и запускайте DivineLabs.Happiness.exe из корня.
4. Настройки и профили находятся в Data. Установка и удаление используют фирменный мастер DivineLabs.

""" + runtime_note + """ Звук выключен.

По умолчанию удаление сохраняет данные. Полное удаление выбирается отдельно. Обновление и удаление 0.2.8 проверены на отдельных тестовых установках.

Версия предварительная. При ошибке укажите версию приложения и шаги повторения в Issues или Discord.
""")
    put("docs/performance.md", f"""# Производительность и замеры

Для версии {comparison_version} известны следующие размеры:

| Показатель | Client | Plus |
| --- | --- | --- |
| Основной EXE | {exe:.2f} МиБ | {plus:.2f} МиБ |

Разница связана с составом редакций. Это не сравнение одинаковых по функциям приложений и не доказательство снижения CPU, памяти или роста FPS. Общие CEF/Flash-компоненты остаются в поставке.

В приложении есть запись технических показателей на 60 секунд. Она выключена по умолчанию; отчёт сохраняется локально в Data/Diagnostics/Performance и не отправляется автоматически.

Можно получить CPU, память и доступные интервалы Flash-кадров. События игровой логики не равны частоте фактического показа изображения. Показатель видимого FPS из этих событий не вычисляется.

Сравнение с обычным браузером и результаты графических оптимизаций пока не опубликованы. Корректный отчёт должен содержать одинаковую сцену, размер окна, состояние кеша, прогрев и несколько повторов. До таких результатов проценты прироста не заявляются.
""")
    put("docs/license.md", """# Какие права даёт лицензия

Название: **DivineLabs Happiness Proprietary License**. Идентификатор: **LicenseRef-DivineLabs-Happiness-Proprietary**. Это собственные закрытые условия проекта, не MIT и не стандартная открытая лицензия.

Законному получателю официальной сборки разрешены установка, запуск для личного использования и тестирование. Исключительные права на собственные оригинальные материалы сохраняются за их правообладателем DivineLabs / TheDivineLabs.

Без отдельного письменного разрешения не допускаются публикация и распространение собственного исходного кода и сборок, перепродажа, сублицензирование, включение в другие продукты и распространение изменённых версий собственных частей проекта.

Доступ к репозиторию или получение файла не передаёт исключительных прав. Права на сторонние компоненты и игровые материалы сохраняются у их владельцев и регулируются их условиями. Обязательные права по закону и ранее правомерно выданные разрешения сохраняются.

Это краткое объяснение. Полный текст и точная область действия находятся в [LICENSE](../LICENSE).
""")
    print(f"Synced {len(news)} public news entries; prepared build {version}; public Client downloads: {bool(client)}. No application files copied.")

if __name__ == "__main__":
    p = argparse.ArgumentParser();p.add_argument("--input", required=True, type=pathlib.Path);p.add_argument("--output", required=True, type=pathlib.Path);p.add_argument("--fetch-public-releases", action="store_true");a = p.parse_args()
    render(a.input, a.output, a.fetch_public_releases)
