#!/usr/bin/env python3
"""
Dynamic Documentation Builder for Toubkal HPC Applications.

Automatically discovers all application directories on the root of the repo,
sorts them alphabetically, and generates the static documentation website
using MkDocs Material.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.exit("Error: 'pyyaml' is required. Please install it with: pip install pyyaml")


def find_application_folders(root_dir: str, extra_ignored: set = None):
    """
    Finds all non-hidden directories containing a README.md,
    ignoring build artifacts, git internals, and cache directories.
    Returns them sorted alphabetically.
    """
    ignored = {
        'public',
        'site',
        '_site',
        'docs',
        'dist',
        'build',
        'node_modules',
        'vendor',
        '__pycache__',
        '.git',
        '.github',
        '.cache',
        '.vscode',
        '.idea',
        'venv',
        '.venv',
        'env',
        '.env',
    }
    if extra_ignored:
        ignored.update(extra_ignored)

    folders = []
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if (
            os.path.isdir(full_path)
            and not entry.startswith('.')
            and not entry.startswith('_')
            and entry not in ignored
        ):
            readme_path = os.path.join(full_path, 'README.md')
            if os.path.exists(readme_path):
                folders.append(entry)

    # Sort alphabetically (case-insensitive)
    return sorted(folders, key=lambda s: s.lower())


def build_docs(output_dir: str = 'public', serve: bool = False):
    # Resolve repository root based on the script location
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Exclude output_dir from application discovery
    out_dirname = os.path.basename(os.path.abspath(output_dir))
    folders = find_application_folders(root_dir, extra_ignored={out_dirname})

    print(f"Discovered {len(folders)} application folders (sorted alphabetically):")
    for f in folders:
        print(f"  - {f}")

    with tempfile.TemporaryDirectory() as temp_dir:
        staging_docs = os.path.join(temp_dir, 'docs')
        os.makedirs(staging_docs, exist_ok=True)

        # 1. Root README as index.md (Home)
        root_readme = os.path.join(root_dir, 'README.md')
        if os.path.exists(root_readme):
            shutil.copy(root_readme, os.path.join(staging_docs, 'index.md'))

        # 2. Add each folder sorted alphabetically
        nav = [{'Home': 'index.md'}]
        for folder in folders:
            src_folder = os.path.join(root_dir, folder)
            dest_folder = os.path.join(staging_docs, folder)
            # Copy folder while ignoring hidden/temporary files
            shutil.copytree(
                src_folder,
                dest_folder,
                ignore=shutil.ignore_patterns('.*', '*.swp', '*~', '__pycache__'),
            )
            nav.append({folder: f'{folder}/README.md'})

        target_site_dir = os.path.abspath(output_dir)

        cfg = {
            'site_name': 'Toubkal HPC Applications',
            'site_description': (
                'Application run examples and benchmarks on Toubkal supercomputer'
            ),
            'theme': {
                'name': 'material',
                'palette': [
                    {
                        'scheme': 'slate',
                        'primary': 'indigo',
                        'accent': 'indigo',
                        'toggle': {
                            'icon': 'material/weather-sunny',
                            'name': 'Switch to light mode',
                        },
                    },
                    {
                        'scheme': 'default',
                        'primary': 'indigo',
                        'accent': 'indigo',
                        'toggle': {
                            'icon': 'material/weather-night',
                            'name': 'Switch to dark mode',
                        },
                    },
                ],
                'features': [
                    'navigation.instant',
                    'navigation.tracking',
                    'navigation.top',
                    'search.suggest',
                    'search.highlight',
                    'content.code.copy',
                ],
            },
            'markdown_extensions': [
                'admonition',
                'pymdownx.details',
                'pymdownx.superfences',
                'pymdownx.highlight',
                'pymdownx.inlinehilite',
                'tables',
            ],
            'docs_dir': staging_docs,
            'site_dir': target_site_dir,
            'nav': nav,
        }

        # Set site_url if provided by GitLab CI environment
        pages_url = os.environ.get('CI_PAGES_URL')
        if pages_url:
            cfg['site_url'] = pages_url

        config_path = os.path.join(temp_dir, 'mkdocs.yml')
        with open(config_path, 'w', encoding='utf-8') as fp:
            yaml.dump(cfg, fp, sort_keys=False)

        if serve:
            print("Launching mkdocs development server...")
            subprocess.run([sys.executable, '-m', 'mkdocs', 'serve', '-f', config_path])
        else:
            print(f"Building documentation into '{output_dir}'...")
            subprocess.run(
                [sys.executable, '-m', 'mkdocs', 'build', '-f', config_path],
                check=True,
            )
            print(f"Documentation successfully built into '{output_dir}'.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Build Toubkal HPC documentation dynamically."
    )
    parser.add_argument(
        '--output',
        default='public',
        help="Output directory for static site (default: public)",
    )
    parser.add_argument(
        '--serve',
        action='store_true',
        help="Start local development server instead of building",
    )
    args = parser.parse_args()

    build_docs(output_dir=args.output, serve=args.serve)
