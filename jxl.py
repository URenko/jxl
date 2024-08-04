import subprocess, filecmp, tempfile
from pathlib import Path, PurePath
from PIL import Image

def cjxl(fpath: Path, *, effect=10, brotli_effort=11):
    if fpath.suffix.lower() != '.jpg':
        return fpath
    with Image.open(fpath) as im:
        if im.format != 'JPEG':
            return fpath
    jxl_path = fpath.with_suffix(fpath.suffix.translate(str.maketrans('pgPG', 'xlXL')))
    subprocess.run([
        "cjxl",
        str(fpath),
        str(jxl_path),
        '--lossless_jpeg', '1',
        '-e', str(effect),
        '--brotli_effort', str(brotli_effort)
    ], check=True)
    with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
        subprocess.run(["djxl", str(jxl_path), tmp.name], check=True)
        assert filecmp.cmp(str(fpath), tmp.name)
    fpath.unlink()
    return jxl_path

jxl = cjxl


def jxl_name(fpath: PurePath):
    if fpath.suffix.lower() != '.jpg':
        return fpath
    return fpath.with_suffix(fpath.suffix.translate(str.maketrans("PGpg", "XLxl")))

def jxl_exists(p: Path):
    return p.exists() or (p.suffix.lower() == '.jpg' and jxl_name(p).exists())

