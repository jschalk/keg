from ch30_etl_app.etl_gui_main import ETLApp


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
