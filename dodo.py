"""Tasks for doit"""

def task_html():
    """Return html documentation."""
    return {
        "actions":[
            "sphinx-apidoc -o docs/ src",
            "sphinx-build -M html docs build"
        ]
    }

def task_client_wheel():
    """Build client wheel"""
    return {
       'actions': ['python -m build -n -w src'],
    }

def task_server_wheel():
    """Build server wheel"""
    return {
       'actions': ['python -m build -n -w src'],
    }

def task_tests():
    """Run tests."""
    return {
        "actions": [
            "python -m unittest tests/test_combinations.py -v",
            "python -m unittest tests/test_cards_to_str.py -v",
            "python -m unittest tests/test_Round_finish_round.py -v",
            "python -m unittest tests/test_Round_dealing_cards.py -v",
            "python -m unittest tests/test_Round_divide_win_balance.py -v",
        ]
    }

def task_int():
    """Gen internationalization"""
    return {
        "actions": ["pybabel compile -D msg -l ru_RU.UTF-8 -d po -i po/ru_RU.UTF-8/LC_MESSAGES/msg.po"]
    }
