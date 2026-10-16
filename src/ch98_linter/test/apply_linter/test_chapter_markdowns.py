from re import findall as re_findall, compile as re_compile, IGNORECASE as re_IGNORECASE
from pathlib import Path
from pytest import mark as pytest_mark
from collections import defaultdict
from pathlib import Path


def get_image_paths_from_markdown(md_text: str) -> list[str]:
    """Extract image paths from markdown and html img tags."""
    markdown_imgs = re_findall(r"!\[[^\]]*]\(([^)]+)\)", md_text)
    html_imgs = re_findall(r'<img[^>]*src=["\']([^"\']+)["\']', md_text)
    return markdown_imgs + html_imgs


def get_missing_markdown_image_file_links(src_dir: Path) -> list[str]:
    missing_files: list[str] = []
    for md_file in src_dir.rglob("*.md"):
        # print(f"{md_file=}")
        md_text = md_file.read_text(encoding="utf-8")

        for image_path_str in get_image_paths_from_markdown(md_text):
            image_path_str = image_path_str.strip()
            if image_path_str.startswith(("http://", "https://")):
                continue

            if image_path_str.startswith("/"):
                image_path = src_dir / image_path_str.lstrip("/")
            else:
                image_path = md_file.parent / image_path_str

            if not image_path.exists():
                missing_files.append(f"{md_file}: image not found -> {image_path_str}")
    return missing_files


def get_all_images_with_metadata(src_dir: Path) -> list[str]:
    failures = []
    for image_path in src_dir.rglob("*"):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        data = image_path.read_bytes()

        if found_markers := [
            marker.decode(errors="ignore")
            for marker in FORBIDDEN_MARKERS
            if marker in data
        ]:
            failures.append(f"{image_path}: found metadata markers {found_markers}")
    return failures


@pytest_mark.skip_on_linux
def test_MarkdownImageLinksFilesExist() -> None:
    # GIVEN
    # repo_root = Path("src").resolve().parents[1]
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    missing_files = get_missing_markdown_image_file_links(src_dir)

    # THEN
    assert not missing_files, "\n".join(missing_files)


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
FORBIDDEN_MARKERS = {
    b"Exif",
    b"http://ns.adobe.com/xap",  # XMP
    b"Photoshop",
    b"ICC_PROFILE",
    b"XML:com.adobe.xmp",
    b"tEXt",
    b"iTXt",
    b"zTXt",
}


# # TODO activate this test
# def test_images_HaveNoMetadata_AllImagesInSrc():
#     # GIVEN
#     src_dir = Path(__file__).resolve().parents[3]
#     # WHEN
#     failures = get_all_images_with_metadata(src_dir)
#     # THEN
#     assertion_failure_str = "Images containing metadata were found:\n"
#     assert not failures, assertion_failure_str + "\n".join(failures)


def get_markdown_footnote_failures(src_dir: Path) -> list[str]:
    failures: list[str] = []

    footnote_pattern = r"\[\^([^\]]+)\]"

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        footnotes = re_findall(footnote_pattern, md_text)

        counts: dict[str, int] = {}
        for footnote in footnotes:
            counts[footnote] = counts.get(footnote, 0) + 1

        failures.extend(
            f"{md_file}: footnote [^{footnote}] appears {count} times (expected 2)"
            for footnote, count in sorted(counts.items())
            if count != 2
        )
    return failures


def test_MarkdownFootnotesAreMirrored() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    failures = get_markdown_footnote_failures(src_dir)

    # THEN
    assert not failures, "\n".join(failures)


def get_markdown_footnote_order_failures(src_dir: Path) -> list[str]:
    failures: list[str] = []

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        references = [int(x) for x in re_findall(r"\[\^(\d+)\](?!:)", md_text)]

        expected = list(range(1, len(references) + 1))

        if references != expected:
            failures.append(
                f"{md_file}: footnotes are out of order "
                f"\n(found   {references}"
                f"\nexpected {expected})"
            )

    return failures


def test_MarkdownFootnotesAreInOrder() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    failures = get_markdown_footnote_order_failures(src_dir)

    # THEN
    assert not failures, "\n".join(failures)


def get_file_paths_from_markdown(md_text: str) -> list[str]:
    """Extract markdown file links (excluding images)."""
    return re_findall(r"(?<!!)\[[^\]]*]\(([^)]+)\)", md_text)


