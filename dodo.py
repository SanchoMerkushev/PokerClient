"""Tasks for doit."""


def task_html():
    """Return html documentation."""
    return {
        "actions": [
            "sphinx-apidoc -o docs/ src",
            "sphinx-build -M html docs build"
        ],
    }


def task_wheel():
    """Build client wheel."""
    return {
        'actions': ['python -m build -n -w'],
        'task_dep': ['intern'],
    }


def task_client():
    """Run client."""
    return {
        'actions': ['python -m src.client -n %(name)s'],
        'params': [{'name': 'name',
                    'short': 'n',
                    'default': '',
                    'help': "Choose name for PokerClient"}],
        'task_dep': ['intern'],
    }


def task_server():
    """Run server."""
    return {
        'actions': ['python -m src.server -t local'],
        'task_dep': ['intern'],
    }


def task_lint():
    """Run linter."""
    return {
        'actions': ['flake8']
    }


def task_tests():
    """Run tests."""
    return {
        "actions": [
            "python -m unittest tests/test_* -v",
        ],
        'task_dep': ['lint'],
    }


def task_intern():
    """Gen internationalization."""
    return {
        "actions": [
            "pybabel compile -D msg -l ru_RU.UTF-8 -d po -i po/ru_RU.UTF-8/LC_MESSAGES/msg.po"],
    }
