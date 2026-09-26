#!/usr/bin/env python3
"""
HTML Styler & Markdown Converter for Canvas LMS Courses
Implements institutional DesignPLUS-compliant page ribbons and clean inner page styling.

Features:
- Pure Python standard library (no pip dependencies).
- Selective Banner Ribbon Generator (for Front Page, Orientation, Unit Overviews, Syllabus).
- Clean Standard Layout Generator (for subpages, readings, lab guides, drills).
- Markdown-to-HTML parser:
  * Styled markdown tables with Navy Blue headers (#1e3a8a) & alternating zebra rows (#f8fafc).
  * Styled dark Consolas code blocks (#0f172a).
  * Styled expandable details accordions (<details><summary>).
  * Styled inline code and lead cards.
"""

import re
import html
from typing import List, Tuple, Optional


def format_inline(s: str) -> str:
    """Formats inline markdown syntax to HTML."""
    s = re.sub(
        r"`([^`]+)`",
        r'<code style="background: #f1f5f9; color: #0369a1; padding: 0.15rem 0.35rem; border-radius: 3px; font-size: 0.9em; font-family: Consolas, monospace; font-weight: 600;">\1</code>',
        s
    )
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    s = s.replace(r"$\rightarrow$", "&rarr;")
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def parse_markdown_to_html(md: str) -> str:
    """Converts structured markdown (tables, code blocks, lists, details) into clean styled HTML."""
    if not md:
        return ""

    code_blocks = []
    def code_block_sub(match):
        lang = match.group(1) or ""
        code = match.group(2)
        idx = len(code_blocks)
        code_html = (
            f'<div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 6px; '
            f'overflow-x: auto; margin: 1.25rem 0; font-family: Consolas, Monaco, monospace; font-size: 0.9em; '
            f'line-height: 1.5;"><pre style="margin: 0; background: transparent; color: inherit;"><code>{html.escape(code.strip())}</code></pre></div>'
        )
        code_blocks.append(code_html)
        return f"__CODE_BLOCK_{idx}__"

    text = re.sub(r"```([a-zA-Z0-9_-]*)\r?\n(.*?)\r?\n```", code_block_sub, md, flags=re.DOTALL)

    lines = text.splitlines()
    output = []
    in_table = False
    table_rows = []
    in_list = False
    list_type = None

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return ""
        html_table = [
            '<div style="overflow-x: auto; margin: 1.25rem 0;"><table style="width: 100%; border-collapse: collapse; border: 1px solid #cbd5e1; font-size: 0.95em;">'
        ]
        header_cells = table_rows[0]
        html_table.append('<thead><tr style="background-color: #1e3a8a; color: #ffffff;">')
        for c in header_cells:
            html_table.append(f'<th style="padding: 10px 14px; border: 1px solid #94a3b8; font-weight: 600;">{format_inline(c)}</th>')
        html_table.append("</tr></thead><tbody>")
        for row_idx, row in enumerate(table_rows[1:]):
            bg = "#f8fafc" if row_idx % 2 == 0 else "#ffffff"
            html_table.append(f'<tr style="background-color: {bg};">')
            for c in row:
                html_table.append(f'<td style="padding: 8px 14px; border: 1px solid #cbd5e1;">{format_inline(c)}</td>')
            html_table.append("</tr>")
        html_table.append("</tbody></table></div>")
        in_table = False
        table_rows = []
        return "".join(html_table)

    def flush_list():
        nonlocal in_list, list_type
        if not in_list:
            return ""
        tag = list_type
        in_list = False
        list_type = None
        return f"</{tag}>\n"

    for line in lines:
        trimmed = line.strip()

        if trimmed.startswith("|") and trimmed.endswith("|"):
            cells = [c.strip() for c in trimmed[1:-1].split("|")]
            if re.match(r"^[:\- ]+$", "".join(cells)):
                pass
            else:
                if not in_table:
                    if in_list:
                        output.append(flush_list())
                    in_table = True
                    table_rows = [cells]
                else:
                    table_rows.append(cells)
            continue
        elif in_table:
            output.append(flush_table())

        if not trimmed:
            if in_list:
                output.append(flush_list())
            continue

        cb_match = re.match(r"^__CODE_BLOCK_(\d+)__$", trimmed)
        if cb_match:
            if in_list:
                output.append(flush_list())
            idx = int(cb_match.group(1))
            output.append(code_blocks[idx])
            continue

        h_match = re.match(r"^(#{1,6})\s+(.*)$", trimmed)
        if h_match:
            if in_list:
                output.append(flush_list())
            level = len(h_match.group(1))
            h_text = format_inline(h_match.group(2).strip())
            if level == 1:
                output.append(f'<h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{h_text}</h2>')
            elif level == 2:
                output.append(f'<h3 style="color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.3rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{h_text}</h3>')
            elif level == 3:
                output.append(f'<h4 style="color: #0f172a; margin-top: 1.25rem; margin-bottom: 0.5rem; font-size: 1.15em;">{h_text}</h4>')
            else:
                output.append(f'<h5 style="color: #334155; margin-top: 1rem; margin-bottom: 0.5rem; font-size: 1.05em;">{h_text}</h5>')
            continue

        if trimmed in ("---", "***", "___"):
            if in_list:
                output.append(flush_list())
            output.append('<hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0;"/>')
            continue

        if trimmed.startswith("<details>"):
            if in_list:
                output.append(flush_list())
            output.append('<details style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0.75rem 1.25rem; margin: 1rem 0;">')
            continue

        if trimmed.startswith("<summary>"):
            s_content = trimmed.replace("<summary>", "").replace("</summary>", "").strip()
            output.append(f'<summary style="font-weight: 600; color: #1e3a8a; cursor: pointer; padding: 0.25rem 0;">{format_inline(s_content)}</summary>')
            continue

        if trimmed.startswith("</details>"):
            output.append("</details>")
            continue

        ul_match = re.match(r"^[-*+]\s+(.*)$", trimmed)
        if ul_match:
            if not in_list or list_type != "ul":
                if in_list:
                    output.append(flush_list())
                output.append('<ul style="line-height: 1.6; margin: 0.5rem 0; padding-left: 1.5rem;">')
                in_list = True
                list_type = "ul"
            output.append(f"<li>{format_inline(ul_match.group(1))}</li>")
            continue

        ol_match = re.match(r"^\d+\.\s+(.*)$", trimmed)
        if ol_match:
            if not in_list or list_type != "ol":
                if in_list:
                    output.append(flush_list())
                output.append('<ol style="line-height: 1.6; margin: 0.5rem 0; padding-left: 1.5rem;">')
                in_list = True
                list_type = "ol"
            output.append(f"<li>{format_inline(ol_match.group(1))}</li>")
            continue

        if in_list:
            output.append(flush_list())

        output.append(f'<p style="line-height: 1.6; margin: 0.75rem 0;">{format_inline(trimmed)}</p>')

    if in_table:
        output.append(flush_table())
    if in_list:
        output.append(flush_list())

    return "\n".join(output)


