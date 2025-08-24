# -*- mode: python ; coding: utf-8 -*-

import sys; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

import subprocess
from pathlib import Path

def get_repo_dir(path: Path) -> Path:
    try:
        # Run the git command to find the top-level directory
        result = subprocess.run(
            ['git', '-C', str(path), 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        # If the path is not inside a Git repository
        raise ValueError(f"{path} is not inside a Git repository")

spec_dir = Path.cwd()  # this assumes you've started your build from the directory containing this .spec file
repo_dir = get_repo_dir(spec_dir)
resources_dir = spec_dir / "resources"
venv_dir = repo_dir / ".pixi/envs/release"
site_packages_dir = venv_dir / "Lib/site-packages"
tools_dir = spec_dir.parent


block_cipher = None


a = Analysis(
    ['main_window.py'],
    pathex=[],
    binaries=[],
    datas=[
        (site_packages_dir / "geopandas", 'geopandas/.'),
        (site_packages_dir / 'sklearn', 'sklearn/.'),
        (site_packages_dir / 'sqlalchemy', 'sqlalchemy/.'),
        (site_packages_dir / 'osgeo', 'osgeo/.'),
        (resources_dir, 'resources/.'),
        (spec_dir / 'widgets', 'widgets/.'),
        (spec_dir.parent / 'fusion_csv_to_sqlite', 'tools/fusion_csv_to_sqlite/.')
    ],
    hiddenimports=[
        'glob',
        'json',
        'boto3',
        'pandas',
        'shapely',
        'shapely.wkt',
        'matplotlib.backends.backend_qt5agg',
    ],
    hookspath=[
        venv_dir / "Library"
    ],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Build into single exe
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
