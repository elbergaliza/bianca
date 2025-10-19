"""
Setup script para o pacote BIANCA
"""

from setuptools import setup, find_packages
import os

# Ler o README para usar como long_description


def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações"

# Ler requirements do requirements.txt


def read_requirements():
    requirements_path = os.path.join(
        os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'tiktoken>=0.11.0',
        'python-dotenv>=1.0.0',
        'openai>=1.0.0',
    ]


setup(
    name="bianca-ai",
    version="1.0.0",
    author="BIANCA Team",
    author_email="bianca@example.com",
    description="Biblioteca de Inteligência Artificial para Novos Componentes e Aplicações",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/bianca-ai",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/bianca-ai/issues",
        "Documentation": "https://github.com/your-username/bianca-ai/wiki",
        "Source Code": "https://github.com/your-username/bianca-ai",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "audio": [
            "speechrecognition>=3.10.0",
            "pyaudio>=0.2.11",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "speechrecognition>=3.10.0",
            "pyaudio>=0.2.11",
        ],
    },
    entry_points={
        "console_scripts": [
            "bianca-info=bianca:main",
        ],
    },
    include_package_data=True,
    package_data={
        "bianca": [
            "README.txt",
            "*.md",
        ],
    },
    keywords=[
        "ai",
        "artificial-intelligence",
        "openai",
        "gpt",
        "tokens",
        "cost-calculation",
        "machine-learning",
        "nlp",
        "natural-language-processing",
    ],
    zip_safe=False,
)

