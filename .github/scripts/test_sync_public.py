import hashlib, io, json, pathlib, tempfile, unittest
from unittest.mock import patch
import sync_public as public

REPO = pathlib.Path(__file__).resolve().parents[2]
class PublicationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="happiness-public-check-")
        self.root = pathlib.Path(self.temp.name);self.feed=self.root/"feed";self.out=self.root/"out"
        (self.feed/"news").mkdir(parents=True);(self.feed/"assets").mkdir()
        metadata=json.loads((REPO/"data/current.json").read_text(encoding="utf-8"));metadata.pop("news",None);metadata.pop("distribution",None)
        (self.feed/"current.json").write_text(json.dumps(metadata),encoding="utf-8")
        (self.feed/"LICENSE").write_bytes((REPO/"LICENSE").read_bytes())
        (self.feed/"assets/divinelabs.svg").write_bytes((REPO/"assets/divinelabs.svg").read_bytes())
        self.article=self.feed/"news/test.md";self.article.write_text("---\ntitle: Test update\ndate: 2026-10-30\nversion: 0.2.8\n---\nAn approved public change.\n",encoding="utf-8")
    def tearDown(self):self.temp.cleanup()
    def test_no_downloads_are_fabricated(self):
        public.render(self.feed,self.out)
        state=json.loads((self.out/"data/current.json").read_text(encoding="utf-8"))
        self.assertIsNone(state["distribution"]["client"]);self.assertIsNone(state["distribution"]["plus"])
        self.assertNotIn("releases/download/",(self.out/"README.md").read_text(encoding="utf-8"))
    def test_published_client_updates_links_and_instructions(self):
        base="https://github.com/"+public.REPOSITORY
        client={"tag":"v0.2.8","page":base+"/releases/tag/v0.2.8","preview":True,"installer":{"url":base+"/releases/download/v0.2.8/setup.exe"},"portable":{"url":base+"/releases/download/v0.2.8/portable.zip"}}
        with patch.object(public,"published_client",return_value=client):public.render(self.feed,self.out,True)
        self.assertIn(client["installer"]["url"],(self.out/"README.md").read_text(encoding="utf-8"))
        self.assertIn(client["installer"]["url"],(self.out/"README.en.md").read_text(encoding="utf-8"))
        self.assertNotIn("Публичные файлы пока не опубликованы",(self.out/"docs/getting-started.md").read_text(encoding="utf-8"))
    def test_runtime_requirement_follows_published_client_version(self):
        base="https://github.com/"+public.REPOSITORY
        client={"tag":"v0.2.9","page":base+"/releases/tag/v0.2.9","preview":True,"installer":{"url":base+"/releases/download/v0.2.9/setup.exe"},"portable":{"url":base+"/releases/download/v0.2.9/portable.zip"}}
        with patch.object(public,"published_client",return_value=client):public.render(self.feed,self.out,True)
        instructions=(self.out/"docs/getting-started.md").read_text(encoding="utf-8")
        self.assertIn("отдельно устанавливать WebView2 не нужно",instructions)
        self.assertNotIn("нужен установленный Microsoft Edge WebView2",instructions)
    def test_bundled_runtime_package_sizes_are_supported(self):
        path=self.feed/"current.json";meta=json.loads(path.read_text(encoding="utf-8"))
        meta["build"]["installerBytes"]=338188173;meta["build"]["portableBytes"]=314828568
        path.write_text(json.dumps(meta),encoding="utf-8");public.render(self.feed,self.out)
        current=json.loads((self.out/"data/current.json").read_text(encoding="utf-8"))
        self.assertEqual(current["build"]["installerBytes"],338188173)
    def add_english_translation(self):
        source=public.read_news(self.feed)[0]
        digest=hashlib.sha256(json.dumps({k:source[k] for k in ["title","date","version","body"]},ensure_ascii=False,sort_keys=True).encode("utf-8")).hexdigest()
        folder=self.feed/"en/news";folder.mkdir(parents=True)
        (folder/"test.md").write_text("---\ntitle: English update\ndate: 2026-10-30\nversion: 0.2.8\nsource_sha256: "+digest+"\n---\nCurrent English content.\n",encoding="utf-8")
    def test_matching_translation_is_published(self):
        self.add_english_translation();public.render(self.feed,self.out)
        self.assertIn("Current English content.",(self.out/"news/en/test.md").read_text(encoding="utf-8"))
        self.assertIn("English update",(self.out/"NEWS.en.md").read_text(encoding="utf-8"))
        self.assertIn("README.en.md",(self.out/"README.md").read_text(encoding="utf-8"))
    def test_stale_translation_falls_back_to_current_source(self):
        self.add_english_translation()
        with self.article.open("a",encoding="utf-8")as f:f.write("Updated source text.\n")
        public.render(self.feed,self.out)
        self.assertIn("(Russian)",(self.out/"NEWS.en.md").read_text(encoding="utf-8"))
        page=(self.out/"news/en/test.md").read_text(encoding="utf-8")
        self.assertIn("Translation unavailable",page);self.assertNotIn("Current English content",page)
    def test_localized_folder_cannot_export_application_source(self):
        folder=self.feed/"en/news";folder.mkdir(parents=True);(folder/"forbidden.pas").write_text("unit Private;",encoding="utf-8")
        with self.assertRaises(ValueError):public.render(self.feed,self.out)
        self.assertFalse((self.out/"README.md").exists())
    def test_release_catalogue_finds_both_runtime_variants(self):
        names=["DivineLabs.Happiness.Client.Setup.exe","DivineLabs-Happiness-Client-portable.zip","DivineLabs.Happiness.Client.SystemWebView2.Setup.exe","DivineLabs-Happiness-Client-SystemWebView2-portable.zip"]
        base="https://github.com/"+public.REPOSITORY
        release={"draft":False,"prerelease":True,"tag_name":"v0.2.10","html_url":base+"/releases/tag/v0.2.10","assets":[{"name":n,"state":"uploaded","browser_download_url":base+"/releases/download/v0.2.10/"+n,"size":100}for n in names]}
        with patch.object(public.urllib.request,"urlopen",return_value=io.BytesIO(json.dumps([release]).encode())):client=public.published_client()
        self.assertIn("systemWebView2",client)
        with patch.object(public,"published_client",return_value=client):public.render(self.feed,self.out,True)
        for lang in ["README.md","README.en.md"]:
            text=(self.out/lang).read_text(encoding="utf-8")
            for n in names:self.assertIn(n,text)
        self.assertIn("installed Microsoft Edge WebView2 Runtime",(self.out/"docs/en/getting-started.md").read_text(encoding="utf-8"))
    def test_application_source_aborts_before_export(self):
        (self.feed/"forbidden.pas").write_text("unit PrivateApplication;",encoding="utf-8")
        with self.assertRaises(ValueError):public.render(self.feed,self.out)
        self.assertFalse((self.out/"README.md").exists())
    def test_secret_like_content_aborts_before_export(self):
        with self.article.open("a",encoding="utf-8")as f:f.write("\nghp_"+"x"*36)
        with self.assertRaises(ValueError):public.render(self.feed,self.out)
        self.assertFalse((self.out/"README.md").exists())
    def test_unknown_metadata_cannot_be_exported(self):
        p=self.feed/"current.json";meta=json.loads(p.read_text(encoding="utf-8"));meta["unreviewed_field"]="not approved";p.write_text(json.dumps(meta),encoding="utf-8")
        with self.assertRaises(ValueError):public.render(self.feed,self.out)
        self.assertFalse((self.out/"README.md").exists())
    def test_repeated_sync_is_idempotent(self):
        public.render(self.feed,self.out);before={str(p.relative_to(self.out)):p.stat().st_mtime_ns for p in self.out.rglob("*")if p.is_file()}
        public.render(self.feed,self.out);after={str(p.relative_to(self.out)):p.stat().st_mtime_ns for p in self.out.rglob("*")if p.is_file()}
        self.assertEqual(before,after)
if __name__=="__main__":unittest.main()
