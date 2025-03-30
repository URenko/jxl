from typing import Optional
import subprocess, filecmp, tempfile, sys
from pathlib import Path, PurePath
from PIL import Image

def cjxl(fpath: Path, output: Optional[Path] = None, *, effect=10, brotli_effort=11, _silent_failed=False, ignore_extension=False):
    if not ignore_extension and fpath.suffix.lower() != '.jpg':
        return fpath
    with Image.open(fpath) as im:
        if im.format != 'JPEG':
            return fpath
    jxl_path = fpath.with_suffix(fpath.suffix.translate(str.maketrans('pgPG', 'xlXL'))) if output is None else output
    p = subprocess.run([
        "cjxl",
        str(fpath),
        str(jxl_path),
        '--lossless_jpeg', '1',
        '-e', str(effect),
        '--brotli_effort', str(brotli_effort)
    ], check=(not _silent_failed))
    if _silent_failed and p.returncode:
        print('The exit code of cjxl is non-zero.', file=sys.stderr)
        if jxl_path.exists():
            jxl_path.unlink()
        return fpath
    with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
        subprocess.run(["djxl", str(jxl_path), tmp.name], check=True)
        if not filecmp.cmp(str(fpath), tmp.name):
            print(f'cjxl {fpath} produced jxl file that cannot be consistently decoded by djxl!', file=sys.stderr)
            jxl_path.unlink()
            return fpath
    fpath.unlink()
    return jxl_path

jxl = cjxl


def jxl_name(fpath: PurePath):
    if fpath.suffix.lower() != '.jpg':
        return fpath
    return fpath.with_suffix(fpath.suffix.translate(str.maketrans("PGpg", "XLxl")))

def jxl_exists(p: Path):
    return p.exists() or (p.suffix.lower() == '.jpg' and jxl_name(p).exists())

