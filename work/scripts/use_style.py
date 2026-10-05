"""Select the client style an edit uses, or re-sync the active one.
usage: python work/scripts/use_style.py <client>/<style>   select a style (e.g. acme-media/talking-head)
       python work/scripts/use_style.py                    re-sync the active style (finalize.sh runs this); if none is set
                                                           and exactly one style exists, select that one
       python work/scripts/use_style.py --list             list every client style and whether it is onboarded
Selecting writes work/active_style.json and copies the style's style/theme.ts to remotion/src/data/style_theme.ts (the engine's
theme.ts re-exports it). Edit the client's style/theme.ts, never the copy: the copy is overwritten on every run.
Prints ONBOARDED, or NEEDS ONBOARDING (style/STYLE_GUIDE.md or style/theme.ts missing: see the skill's references/ONBOARDING.md)."""
import os, sys, json, shutil
from client_style import CLIENTS, ACTIVE, PROJ, rel, has_audio

THEME_COPY = os.path.join(PROJ, 'remotion', 'src', 'data', 'style_theme.ts')


def styles():
    out = []
    if not os.path.isdir(CLIENTS):
        return out
    for c in sorted(os.listdir(CLIENTS)):
        cd = os.path.join(CLIENTS, c)
        if c.startswith(('_', '.')) or not os.path.isdir(cd):
            continue
        for s in sorted(os.listdir(cd)):
            if os.path.isdir(os.path.join(cd, s, 'source')) or os.path.isdir(os.path.join(cd, s, 'style')):
                out.append((c, s))
    return out


def onboarded(c, s):
    st = os.path.join(CLIENTS, c, s, 'style')
    return all(os.path.exists(os.path.join(st, f)) for f in ('STYLE_GUIDE.md', 'theme.ts'))


args = [a for a in sys.argv[1:] if not a.startswith('--')]
if '--list' in sys.argv:
    for c, s in styles():
        print(f'{c}/{s}: ' + ('ONBOARDED' if onboarded(c, s) else 'NEEDS ONBOARDING'))
    sys.exit(0)

quiet = False
if args:
    c, _, s = args[0].strip('/').replace('\\', '/').partition('/')
    if not s:
        sys.exit('give <client>/<style>, e.g. acme-media/talking-head')
elif os.path.exists(ACTIVE):
    a = json.load(open(ACTIVE)); c, s = a['client'], a['style']; quiet = True
else:
    found = styles()
    if len(found) != 1:
        sys.exit('no active client style. Run: python work/scripts/use_style.py <client>/<style>\navailable: '
                 + (', '.join(f'{a}/{b}' for a, b in found) or 'none - add one to clients/ (see clients/_template/README.md)'))
    c, s = found[0]

sd = os.path.join(CLIENTS, c, s)
if not os.path.isdir(sd):
    sys.exit(f'{rel(sd)} does not exist. available: ' + (', '.join(f'{a}/{b}' for a, b in styles()) or 'none'))
json.dump({'client': c, 'style': s}, open(ACTIVE, 'w'), indent=1)

theme = os.path.join(sd, 'style', 'theme.ts')
if os.path.exists(theme):
    new = open(theme, encoding='utf-8').read()
    old = open(THEME_COPY, encoding='utf-8').read() if os.path.exists(THEME_COPY) else None
    if new != old:
        with open(THEME_COPY, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(new)
        if quiet:
            print('use_style: theme re-synced from ' + rel(theme))

if quiet:
    sys.exit(0)
own = os.path.join(sd, 'sound-pack')
pack = own if has_audio(own) else os.path.join(CLIENTS, c, 'sound-pack')
print(f'active style: {c}/{s}  ->  ' + ('ONBOARDED' if onboarded(c, s) else 'NEEDS ONBOARDING (see references/ONBOARDING.md)'))
print('  style guide: ' + rel(os.path.join(sd, 'style', 'STYLE_GUIDE.md')))
print('  source:      ' + rel(os.path.join(sd, 'source')))
print('  examples:    ' + (rel(os.path.join(sd, 'examples')) if os.path.isdir(os.path.join(sd, 'examples')) else '(none)'))
print('  sound pack:  ' + rel(pack) + ('' if has_audio(pack) else '  (EMPTY - no .mp3/.wav)'))
