# PyInstaller spec: `pyinstaller AroPresent.spec` -> dist/AroPresent.app (macOS) or dist/AroPresent.exe (Windows)
import sys

a = Analysis(
    ["desktop.py"],
    datas=[
        ("aropresent/views", "aropresent/views"),
        ("aropresent/slide_templates", "aropresent/slide_templates"),
    ],
    hiddenimports=[],
)
pyz = PYZ(a.pure)

if sys.platform == "darwin":
    exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="AroPresent", console=False)
    coll = COLLECT(exe, a.binaries, a.datas, name="AroPresent")
    app = BUNDLE(coll, name="AroPresent.app", bundle_identifier="com.aropresent.app")
else:
    exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name="AroPresent", console=False)
