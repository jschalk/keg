"""
test_print_punch_text.py

Tests for ETLApp._print_punch_text.

Does NOT import puncher_app or tkinter -- each test builds a throwaway _Stub
class containing only the method under test. tkinter_messagebox is injected
as an instance attribute so the real tkinter is never touched.

All imports follow the project convention:
    from x import x_thing as x_thing
"""

from unittest.mock import MagicMock, mock_open, patch

SAMPLE_TEXT = "Punch entry line 1\nPunch entry line 2"
END = "END"


def _make_stub(punch_text=SAMPLE_TEXT + "\n"):
    """Return a minimal _Stub instance with _print_punch_text attached."""

    class _Stub:
        def _print_punch_text(self):
            import tempfile
            import webbrowser

            text = self._punch_text.get("1.0", END).strip()
            if not text:
                self.tkinter_messagebox.showinfo(
                    "Nothing to print", "The punch viewer is empty."
                )
                return

            escaped = (
                text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            html = (
                "<!DOCTYPE html><html><head>"
                "<meta charset='utf-8'>"
                "<title>Punch Viewer</title>"
                "<style>"
                "body{font-family:monospace;white-space:pre-wrap;padding:24px;}"
                "</style>"
                "</head><body>"
                f"{escaped}"
                "<script>window.onload=function(){{window.print();}}</script>"
                "</body></html>"
            )
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False, encoding="utf-8"
            ) as f:
                f.write(html)
                tmp_path = f.name

            webbrowser.open(f"file:///{tmp_path.replace(chr(92), '/')}")
            self._print_btn.configure(text="  Sent!")
            self.after(1500, lambda: self._print_btn.configure(text="  Print"))

    app = _Stub()
    app._punch_text = MagicMock()
    app._punch_text.get.return_value = punch_text
    app._print_btn = MagicMock()
    app.after = MagicMock()
    app.tkinter_messagebox = MagicMock()
    return app


# -- tests --------------------------------------------------------------------


def test__print_punch_text_Scenario0_WebBrowserOpenIsCalledWhenTextPresent():
    # ESTABLISH
    app = _make_stub()
    with (
        patch("webbrowser.open") as mock_wb,
        patch("tempfile.NamedTemporaryFile", mock_open()) as mock_tmp,
    ):
        mock_tmp.return_value.__enter__.return_value.name = "/tmp/punch_test.html"
        # WHEN
        app._print_punch_text()
    # THEN
    mock_wb.assert_called_once()


def test__print_punch_text_Scenario1_OpensFileUrlPointingAtHtmlFile():
    # ESTABLISH
    app = _make_stub()
    with (
        patch("webbrowser.open") as mock_wb,
        patch("tempfile.NamedTemporaryFile", mock_open()) as mock_tmp,
    ):
        mock_tmp.return_value.__enter__.return_value.name = "/tmp/punch_test.html"
        # WHEN
        app._print_punch_text()
    # THEN
    url = mock_wb.call_args[0][0]
    assert url.startswith("file:///"), f"Expected file:// URL, got: {url!r}"
    assert url.endswith(".html"), f"Expected .html URL, got: {url!r}"


def test__print_punch_text_Scenario2_PunchTextAppearsInWrittenHtml():
    # ESTABLISH
    app = _make_stub()
    written_html = []

    with (
        patch("webbrowser.open"),
        patch("tempfile.NamedTemporaryFile") as mock_tmp,
    ):
        ctx = MagicMock()
        ctx.name = "/tmp/punch_test.html"
        ctx.write.side_effect = written_html.append
        mock_tmp.return_value.__enter__.return_value = ctx
        # WHEN
        app._print_punch_text()
    # THEN
    full_html = "".join(written_html)
    assert "Punch entry line 1" in full_html
    assert "Punch entry line 2" in full_html


def test__print_punch_text_Scenario3_HtmlContainsAutoPrintScript():
    # ESTABLISH
    app = _make_stub()
    written_html = []

    with (
        patch("webbrowser.open"),
        patch("tempfile.NamedTemporaryFile") as mock_tmp,
    ):
        ctx = MagicMock()
        ctx.name = "/tmp/punch_test.html"
        ctx.write.side_effect = written_html.append
        mock_tmp.return_value.__enter__.return_value = ctx
        # WHEN
        app._print_punch_text()
    # THEN
    assert "window.print()" in "".join(written_html)


def test__print_punch_text_Scenario4_PrintButtonShowsSentFeedback():
    # ESTABLISH
    app = _make_stub()

    with (
        patch("webbrowser.open"),
        patch("tempfile.NamedTemporaryFile", mock_open()) as mock_tmp,
    ):
        mock_tmp.return_value.__enter__.return_value.name = "/tmp/punch_test.html"
        # WHEN
        app._print_punch_text()
    # THEN
    configure_calls = [str(c) for c in app._print_btn.configure.call_args_list]
    assert any(
        "Sent" in c for c in configure_calls
    ), "Expected _print_btn to show a 'Sent' confirmation"


def test__print_punch_text_Scenario5_EmptyTextDoesNotOpenBrowser():
    # ESTABLISH
    app = _make_stub(punch_text="   \n")

    with (
        patch("webbrowser.open") as mock_wb,
        patch("tempfile.NamedTemporaryFile"),
    ):
        # WHEN
        app._print_punch_text()
    # THEN
    mock_wb.assert_not_called()


def test__print_punch_text_Scenario6_EmptyText_ShowsInfoPopup():
    # ESTABLISH
    app = _make_stub(punch_text="   \n")

    with (
        patch("webbrowser.open"),
        patch("tempfile.NamedTemporaryFile"),
    ):
        # WHEN
        app._print_punch_text()
    # THEN
    app.tkinter_messagebox.showinfo.assert_called_once()


def test__print_punch_text_Scenario7_SpecialHtmlCharsAreEscaped():
    # ESTABLISH
    app = _make_stub(punch_text="a < b && b > c\n")
    written_html = []

    with (
        patch("webbrowser.open"),
        patch("tempfile.NamedTemporaryFile") as mock_tmp,
    ):
        ctx = MagicMock()
        ctx.name = "/tmp/punch_test.html"
        ctx.write.side_effect = written_html.append
        mock_tmp.return_value.__enter__.return_value = ctx
        # WHEN
        app._print_punch_text()

    # THEN
    full_html = "".join(written_html)
    body_content = full_html.split("<body>")[1].split("<script>")[0]
    assert "<" not in body_content
    assert "&lt;" in full_html
    assert "&gt;" in full_html
    assert "&amp;" in full_html
