#!/usr/bin/env python3
from __future__ import annotations

import html
import os
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "oldsite" / "kotek.net" / "www"
CONTENT = ROOT / "content"
STATIC = ROOT / "static"

BLOG_DATES: dict[str, str] = {
    "astronomy_and_gis": "2007-07-30",
    "spring_bean_name_resolver": "2007-08-21",
    "spring_and_memento_pattern": "2007-09-17",
    "writing_fast_nio_webserver": "2008-09-05",
    "label_layout_algorithm": "2009-01-17",
    "pixy2": "2009-02-05",
    "more_realistic_view_on_groovy": "2009-06-09",
    "piccolo_and_svg": "2009-11-07",
    "using_ant_and_javac_without_installation": "2009-11-30",
    "rangeset_and_huge_datasets": "2009-11-30",
    "swingutilities.invokeandwait_with_return_value": "2010-11-11",
    "junit3_scala_testcase": "2010-11-28",
    "jdbm2_released": "2010-12-19",
    "enumeration_problem_at_scala_2.8.1": "2010-12-20",
    "jdbm_2.1_and_beyond": "2011-01-16",
    "quick_look_at_upcoming_parallel_collections_in_scala_2.9": "2011-03-29",
    "galway_sky_atlas_1st_edition": "2011-04-12",
    "scala_problems": "2011-07-06",
    "jdbm_3_is_coming": "2011-10-23",
    "pixy2_updated": "2011-11-01",
    "jdbm_3.0_alpha_1_released": "2012-01-18",
    "kotlin_pre-pre-pre_alpha_survival_guide": "2012-02-16",
    "announcing_JDBM4": "2012-06-08",
    "JDBM4_now_open_for_public": "2012-09-16",
    "JDBM4_renamed_to_MapDB": "2012-11-03",
    "3G_map": "2012-11-12",
    "MapDB_Future": "2013-04-23",
    "MapDB_Reloaded": "2013-06-19",
    "MapDB_09_format_support": "2013-07-01",
    "MapDB_and_the_road_ahead": "2013-09-25",
    "MapDB_1_in_january": "2013-11-06",
    "MapDB_and_CodeFutures": "2014-01-21",
    "MapDB_Roadmap_and_near_future": "2014-05-14",
    "MapDB_11_and_unsafe": "2014-07-01",
    "MapDB_20_is_near": "2015-06-16",
    "MapDB_2_beta_1": "2015-06-29",
    "MapDB_update": "2015-09-25",
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def title_from_markdown(text: str, fallback: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines[:-1]):
        if line.strip() and re.match(r"^=+\s*$", lines[index + 1].strip()):
            return line.strip()
    for line in lines:
        match = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", match.group(1)))).strip()
    return fallback


def first_paragraph(text: str) -> str:
    body = text
    body = re.sub(r"^\s*.+\n=+\s*\n", "", body, count=1)
    body = re.sub(r"^\s*#.*\n", "", body, count=1).strip()
    blocks = [block.strip() for block in re.split(r"\n\s*\n", body) if block.strip()]
    if not blocks:
        return ""
    return blocks[0]


def plain_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_]+", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def rewrite_same_domain_links(text: str) -> str:
    text = re.sub(r"https?://(?:www\.)?kotek\.net/blog/([A-Za-z0-9_.-]+)", r"/blog/\1/", text)
    text = re.sub(r"https?://(?:www\.)?kotek\.net/(consulting|publications|contact|asterope)/?", r"/\1/", text)
    return text


def strip_self_closing_p(text: str) -> str:
    return re.sub(r"<p\s*/?>", "\n", text)


def remove_zip_entry(path: Path, entry_name: str) -> None:
    stat = path.stat()
    with zipfile.ZipFile(path, "r") as src:
        infos = [info for info in src.infolist() if info.filename != entry_name]
        if len(infos) == len(src.infolist()):
            return

        tmp = path.with_suffix(path.suffix + ".tmp")
        with zipfile.ZipFile(tmp, "w") as dst:
            for info in infos:
                dst.writestr(info, src.read(info.filename))
    tmp.replace(path)
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))


def toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def page_frontmatter(
    title: str,
    *,
    template: str = "page.html",
    path: str | None = None,
    date: str | None = None,
    description: str | None = None,
    render_title: bool = False,
) -> str:
    lines = ["+++", f"title = {toml_string(title)}", f'template = "{template}"']
    if description:
        lines.append(f"description = {toml_string(description)}")
    if path:
        lines.append(f'path = "{path}"')
    if date:
        lines.append(f"date = {date}")
    lines.append("[extra]")
    lines.append(f"render_title = {str(render_title).lower()}")
    lines.append("+++")
    return "\n".join(lines) + "\n\n"


def section_frontmatter(title: str, *, template: str, sort_by: str | None = None) -> str:
    lines = ["+++", f"title = {toml_string(title)}", f'template = "{template}"']
    if sort_by:
        lines.append(f'sort_by = "{sort_by}"')
    lines.append("+++")
    return "\n".join(lines) + "\n\n"


def migrate_pages() -> None:
    pages = [
        ("_index.md", OLD / "index.md.html", "Jan Kotek", "index.html"),
        ("consulting.md", OLD / "consulting" / "index.md.html", "Consulting", "page.html"),
        ("contact.md", OLD / "contact" / "index.md.html", "Contact", "page.html"),
        ("publications.md", OLD / "publications" / "index.md", "Publications", "page.html"),
        ("asterope.md", OLD / "asterope" / "index.md", "Asterope", "page.html"),
    ]

    for target, source, fallback_title, template in pages:
        text = strip_self_closing_p(rewrite_same_domain_links(source.read_text(encoding="utf-8")))
        title = title_from_markdown(text, fallback_title)
        write(CONTENT / target, page_frontmatter(title, template=template) + text.rstrip() + "\n")


def migrate_blog() -> None:
    blog_dir = CONTENT / "blog"
    blog_dir.mkdir(parents=True, exist_ok=True)
    intro = "<h1>Blog</h1>\n<p><b>NOTE:</b> Blog has moved to <a href=\"http://www.mapdb.org/blog/\">new location</a> at mapdb.org.</p>\n"
    write(blog_dir / "_index.md", section_frontmatter("Blog", template="section.html", sort_by="date") + intro)

    for source in sorted((OLD / "blog").glob("*.md")):
        match = re.match(r"^(\d+)\s+(.+)\.md$", source.name)
        if not match:
            continue
        slug = match.group(2)
        date = BLOG_DATES.get(slug)
        if not date:
            print(f"WARNING: no date for {slug}, skipping")
            continue
        text = rewrite_same_domain_links(source.read_text(encoding="utf-8").rstrip())
        title = title_from_markdown(text, slug.replace("_", " "))
        summary = first_paragraph(text)
        content = text
        if summary and "<!-- more -->" not in content:
            content = content.replace(summary, summary + "\n\n<!-- more -->", 1)

        fm = page_frontmatter(
            title,
            path=f"blog/{slug}",
            date=date,
            description=plain_text(summary),
        )
        write(blog_dir / f"{slug}.md", fm + content + "\n")


def copy_assets() -> None:
    static_roots = ["img", "down"]
    for name in static_roots:
        src = OLD / name
        dst = STATIC / name
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    asterope = STATIC / "asterope"
    asterope.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OLD / "asterope" / "m45.jpg", asterope / "m45.jpg")

    remove_zip_entry(STATIC / "down" / "mapdb-demo2.zip", "mapdb-demo2/hs_err_pid5139.log")


def main() -> None:
    clean_dir(CONTENT)
    clean_dir(STATIC)
    migrate_pages()
    migrate_blog()
    copy_assets()


if __name__ == "__main__":
    main()
