import sys
from unittest.mock import patch

from src.__version import version
from src.main import main


def test_version(capsys):
    with patch.object(sys, "argv", ["prog", "--version"]):
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == version

    with patch.object(sys, "argv", ["prog", "-V"]):
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == version
