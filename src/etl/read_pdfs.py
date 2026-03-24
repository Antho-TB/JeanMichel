import sys
try:
    import fitz
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyMuPDF', '--quiet'])
    import fitz

files = [
    r'c:\Users\abezille\dev\MyReport\Vu Visio.pdf',
    r'c:\Users\abezille\dev\MyReport\Listing appli.pdf',
    r'c:\Users\abezille\dev\MyReport\Flux niv 4.pdf'
]

with open('pdf_content.txt', 'w', encoding='utf-8') as out:
    for f in files:
        try:
            doc = fitz.open(f)
            out.write(f'\n\n--- CONTENT OF {f} ---\n')
            for i, page in enumerate(doc):
                out.write(f'Page {i+1}:\n')
                out.write(page.get_text() + '\n')
            doc.close()
        except Exception as e:
            out.write(f'Error reading {f}: {e}\n')
