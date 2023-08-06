from setuptools import setup, find_packages

with open("README.md", "r") as f:
    ld = f.read()

with open("requirements.txt", "r") as f:
    rq = f.read().splitlines()

setup(
    name='trie_nathaniel',
    version='0.0.1',
    description='Calls commands to the trie server that can modify its state',
    python_requires='>=3.6',
    install_requires=rq,
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    author='Nathaniel Thomas',
    author_email='catchnate+pypi@gmail.com',
    py_modules=["triecli"],
    package_dir={"triecli": "triecli"},
    license='MIT',
    url='https://github.com/Nathaniel-github/TrieClient',
    long_description=ld,
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": [
            "triecli=trie_nathaniel:main",
        ]
    },
    dependency_links=[
        'https://pypi.org/project/inquirer/'
    ],

    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
    ]
)
