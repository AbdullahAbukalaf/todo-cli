from setuptools import setup

setup(
    name="todo-cli",
    version="1.0.0",
    py_modules=["todo", "storage", "task"],
    entry_points={
        "console_scripts": [
            "todo=todo:main",
        ],
    },
)
