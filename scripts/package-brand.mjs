import { createRequire } from 'node:module';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { cp, mkdir, mkdtemp, readFile, readdir, rename, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
// Reuse the destination's pinned Sharp dependency without changing its lockfile.
const loadDependency = createRequire(join(root, 'package.json'));
const sharp = loadDependency('sharp');
const brand = join(root, 'public/assets/brand');
const logos = join(brand, 'logos');

for (const file of (await readdir(logos)).filter((name) => name.endsWith('.svg'))) {
  const width = file.includes('wordmark') ? 1200 : 512;
  await sharp(join(logos, file), { density: 300 })
    .resize({ width })
    .png()
    .toFile(join(logos, file.replace(/\.svg$/, '.png')));
}
for (const name of ['atoma', 'grant-intelligence']) {
  await sharp(join(brand, `${name}-social-1200x630.svg`))
    .png()
    .toFile(join(brand, `${name}-social-1200x630.png`));
}
await sharp(join(brand, 'atoma-favicon.svg'), { density: 300 })
  .resize(180, 180)
  .png()
  .toFile(join(brand, 'atoma-touch-icon.png'));
await sharp(join(brand, 'atoma-brand-board.svg')).png().toFile(join(brand, 'atoma-brand-board.png'));
await cp(join(root, 'docs/ATOMA_DESIGN_PACKAGE.md'), join(brand, 'DESIGN-GUIDE.md'));
await cp(join(root, 'public/assets/atoma-tokens.css'), join(brand, 'tokens.css'));

async function entries(directory) {
  const files = [];
  for (const item of await readdir(directory, { withFileTypes: true })) {
    if (item.name.startsWith('.') || ['atoma-brand-package.zip', 'manifest.json'].includes(item.name)) continue;
    const path = join(directory, item.name);
    if (item.isDirectory()) files.push(...(await entries(path)));
    else files.push(path);
  }
  return files.sort();
}
const manifest = [];
for (const path of await entries(brand)) {
  const data = await readFile(path);
  manifest.push({
    path: relative(brand, path),
    bytes: data.length,
    sha256: createHash('sha256').update(data).digest('hex'),
  });
}
await writeFile(join(brand, 'manifest.json'), `${JSON.stringify({ version: '1.0.0', files: manifest }, null, 2)}\n`);

const staging = await mkdtemp(join(tmpdir(), 'atoma-brand-'));
try {
  const bundle = join(staging, 'atoma-design-package');
  await mkdir(bundle);
  await mkdir(join(bundle, 'scripts'));
  for (const path of ['scripts/build-brand-vectors.py', 'scripts/package-brand.mjs', 'scripts/verify-brand-ui.py']) {
    await cp(join(root, path), join(bundle, path));
  }
  await mkdir(join(bundle, 'public/assets'), { recursive: true });
  await mkdir(join(bundle, 'public/engineering/brand'), { recursive: true });
  await cp(join(root, 'src/pages/engineering'), join(bundle, 'src/pages/engineering'), { recursive: true });
  // Export these standalone documents as HTML, removing only Astro's script directive.
  for (const [source, destination] of [
    ['src/pages/engineering/index.astro', 'public/engineering/index.html'],
    ['src/pages/engineering/brand/index.astro', 'public/engineering/brand/index.html'],
  ]) {
    const html = (await readFile(join(root, source), 'utf8')).replaceAll(' is:inline', '');
    await writeFile(join(bundle, destination), html);
  }
  for (const name of ['atoma-tokens.css', 'engineering.css', 'engineering.js']) {
    await cp(join(root, 'public/assets', name), join(bundle, 'public/assets', name));
  }
  await cp(brand, join(bundle, 'public/assets/brand'), {
    recursive: true,
    filter: (path) => !basename(path).startsWith('.') && !path.endsWith('atoma-brand-package.zip'),
  });
  await mkdir(join(bundle, 'docs'));
  await cp(join(root, 'docs/ATOMA_DESIGN_PACKAGE.md'), join(bundle, 'docs/ATOMA_DESIGN_PACKAGE.md'));
  await cp(join(root, 'docs/ATOMA_PACKAGE_README.md'), join(bundle, 'README.md'));
  await writeFile(
    join(bundle, 'package.json'),
    `${JSON.stringify(
      {
        name: 'atoma-design-package',
        version: '1.0.0',
        private: true,
        type: 'module',
        scripts: {
          'brand:vectors': 'uv run scripts/build-brand-vectors.py',
          'brand:package': 'node scripts/package-brand.mjs',
          'brand:build': 'npm run brand:vectors && npm run brand:package',
        },
        devDependencies: { sharp: sharp.versions.sharp },
      },
      null,
      2
    )}\n`
  );
  await cp(join(root, 'docs/ATOMA_PACKAGE_README.md'), join(bundle, 'docs/ATOMA_PACKAGE_README.md'));
  const result = spawnSync('zip', ['-qr', join(staging, 'package.zip'), 'atoma-design-package'], {
    cwd: staging,
    encoding: 'utf8',
  });
  if (result.status !== 0) throw new Error(result.stderr || 'zip failed');
  await rename(join(staging, 'package.zip'), join(brand, 'atoma-brand-package.zip'));
} finally {
  await rm(staging, { recursive: true, force: true });
}
console.log(`Packaged ${manifest.length} brand files, website sources, fonts, licenses, and rebuild scripts.`);
