"""Where the ACTIVE client style lives. Every script that needs the style or the sound pack imports this.
The active style is set with `python work/scripts/use_style.py <client>/<style>` and stored in work/active_style.json.

Layout (all of clients/ except clients/_template is git-ignored: client material never reaches the repo):
  clients/<client>/sound-pack/            the client's SFX (shared by all of the client's styles)
  clients/<client>/sound-pack/_catalogue/ sfx_analysis.json, sfx_events.json, sfx_audition.json (built by sfx_catalog.py)
  clients/<client>/<style>/source/        what the user dropped in: creative-direction PDF, PNG exports, reference notes
  clients/<client>/<style>/style/         generated at onboarding: STYLE_GUIDE.md, theme.ts, board/ (page tiles)
  clients/<client>/<style>/examples/      approved past edits in this style (optional)
  clients/<client>/<style>/sound-pack/    optional: a style-specific pack that overrides the client's pack"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # work/
PROJ = os.path.dirname(ROOT)
CLIENTS = os.path.join(PROJ, 'clients')
ACTIVE = os.path.join(ROOT, 'active_style.json')
AUDIO = ('.mp3', '.wav')


def active():
    """(client, style) of the active style; exits with a clear message if none is set."""
    if not os.path.exists(ACTIVE):
        sys.exit('no active client style - run: python work/scripts/use_style.py <client>/<style>')
    a = json.load(open(ACTIVE))
    return a['client'], a['style']


def client_dir():
    return os.path.join(CLIENTS, active()[0])


def style_dir():
    c, s = active()
    return os.path.join(CLIENTS, c, s)


def has_audio(d):
    for dp, dn, fn in os.walk(d):
        if any(f.lower().endswith(AUDIO) for f in fn):
            return True
    return False


def sound_lib():
    """The style's own sound-pack/ if it has audio, else the client's sound-pack/."""
    own = os.path.join(style_dir(), 'sound-pack')
    return own if has_audio(own) else os.path.join(client_dir(), 'sound-pack')


def catalogue(name):
    """Path of a catalogue file (sfx_analysis.json / sfx_events.json / sfx_audition.json) for the active sound pack."""
    d = os.path.join(sound_lib(), '_catalogue')
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def rel(p):
    return os.path.relpath(p, PROJ).replace(os.sep, '/')
