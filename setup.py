from setuptools import setup, find_packages

setup(
    name="analizador_datos",
    version="0.1.0",
    description="Aplicación de análisis de datos",
    author="Deyton Riascos Ortiz",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "flet==0.28.2",
        "flet-desktop==0.28.2",
        "flet-webview==0.28.2",
        "pandas>=2.2.2",
        "numpy>=1.26.4",
        "matplotlib>=3.8.4",
        "seaborn>=0.13.2",
        "duckdb>=0.10.0",
        "black>=24.0.0",
        "flake8>=7.0.0",
        "isort>=5.13.0",
        "pytest>=8.1.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
