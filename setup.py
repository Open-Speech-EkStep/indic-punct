from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="indic-punct",
    version='0.0.7',
    description='Punctuation and inverse text normalization for Indic languages and English',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Open-Speech-EkStep/indic-punct',
    keywords='nlp, punctuation, Indic languages, deep learning',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=[
        'wget',
        'certifi==2020.12.5',
        'inflect==5.3.0',
        'numpy==1.20.2',
        'pandas==1.2.4',
        'python-dateutil==2.8.1',
        'pytz==2021.1',
        'six==1.15.0',
        'tqdm==4.60.0',
        'torch==1.7.1',
        'scipy==1.5.4',
        'sentencepiece==0.1.94',
        'tokenizers==0.9.4',
        'torchvision==0.8.2',
        'transformers==4.0.1',
        'indic-nlp-library==0.81'
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
)
