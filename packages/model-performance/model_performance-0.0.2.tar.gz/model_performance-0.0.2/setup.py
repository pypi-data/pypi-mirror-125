
VERSION = '0.0.2' 
DESCRIPTION = 'Model Analysis and Performance Package'

from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()


setup(

        name="model_performance", 
        version=VERSION,
        author="Mrinal Shankar",
        author_email="<mrinal.svp@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
		url = "https://github.com/mrinal-shankar/Model-Performance",
        packages=find_packages(),
        install_requires=['numpy', 'pandas'],
        
        keywords=['python', 'model performance'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

