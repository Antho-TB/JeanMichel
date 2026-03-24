import os

md_path = r"C:\Users\abezille\.gemini\antigravity\brain\eed92070-da65-4021-87cf-e6fc26b0ca37\presentation_migration_achats.md"
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Nettoyage des balises du carrousel de l'agent
content = content.replace("````carousel\n", "").replace("\n````", "")

html_template = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Migration Data Achats - Sylob V25</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reset.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/white.min.css">
  <style>
    .reveal h1 {{ font-size: 1.8em; color: #2C3E50; text-transform: none; text-align: center; }}
    .reveal h2 {{ font-size: 1.4em; color: #34495E; text-transform: none; }}
    .reveal table {{ font-size: 0.6em; width: 100%; border-collapse: collapse; margin-top: 20px; }}
    .reveal th {{ background-color: #3498DB; color: white; padding: 12px; }}
    .reveal td {{ border: 1px solid #BDC3C7; padding: 10px; }}
    .reveal blockquote {{ background: #EAEDED; padding: 15px; border-left: 5px solid #E74C3C; font-size: 0.7em; text-align: left; width: 90%; margin: 20px auto; }}
    .mermaid {{ display: flex; justify-content: center; font-size: 16px; margin-top: 20px; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section data-markdown>
        <textarea data-template>
{content}
        </textarea>
      </section>
    </div>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/plugin/markdown/markdown.js"></script>
  <script>
    mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    Reveal.initialize({{
      plugins: [ RevealMarkdown ],
      markdown: {{ separator: '<!-- slide -->' }},
      width: '100%',
      height: '100%',
      margin: 0.1,
      minScale: 1,
      maxScale: 1
    }}).then(() => {{
      setTimeout(() => {{
        mermaid.init(undefined, document.querySelectorAll('.language-mermaid'));
      }}, 500);
    }});
  </script>
</body>
</html>
"""

output_path = r"C:\Users\abezille\dev\MyReport\Presentation_Sylob_Achats.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Presentation HTML generee dans : {output_path}")
