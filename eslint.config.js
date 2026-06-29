import astroEslintParser from 'astro-eslint-parser';
import eslintPluginAstro from 'eslint-plugin-astro';
import globals from 'globals';
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import typescriptParser from '@typescript-eslint/parser';

export default [
  js.configs.recommended,
  ...eslintPluginAstro.configs['flat/recommended'],
  ...tseslint.configs.recommended,
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  {
    files: ['**/*.astro'],
    languageOptions: {
      parser: astroEslintParser,
      parserOptions: {
        parser: '@typescript-eslint/parser',
        extraFileExtensions: ['.astro'],
      },
    },
  },
  {
    files: ['**/*.{js,jsx,astro}'],
    rules: {
      'no-mixed-spaces-and-tabs': ['error', 'smart-tabs'],
    },
  },
  {
    // Define the configuration for `<script>` tag.
    // Script in `<script>` is assigned a virtual file name with the `.js` extension.
    files: ['**/*.{ts,tsx}', '**/*.astro/*.js'],
    languageOptions: {
      parser: typescriptParser,
    },
    rules: {
      // Note: you must disable the base rule as it can report incorrect errors
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          destructuredArrayIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/no-non-null-assertion': 'off',
    },
  },
  {
    files: ['src/components/common/Analytics.astro', 'src/components/common/Analytics.astro/**'],
    rules: {
      'prefer-rest-params': 'off',
      'no-var': 'off',
    },
  },
  {
    // RAPID²AI operator-console pages (COO / Chef / App / landing / auth callback)
    // carry hand-written browser glue in their <script> tags. Google Identity
    // Services and the rapidai-auth.js shim load as separate is:inline scripts,
    // so `google` and `RapidAIAuth` are runtime globals the bundle can't see and
    // the DOM access is deliberately terse. These scripts are marked
    // `// @ts-nocheck` (they ship as-is and `astro build` validates them); relax
    // the matching lint rules for just these virtual script files, mirroring the
    // Analytics.astro exemption above.
    files: [
      'src/pages/index.astro',
      'src/pages/index.astro/**',
      'src/pages/app/index.astro',
      'src/pages/app/index.astro/**',
      'src/pages/coo/index.astro',
      'src/pages/coo/index.astro/**',
      'src/pages/chef/index.astro',
      'src/pages/chef/index.astro/**',
      'src/pages/auth/callback.astro',
      'src/pages/auth/callback.astro/**',
    ],
    rules: {
      '@typescript-eslint/ban-ts-comment': 'off',
      'no-var': 'off',
      'no-empty': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
    },
  },
  {
    ignores: ['dist', 'node_modules', '.github', 'types.generated.d.ts', '.astro'],
  },
];
