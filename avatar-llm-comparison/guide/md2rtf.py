"""Minimal Markdown -> RTF converter: headings, paragraphs, bullet/numbered lists, tables, fenced code, bold/italic/code/links."""
import re, sys

def esc(s):
    out = []
    for ch in s:
        if ch in '\\{}':
            out.append('\\' + ch)
        elif ord(ch) > 127:
            o = ord(ch)
            if o > 0xFFFF:
                out.append('?')
            else:
                out.append('\\u%d?' % (o - 65536 if o > 32767 else o))
        else:
            out.append(ch)
    return ''.join(out)

def inline(s):
    # links: [text](url) -> text (url)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', lambda m: m.group(1) + ' (' + m.group(2) + ')', s)
    # escape first, then apply markup on escaped text (markers contain no escapable chars)
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'{\\b \1}', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'{\\i \1}', s)
    s = re.sub(r'`([^`]+)`', r'{\\f1\\fs18 \1}', s)
    return s

def table(rows):
    rows = [r for r in rows if not re.match(r'^\s*\|?\s*:?-{3,}', r)]
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    ncol = max(len(c) for c in cells)
    width = 9360  # twips, ~6.5in
    out = []
    for i, row in enumerate(cells):
        row += [''] * (ncol - len(row))
        out.append('\\trowd\\trgaph80\\trleft0')
        x = 0
        for _ in range(ncol):
            x += width // ncol
            out.append('\\clbrdrt\\brdrs\\brdrw10\\clbrdrl\\brdrs\\brdrw10\\clbrdrb\\brdrs\\brdrw10\\clbrdrr\\brdrs\\brdrw10' + ('\\clcbpat3' if i == 0 else '') + '\\cellx%d' % x)
        for c in row:
            txt = inline(c)
            if i == 0:
                txt = '{\\b ' + txt + '}'
            out.append('\\pard\\intbl\\fs18 ' + txt + '\\cell')
        out.append('\\row')
    out.append('\\pard\\sa120\\par')
    return '\n'.join(out)

def convert(md):
    lines = md.split('\n')
    out = [r'{\rtf1\ansi\deff0{\fonttbl{\f0\fswiss Calibri;}{\f1\fmodern Courier New;}}{\colortbl;\red0\green0\blue0;\red60\green60\blue60;\red232\green232\blue232;}\fs22\sa120']
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                buf.append(lines[i]); i += 1
            out.append('\\pard\\sa0\\f1\\fs16 ' + '\\line '.join(esc(b) for b in buf) + '\\par\\pard\\sa120\\f0\\fs22')
            i += 1; continue
        if ln.strip() == '---':
            out.append('\\pard\\brdrb\\brdrs\\brdrw10\\brsp20\\sa120\\par'); i += 1; continue
        m = re.match(r'^(#{1,3})\s+(.*)', ln)
        if m:
            lvl = len(m.group(1)); size = {1: 40, 2: 30, 3: 25}[lvl]
            out.append('\\pard\\sb240\\sa120\\keepn{\\b\\fs%d %s}\\par' % (size, inline(m.group(2))))
            i += 1; continue
        if ln.lstrip().startswith('|'):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                buf.append(lines[i]); i += 1
            out.append(table(buf)); continue
        m = re.match(r'^(\s*)[-*]\s+(.*)', ln)
        if m:
            while i < len(lines) and re.match(r'^(\s*)[-*]\s+(.*)', lines[i]):
                mm = re.match(r'^(\s*)[-*]\s+(.*)', lines[i])
                text = mm.group(2); i += 1
                while i < len(lines) and lines[i].startswith('  ') and lines[i].strip() and not re.match(r'^\s*[-*]\s', lines[i]):
                    text += ' ' + lines[i].strip(); i += 1
                out.append("\\pard\\fi-360\\li720\\sa80{\\pntext\\'b7\\tab}{\\*\\pn\\pnlvlblt\\pnf0\\pnindent360{\\pntxtb\\'b7}}" + inline(text) + '\\par')
            out.append('\\pard\\sa120'); continue
        m = re.match(r'^\s*(\d+)\.\s+(.*)', ln)
        if m:
            while i < len(lines) and re.match(r'^\s*(\d+)\.\s+(.*)', lines[i]):
                mm = re.match(r'^\s*(\d+)\.\s+(.*)', lines[i])
                out.append('\\pard\\fi-360\\li720\\sa80 %s.\\tab %s\\par' % (mm.group(1), inline(mm.group(2)))); i += 1
            out.append('\\pard\\sa120'); continue
        if not ln.strip():
            i += 1; continue
        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3}\s|\s*[-*]\s|\s*\d+\.\s|```|\||---)', lines[i]):
            buf.append(lines[i]); i += 1
        out.append('\\pard\\sa120 ' + inline(' '.join(b.strip() for b in buf)) + '\\par')
    out.append('}')
    return '\n'.join(out)

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    open(dst, 'w', encoding='ascii', errors='strict').write(convert(open(src, encoding='utf-8').read()))
    print('wrote', dst)
