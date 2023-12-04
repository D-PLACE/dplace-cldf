from setuptools import setup


setup(
    name='cldfbench_dplace',
    py_modules=['cldfbench_dplace'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'dplace-dataset-ea=cldfbench_dplace:Dataset',
        ]
    },
    install_requires=[
        'cldfzenodo>=2.1.0',
        'commonnexus>=1.9.1',
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
