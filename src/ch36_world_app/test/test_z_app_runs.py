from ch36_world_app.w1_app import ETLApp
from os import environ as os_environ
from pytest import fail as pytest_fail


def test_ETLApp_ApplicationInitRunsWithoutError(tk_app):
    # sourcery skip: no-conditionals-in-tests
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
