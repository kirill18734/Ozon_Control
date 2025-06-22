import os
import shutil
from pathlib import Path
import PyInstaller.__main__


def build():
    root = Path(__file__).resolve().parent
    exe_name = 'OzonControl'

    options = [
        str(root / 'main.py'),
        '--onefile',
        '--noconsole',
        f'--name={exe_name}',
    ]

    data_dirs = [
        'ScreenToPrint',
        'UI',
        'expansion',
        'local_print_server',
        'Tesseract-OCR',
    ]
    data_files = [
        'config.json',
        'img_black.png',
        'img_white.png',
        'screenshot.png',
    ]

    sep = ';' if os.name == 'nt' else ':'
    for item in data_dirs:
        options.append(f'--add-data={root / item}{sep}{item}')
    for item in data_files:
        options.append(f'--add-data={root / item}{sep}{item}')

    PyInstaller.__main__.run(options)

    suffix = '.exe' if os.name == 'nt' else ''
    dist_exe = root / 'dist' / (exe_name + suffix)
    if dist_exe.exists():
        final_path = root / dist_exe.name
        shutil.move(dist_exe, final_path)
        shutil.rmtree(root / 'build', ignore_errors=True)
        shutil.rmtree(root / 'dist', ignore_errors=True)
        spec_file = root / f'{exe_name}.spec'
        if spec_file.exists():
            spec_file.unlink()
        print(f'Executable created: {final_path}')
    else:
        print('Executable not found. Check PyInstaller output.')


if __name__ == '__main__':
    build()