def render_designplus_html(
    page_title: str,
    lead_paragraph: str,
    accordion_panels: List[Tuple[str, str]],
    page_id: str,
    icon_class: str = "far fa-compass"
) -> str:
    """
    Renders a DesignPLUS-compliant page with the signature top ribbon banner and accordion sections.
    Use on: Home Page, Start Here, Unit Overviews, and Syllabus.
    """
    panels_html = []
    for idx, (panel_title, panel_content) in enumerate(accordion_panels, 1):
        panels_html.append(f"""
<div class="dp-content-block">
<h3 class="dp-has-icon dp-locked"><i class="far fa-folder-open"><span class="dp-icon-content" style="display: none;">&nbsp;</span></i> <span>{panel_title}</span></h3>
<div class="dp-panel-body" style="padding-left: 1rem; border-left: 2px solid #e2e8f0; margin-bottom: 1.5rem;">
{panel_content}
</div>
</div>""")

    body_content = "\n".join(panels_html)

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(page_title)}</title>
</head>
<body>
<div id="dp-wrapper" class="dp-wrapper dp-hdg-i-cp-brdr-h2-dp-primary dp-hdg-txt-h3-dp-primary dp-hdg-txt-h4-dp-primary dp-hdg-txt-h5-dp-primary dp-hdg-i-cp-brdr-h5-dp-primary dp-hdg-b-h2-brdr-b dp-hdg-txt-h6-dp-primary dp-hdg-i-cp-brdr-h6-dp-primary dp-hdg-i-styl-h2-pill dp-hdg-i-styl-h3-pill dp-hdg-cp-brdr-h3-dp-secondary dp-hdg-cp-brdr-h2-dp-secondary dp-hdg-brdr-h2-1 dp-hdg-brdr-h3-1 dp-hdg-brdr-h4-1 dp-hdg-brdr-h5-1 dp-hdg-brdr-h6-1 dp-hdg-i-sz-h2-fill dp-hdg-i-sz-h3-fill dp-hdg-i-sz-h5-fill dp-hdg-i-sz-h6-fill dp-hdg-i-brdr-h5-2 dp-hdg-i-brdr-h6-2 dp-hdg-b-h3-brdr-b dp-hdg-txt-h2-dp-primary dp-hdg-i-brdr-h2-1 dp-hdg-i-brdr-h3-1 dp-hdg-i-sz-h4-fill dp-hdg-i-cp-brdr-h3-dp-primary dp-hdg-i-brdr-h4-1 dp-hdg-i-bg-h2-dp-primary dp-hdg-i-bg-h3-dp-primary dp-hdg-b-h4-brdr-b dp-hdg-d-h4-table-l dp-hdg-i-styl-h4-pill dp-hdg-i-cp-brdr-h4-dp-primary">
<div class="dp-content-block">
<header class="dp-header dp-basic-bar dp-header-s-brdr-l dp-header-brdr-w-4 dp-header-out-dp-secondary dp-header-pre-s-brdr-r dp-header-pre-font-sm dp-header-pre-out-dp-secondary dp-header-sub-brdr-w-0 dp-header-desc-txt-dp-primary dp-header-desc-out-dp-primary dp-header-sub-bg-dp-white dp-header-sub-txt-dp-primary dp-header-sub-out-dp-primary">
<h2 class="dp-heading dp-locked"><span class="dp-header-title">{html.escape(page_title)}</span></h2>
</header>
<p>&nbsp;</p>
<div class="dp-lead-paragraph" style="font-size: 1.1em; line-height: 1.6; color: #1e293b; margin-bottom: 1.5rem;">
{lead_paragraph}
</div>
</div>
{body_content}
</div>
</body>
</html>"""


def render_standard_page_html(
    page_title: str,
    lead_paragraph: str,
    content_panels: List[Tuple[str, str]],
    page_id: str,
    workflow_state: str = "active"
) -> str:
    """
    Renders clean, distraction-free HTML for inner module pages.
    Avoids heavy repetitive banner ribbons. Uses crisp navy headers, lead card callouts, and clean margins.
    """
    panels_html = []
    for title, content in content_panels:
        panels_html.append(f"""
<section style="margin-bottom: 2rem;">
  <h3 style="color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.35rem; margin-top: 1.5rem; margin-bottom: 0.75rem; font-size: 1.25em;">{title}</h3>
  <div style="line-height: 1.6; color: #1e293b;">
    {content}
  </div>
</section>""")

    body_content = "\n".join(panels_html)

    return f"""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>{html.escape(page_title)}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; max-width: 960px; margin: 0 auto; padding: 1.5rem 1rem;">
  <header style="border-bottom: 2px solid #1e3a8a; padding-bottom: 0.75rem; margin-bottom: 1.5rem;">
    <h1 style="color: #1e3a8a; margin: 0; font-size: 1.75em;">{html.escape(page_title)}</h1>
  </header>
  
  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1rem 1.25rem; margin-bottom: 1.5rem; border-radius: 0 4px 4px 0; font-size: 1.05em; line-height: 1.6; color: #334155;">
    {lead_paragraph}
  </div>

  <main>
    {body_content}
  </main>
</body>
</html>"""
