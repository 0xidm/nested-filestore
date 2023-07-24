from setuptools import setup

setup(
    version='0.1.0',
    name='Nested Filestore',
    description="Nested Filestore",
    packages=[
        'nested_filestore',
    ],
    scripts=[
        'bin/nested_manager.py'
    ],
    include_package_data=True,
    keywords='',
    author='0xidm',
    author_email='0xidm@protonmail.com',
    url='https://linktr.ee/0xidm',
    install_requires=[
        "python-dotenv",
        "click",
        "rich",
        "ratarmountcore[gzip]",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pdbpp",
            "mypy",
            "pylint",
            "ipython",
        ],
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
        ]
    },
    license='MIT',
    zip_safe=True,
)
