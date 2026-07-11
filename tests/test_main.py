from nudl_py.main import main


def test_main_runs(capsys):
    main()
    captured = capsys.readouterr()
    assert "nudl-py" in captured.out