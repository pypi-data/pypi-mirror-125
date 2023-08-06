import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class post_install():
    def run(self):
        import nltk
        nltk.download('stopwords')
        nltk.download('wordnet')


setuptools.setup(
    name="cleantext-tn",
    version="0.0.1",
    author="Thu Nguyen",
    author_email="minhthu6521@gmail.com",
    description="Clean text package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minhthu6521/clean-text",
    project_urls={
        "Bug Tracker": "https://github.com/minhthu6521/clean-text/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    cmdclass={'install_data': post_install},
)