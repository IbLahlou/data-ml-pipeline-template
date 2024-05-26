from setuptools import setup, find_packages

setup(
    name="{{cookiecutter.project_slug}}",
    version="0.1.0",
    description="{{cookiecutter.project_description}}",
    author="{{cookiecutter.author_name}}",
    author_email="{{cookiecutter.email}}",
    python_requires=">={{cookiecutter.python_version}}",
    packages=find_packages(),
    install_requires=[
        "prefect",
        "bentoml",
        "mlflow",
        "numpy",
        "pandas",
        "matplotlib",
        "pyYAML",
        "tqdm",
        "types-PyYAML",
        "pytest",
        "unidecode",
        "scikit-learn",
    ],
)
