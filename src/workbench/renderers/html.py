"""HTML renderers for deliverables."""

from __future__ import annotations

from markdown import markdown

from workbench.renderers.markdown import render_brief, render_matrix, render_slides


def render_brief_html(deliverable) -> str:
    return markdown(render_brief(deliverable), extensions=["tables"])


def render_matrix_html(deliverable) -> str:
    return markdown(render_matrix(deliverable), extensions=["tables"])


def render_slides_html(deliverable) -> str:
    sections = [
        "<article class='deck'>",
        "<header><h1>{}</h1><p>{}</p></header>".format(deliverable.title, deliverable.deck_goal),
    ]
    for slide in deliverable.slides:
        sections.append("<section class='slide'>")
        sections.append("<div class='slide-kicker'>Slide {}</div>".format(slide.slide_number))
        sections.append("<h2>{}</h2>".format(slide.title))
        sections.append("<ul>")
        for bullet in slide.bullets:
            traces = " ".join("<span class='trace-badge'>{}</span>".format(trace.locator.label) for trace in bullet.trace_refs)
            sections.append("<li><span>{}</span>{}</li>".format(bullet.text, traces))
        sections.append("</ul>")
        if slide.speaker_notes:
            sections.append("<div class='speaker-notes'><h3>Speaker Notes</h3><ul>")
            for note in slide.speaker_notes:
                sections.append("<li>{}</li>".format(note.text))
            sections.append("</ul></div>")
        sections.append("</section>")
    sections.append("</article>")
    return "".join(sections)

