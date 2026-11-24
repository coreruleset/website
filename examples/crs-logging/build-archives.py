#!/usr/bin/env python3
"""Build the downloadable zip archives for the CRS logging blog series.

Each blog post gets one archive in its page bundle, with the example files
it needs in the same layout as this directory, under a top-level
`crs-logging/` folder:

    crs-logging/
    ├── README.md
    ├── generate-traffic.sh
    ├── waf/...
    └── elk/...            (or grafana-loki/...)

so that `cd crs-logging/elk && docker compose up -d` works exactly as it
does in the repository (the compose files refer to ../waf/).

Usage (from anywhere):

    python3 examples/crs-logging/build-archives.py          # (re)build the archives
    python3 examples/crs-logging/build-archives.py --check  # exit 1 if any is out of date

Run it after changing any file below and commit the archives. CI runs
--check on every pull request. The file lists mirror the module mounts in
config/_default/hugo.yaml; keep the two in sync.
"""

import argparse
import fnmatch
import io
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BLOG = REPO / "content" / "blog"

# Fixed metadata so that rebuilding unchanged files gives identical archives.
TIMESTAMP = (2026, 1, 1, 0, 0, 0)

# post bundle -> (archive name, glob patterns relative to this directory)
ARCHIVES = {
    "2026-11-03-crs-logging-part-1-what-your-waf-is-telling-you": (
        "crs-logging-waf.zip",
        ["README.md", "generate-traffic.sh", "waf/*"],
    ),
    "2026-11-10-crs-logging-part-2-elastic-stack": (
        "crs-logging-elk.zip",
        ["README.md", "generate-traffic.sh", "waf/*", "elk/**"],
    ),
    "2026-11-17-crs-logging-part-3-grafana-loki": (
        "crs-logging-grafana-loki.zip",
        ["README.md", "generate-traffic.sh", "waf/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf", "grafana-loki/**"],
    ),
}


def collect(patterns):
    """Files under HERE matching any pattern, as sorted relative paths."""
    files = set()
    for path in HERE.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(HERE).as_posix()
        if rel.startswith(".") or "/." in rel or rel.endswith(".pyc"):
            continue
        for pattern in patterns:
            # "dir/**" matches everything below dir, "dir/*" only direct children
            if pattern.endswith("/**"):
                if rel.startswith(pattern[:-2]):
                    files.add(rel)
            elif fnmatch.fnmatchcase(rel, pattern) and rel.count("/") == pattern.count("/"):
                files.add(rel)
    return sorted(files)


def build(patterns):
    """Return the archive as bytes."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in collect(patterns):
            src = HERE / rel
            info = zipfile.ZipInfo(f"crs-logging/{rel}", date_time=TIMESTAMP)
            mode = 0o755 if src.stat().st_mode & 0o111 else 0o644
            info.external_attr = (0o100000 | mode) << 16  # regular file + permissions
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, src.read_bytes())
    return buf.getvalue()


def contents(data):
    """Comparable view of an archive: name -> (mode, bytes)."""
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        return {i.filename: (i.external_attr >> 16, zf.read(i)) for i in zf.infolist()}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="do not write, fail if an archive is out of date")
    args = parser.parse_args()

    stale = []
    for bundle, (name, patterns) in ARCHIVES.items():
        target = BLOG / bundle / name
        if not target.parent.is_dir():
            sys.exit(f"missing page bundle: {target.parent}")
        data = build(patterns)
        current = target.read_bytes() if target.exists() else None
        up_to_date = current is not None and contents(current) == contents(data)
        if args.check:
            if not up_to_date:
                stale.append(target.relative_to(REPO))
            continue
        if not up_to_date:
            target.write_bytes(data)
        print(f"{'unchanged' if up_to_date else 'wrote':9} {target.relative_to(REPO)} ({len(contents(data))} files)")

    if stale:
        print("Out of date, run python3 examples/crs-logging/build-archives.py:", file=sys.stderr)
        for path in stale:
            print(f"  {path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
