from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def has_files(patterns: list[str]) -> bool:
    return any(any(Path('.').glob(pattern)) for pattern in patterns)


def node_quality() -> bool:
    package = Path('package.json')
    if not package.exists():
        return False

    data = json.loads(package.read_text(encoding='utf-8'))
    scripts = data.get('scripts', {}) if isinstance(data, dict) else {}

    if Path('pnpm-lock.yaml').exists() and shutil.which('pnpm'):
        run(['pnpm', 'install', '--frozen-lockfile'])
        prefix = ['pnpm']
    elif Path('yarn.lock').exists() and shutil.which('yarn'):
        run(['yarn', 'install', '--frozen-lockfile'])
        prefix = ['yarn']
    else:
        if Path('package-lock.json').exists():
            run(['npm', 'ci'])
        else:
            run(['npm', 'install'])
        prefix = ['npm', 'run']

    for name in ('lint', 'test', 'build'):
        if name in scripts:
            if prefix == ['pnpm']:
                run(['pnpm', 'run', name])
            elif prefix == ['yarn']:
                run(['yarn', name])
            else:
                run(['npm', 'run', name])
    return True


def dotnet_quality() -> bool:
    solutions = sorted(Path('.').glob('*.sln'))
    projects = sorted(Path('.').glob('**/*.csproj'))
    if not solutions and not projects:
        return False

    targets = solutions if solutions else projects
    for target in targets:
        target_text = str(target)
        run(['dotnet', 'restore', target_text])
        run(['dotnet', 'build', target_text, '--no-restore', '--configuration', 'Release'])
        run(['dotnet', 'test', target_text, '--no-build', '--configuration', 'Release'])
    return True


def python_quality() -> bool:
    markers = [Path('pyproject.toml'), Path('requirements.txt'), Path('setup.py')]
    if not any(p.exists() for p in markers):
        return False

    if Path('requirements.txt').exists():
        run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    elif Path('pyproject.toml').exists():
        run([sys.executable, '-m', 'pip', 'install', '.'])

    if has_files(['tests/**/*.py', 'test_*.py', '**/test_*.py', '**/*_test.py']):
        run([sys.executable, '-m', 'pip', 'install', 'pytest'])
        run([sys.executable, '-m', 'pytest', '-q'])
    else:
        print('Python project detected but no pytest-style test files were found.')
    return True


def main() -> int:
    detected = []
    try:
        if node_quality():
            detected.append('Node.js')
        if dotnet_quality():
            detected.append('.NET')
        if python_quality():
            detected.append('Python')
    except subprocess.CalledProcessError as exc:
        print(f'Quality gate failed with exit code {exc.returncode}.', file=sys.stderr)
        return exc.returncode or 1

    if not detected:
        print('No supported project stack detected. Configure project-specific commands in .github/scripts/run_quality_gates.py.')
    else:
        print('Completed quality gates for:', ', '.join(detected))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
