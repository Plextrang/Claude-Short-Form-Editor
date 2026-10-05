"""First-run setup + health check. Safe to run every time; it only installs what is missing.
usage: python work/scripts/setup_check.py
- Python packages (requirements.txt): looked up the same way the scripts do (work/pylibs first, then the normal environment);
  missing ones are installed with pip into the current Python environment.
- Node packages for the video engine: `npm ci` in remotion/ if node_modules is missing.
- ffmpeg + ffprobe must be on PATH (cannot be installed automatically - the script tells you)."""
import os, sys, shutil, subprocess, importlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'pylibs'))
ok = True
HINT = {'win32': 'winget install -e --id {w}', 'darwin': 'brew install {b}'}.get(sys.platform, 'sudo apt install {a}')

DATA = os.path.join(PROJ, 'remotion', 'src', 'data')
for f in ['edit.ts', 'words.json', 'scenes.ts', 'style_theme.ts']:  # git-ignored files: start from the templates
    if not os.path.exists(os.path.join(DATA, f)):
        shutil.copy(os.path.join(ROOT, 'templates', f), os.path.join(DATA, f))
        print('created remotion/src/data/' + f + ' from work/templates')

missing = []
for mod in ['faster_whisper', 'soundfile', 'numpy', 'PIL', 'librosa']:
    try:
        importlib.import_module(mod)
    except Exception:
        missing.append(mod)
if missing:
    print('installing Python packages (missing: ' + ', '.join(missing) + ') ...', flush=True)
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', os.path.join(PROJ, 'requirements.txt')])
    ok &= r.returncode == 0
else:
    print('python packages: ok')

nm = os.path.join(PROJ, 'remotion', 'node_modules')
if not os.path.isdir(nm):
    npm = shutil.which('npm')
    if not npm:
        print('MISSING: Node.js/npm - install Node 18+: ' + HINT.format(w='OpenJS.NodeJS.LTS', b='node', a='nodejs npm')); ok = False
    else:
        print('installing Node packages (npm ci) ...', flush=True)
        r = subprocess.run([npm, 'ci'], cwd=os.path.join(PROJ, 'remotion'))
        ok &= r.returncode == 0
else:
    print('node packages: ok')

for tool in ['ffmpeg', 'ffprobe']:
    if not shutil.which(tool):
        print(f'MISSING: {tool} - install ffmpeg: ' + HINT.format(w='Gyan.FFmpeg', b='ffmpeg', a='ffmpeg')); ok = False
if ok:
    print('ffmpeg: ok')
print('SETUP OK' if ok else 'SETUP INCOMPLETE - fix the MISSING items above')
sys.exit(0 if ok else 1)
