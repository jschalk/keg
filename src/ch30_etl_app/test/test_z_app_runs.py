from ch30_etl_app.etl_gui_main import ETLApp
from os import environ as os_environ
from pytest import fail as pytest_fail


def test_ETLApp_ApplicationInitRunsWithoutError(tk_app):
    if tk_app:
        # ESTABLISH / WHEN
        root = ETLApp()
        # Schedule close almost immediately
        root.after(100, root.destroy)

        # THEN
        try:
            root.mainloop()
        except Exception as e:
            pytest_fail(f"Tkinter app crashed: {e}")
