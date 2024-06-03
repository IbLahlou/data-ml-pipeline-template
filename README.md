# Cookiecutter Template for Prefect, BentoML, and MLflow Projects

This repository contains a Cookiecutter template for setting up an end-to-end machine learning project using Prefect, BentoML, and MLflow. This template helps you quickly bootstrap a project with a predefined structure and necessary configurations.

## Project Structure

The generated project will have the following structure:

```plaintext
.
├── bentoml
│   ├── bentoml.yaml
│   ├── README.md
│   └── service.py
├── data
│   ├── test.csv
│   └── train.csv
├── deployment
│   └── services
│       ├── latest_model_service.yaml
│       └── previous_model_service.yaml
├── main.py
├── README.md
├── requirements.txt
├── res
│   └── trails.ipynb
├── setup.py
└── tasks
    ├── a_start_mlflow_server.py
    ├── b_load_data.py
    ├── c_data_preprocessing.py
    ├── d_data_split.py
    ├── e_train_model.py
    ├── f_evaluate_model.py
    ├── g_save_model.py
    ├── __init__.py
    └── __pycache__
        └── __init__.cpython-39.pyc
```

## How to Use

To generate a new project using this template, follow these steps:

1. **Install Cookiecutter**:
    ```bash
    pip install cookiecutter
    ```

2. **Generate a new project**:
    ```bash
    cookiecutter https://github.com/IbLahlou/MLOPS-template-PBR.git
    ```

3. **Navigate to the generated project directory**:
    ```bash
    cd MLOPS-template-PBR
    ```

4. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Template Configuration

When you run Cookiecutter, you will be prompted to enter the following information to configure your new project:

- `project_name`: The name of your project.
- `project_slug`: The directory name for your project.
- `project_description`: A short description of your project.
- `author_name`: Your name.
- `email`: Your email address.
- `github_username`: Your GitHub username.
- `python_version`: The Python version to use.
- `use_streamlit`: Whether to include Streamlit support (`yes` or `no`).
- `ml_framework`: The machine learning framework to use (`tensorflow`, `torch`, `sklearn`, or `other`).

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter): A command-line utility that creates projects from project templates.
- [Prefect](https://www.prefect.io/): A modern workflow orchestration tool.
- [BentoML](https://www.bentoml.com/): A flexible, high-performance model serving framework.
- [MLflow](https://mlflow.org/): An open-source platform for managing the end-to-end machine learning lifecycle.
