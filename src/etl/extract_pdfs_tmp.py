import sys
import subprocess
try:
    import fitz
except ImportError:
    print("Installation de PyMuPDF...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyMuPDF', '--quiet'])
    import fitz

files = [
    r'c:\Users\abezille\dev\MyReport\Vu Visio.pdf',
    r'c:\Users\abezille\dev\MyReport\Listing appli.pdf',
    r'c:\Users\abezille\dev\MyReport\Flux niv 4.pdf'
]

for f in files:
    try:
        doc = fitz.open(f)
        print(f'\n\n--- CONTENT OF {f} ---')
        for i, page in enumerate(doc):
            print(f'Page {i+1}:')
            print(page.get_text())
        doc.close()
    except Exception as e:
        print(f'Error reading {f}: {e}')
