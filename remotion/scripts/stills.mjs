// Render many stills of a composition with a single bundle.
// usage: node scripts/stills.mjs <compositionId> <outDir> <frame> [frame...] [--scale=0.5] [--entry=src/preview/X.entry.tsx]
// (default entry src/index.ts = Main; pass --entry to render a scene's own preview composition, local frame numbers)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition, openBrowser} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs';

const args = process.argv.slice(2);
const scaleArg = args.find((a) => a.startsWith('--scale='));
const scale = scaleArg ? Number(scaleArg.split('=')[1]) : 0.5;
const entryArg = args.find((a) => a.startsWith('--entry='));
const entry = entryArg ? entryArg.split('=')[1] : 'src/index.ts';
const [id, outDir, ...rest] = args.filter((a) => !a.startsWith('--'));
const frames = rest.map(Number);
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve(entry)});
const browser = await openBrowser('chrome');
const composition = await selectComposition({serveUrl, id, puppeteerInstance: browser});
const conc = Number(process.env.CONC || 3);
let i = 0;
const work = async () => {
  while (i < frames.length) {
    const f = frames[i++];
    const out = path.join(outDir, `${id}_${String(f).padStart(4, '0')}.png`);
    if (process.env.SKIP_EXISTING && fs.existsSync(out)) continue;
    await renderStill({composition, serveUrl, frame: f, output: out, scale, imageFormat: 'png', puppeteerInstance: browser, timeoutInMilliseconds: 180000});
    process.stdout.write(`${f} `);
  }
};
await Promise.all(Array.from({length: conc}, work));
await browser.close({silent: true});
console.log('\ndone');
process.exit(0);
