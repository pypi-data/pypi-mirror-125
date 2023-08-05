import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="owm-api-dftorres",
    version="0.0.1",
    author="Daniel Felipe Torres",
    author_email="dafetohe2@gmail.com",
    description="Obtener la información actual y la previsión del tiempo desde open weather map api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dftorres/mi_proyecto",
    project_urls={
        "Bug Tracker": "https://github.com/dftorres/mi_proyecto/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
