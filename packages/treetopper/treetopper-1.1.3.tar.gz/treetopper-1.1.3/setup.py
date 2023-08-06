import setuptools

keywords = ['forestry', 'natural resources', 'natural', 'resources',
            'forest', 'environmental', 'environmental science', 'science',
            'timber', 'tree', 'trees', 'west', 'coast', 'west coast', 'logging',
            'cruising', 'scaling', 'inventory', 'forests', 'board feet', 'cubic feet',
            'DBH', 'diameter at breast height', 'DIB', 'diameter inside bark', 'RD',
            'relative density', 'HDR', 'height to diameter ratio', 'species', 'VBAR',
            'volume to basal area ratio', 'BA', 'basal area', 'TPA', 'trees per acre',
            'scribner', 'timber marketing', 'forest marketing', 'timber management',
            'forest management']

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name = 'treetopper',
    version = "1.1.3",
    author = 'Zach Beebe',
    author_email = 'z.beebe@yahoo.com',
    description = 'Python module for calculating Timber data from tree species of the west coast',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/zacharybeebe/treetopper',
    license = 'MIT',
    packages = setuptools.find_packages(),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    keywords = keywords,
    python_requires = '>=3.6',
    py_modules = ['treetopper'],
    install_requires=[
        'fpdf >= 1.7.2',
        'openpyxl >= 3.0.6',
        'pyodbc >= 4.0.30',
        "pywin32 >=1.0 ; sys_platform == 'win32'"
    ],
    include_package_data = True,
)
