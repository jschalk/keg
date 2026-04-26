from ch30_etl_app.etl_gui_main import ETLApp
from os import environ as os_environ
from pytest import mark as pytest_mark


@pytest_mark.skipif(
    not os_environ.get("DISPLAY"),
    reason="No display available for Tkinter",
)
def test_ETLApp_ApplicationInitRunsWithoutError():
    # ESTABLISH / WHEN
    root = ETLApp()
    # Schedule close almost immediately
    root.after(100, root.destroy)

    # THEN
    try:
        root.mainloop()
    except Exception as e:
        assert False, f"Tkinter app crashed: {e}"
