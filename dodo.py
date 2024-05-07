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
       'actions': ['python -m build -n -w src/client'],
    }

def task_server_wheel():
    """Build server wheel"""
    return {
       'actions': ['python -m build -n -w src/server'],
    }

def task_tests():
    """Run tests."""
    return {
        "actions": ["python -m unittest src.server.test_combinations -v"]
    }
