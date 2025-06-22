[project]
name = "fotix"
version = "0.1.0"
description = "Fotix: Aplicativo de desktop para encontrar e gerenciar fotos e vídeos duplicados."
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "pydantic",
    "pytest",
    "pytest-cov",
]

[tool.pytest.ini_options]
# Adiciona o diretório 'src' ao PYTHONPATH para que o pytest encontre os módulos.
pythonpath = [
  "src"
]

[tool.pyright]
# Adiciona o diretório 'src' aos caminhos de análise do Pyright/Pylance.
# Isso resolve o erro 'reportMissingImports' no VS Code.
extraPaths = ["src"]

[tool.pylance]
# Configuração redundante para garantir compatibilidade com Pylance.
# A seção [tool.pyright] é geralmente suficiente.
extraPaths = ["src"]