def get_missing_markdown_file_links(src_dir: Path) -> list[str]:
    missing_files: list[str] = []

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        for file_path_str in get_file_paths_from_markdown(md_text):
            file_path_str = file_path_str.strip()

            # Skip anchors
            if file_path_str.startswith("#"):
                continue

            # Skip external links
            if file_path_str.startswith(("http://", "https://")):
                continue

            # Remove anchor portion from local links
            file_path_str = file_path_str.split("#")[0]

            if not file_path_str:
                continue

            if file_path_str.startswith("/"):
                file_path = src_dir / file_path_str.lstrip("/")
            else:
                file_path = md_file.parent / file_path_str

            if not file_path.exists():
                missing_files.append(f"{md_file}: file not found -> {file_path_str}")

    return missing_files


def test_MarkdownFileLinksFilesExist() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    missing_files = get_missing_markdown_file_links(src_dir)

    # THEN
    assert not missing_files, "\n".join(missing_files)


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico"}


def get_referenced_images(src_dir: Path) -> set[Path]:
    referenced: set[Path] = set()

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        for image_path_str in get_image_paths_from_markdown(md_text):
            image_path_str = image_path_str.strip()

            # Skip external links
            if image_path_str.startswith(("http://", "https://")):
                continue

            # Remove anchor/query portions if present
            image_path_str = image_path_str.split("#")[0].split("?")[0]

            if not image_path_str:
                continue

            if image_path_str.startswith("/"):
                image_path = src_dir / image_path_str.lstrip("/")
            else:
                image_path = md_file.parent / image_path_str

            referenced.add(image_path.resolve())

    return referenced


def get_unreferenced_images(src_dir: Path) -> list[str]:
    referenced_images = get_referenced_images(src_dir)
    unreferenced: list[str] = []

    for image_file in src_dir.rglob("*"):
        if image_file.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        if not image_file.is_file():
            continue

        if image_file.resolve() not in referenced_images:
            unreferenced.append(str(image_file))

    return unreferenced


@pytest_mark.skip_on_linux
def test_AllImagesAreReferencedInMarkdown() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    unreferenced_images = get_unreferenced_images(src_dir)

    # THEN
    assert not unreferenced_images, "\n".join(unreferenced_images)


def get_oversized_images(src_dir: Path, max_size_bytes: int = 100 * 1024) -> list[str]:
    oversized: list[str] = []

    for image_path in src_dir.rglob("*"):
        if (
            not image_path.is_file()
            or image_path.suffix.lower() not in IMAGE_EXTENSIONS
        ):
            continue

        size = image_path.stat().st_size
        if size > max_size_bytes:
            oversized.append(
                f"{image_path}: {size // 1024}kb (limit {max_size_bytes // 1024}kb)"
            )

    return oversized


def test_AllImagesUnder100kb() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    oversized_images = get_oversized_images(src_dir)

    # THEN
    assert not oversized_images, "\n".join(oversized_images)


IMAGE_TAG_PATTERN = re_compile(
    r'<img\b[^>]*\balt="([^"]+)"',
    flags=re_IGNORECASE,
)


def test_markdown_ImageDescriptionsAreUniqueAcrossCodebase_Scenario1_NoDuplicateAltText() -> (
    None
):
    # ESTABLISH
    root_dir = Path("src")

    alt_text_locations: dict[str, list[Path]] = defaultdict(list)

    # WHEN
    for markdown_path in root_dir.rglob("*.md"):
        content = markdown_path.read_text(encoding="utf-8")

        for match in IMAGE_TAG_PATTERN.finditer(content):
            alt_text = match.group(1).strip()
            alt_text_locations[alt_text].append(markdown_path)

    duplicates = {
        alt_text: sorted(str(path) for path in paths)
        for alt_text, paths in alt_text_locations.items()
        if len(paths) > 1
    }

    # THEN
    assertion_fail_str = "Duplicate image descriptions found:\n" + "\n".join(
        f'  alt="{alt_text}"\n    ' + "\n    ".join(paths)
        for alt_text, paths in sorted(duplicates.items())
    )
    assert not duplicates, assertion_fail_str


SKIPPED_DIR_NAMES = {".git", ".venv", "node_modules"}


def get_markdown_bold_line_br_failures(src_dir: Path) -> list[str]:
    failures = []
    for chapter_dir in sorted(src_dir.glob("ch[0-9][0-9]_*")):
        if not chapter_dir.is_dir():
            continue
        for md_path in sorted(chapter_dir.glob("*.md")):
            lines = md_path.read_text(encoding="utf-8").splitlines()
            for line_number, line in enumerate(lines, start=1):
                if line.strip() == "***":
                    continue
                if line.startswith("**") and not line.endswith("<br>"):
                    failures.append(f"{md_path}:{line_number}: {line!r}")
    return failures


def test_MarkdownLinesStartingWithBoldEndWithBr() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    failures = get_markdown_bold_line_br_failures(src_dir)

    # THEN
    print(f"{len(failures)=}")
    assert not failures, "\n".join(failures)
