import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='uthibs',                   # How you named your package folder (MyLib)
    packages=['uthibs'],             # Chose the same as "name"
    version='0.0.3',                 # Start with a small number and increase it with every change you make
    author='Thibaud Lamothe',        # Type in your name
    author_email='hello@etomal.com', # Type in your E-Mail
    license='MIT',                   # https://help.github.com/articles/licensing-a-repository
    description='Re-usable functions from my different projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ThibaudLamothe/uthibs',
    download_url='https://github.com/ThibaudLamothe/uthibs/archive/refs/tags/v.0.0.1.tar.gz',
    keywords=['FUNCTIONS', 'UTILS', 'GENERIC'],
    install_requires=[
        'chart_studio==1.1.0',
        'dash==2.0.0',
        'dash-core-components==2.0.0',
        'dash-html-components==2.0.0',
        'matplotlib==3.4.3',
        'numpy==1.21.3',
        'pandas==1.3.4',
        'Pillow==8.4.0',
        'plotly==5.3.1',
        'psycopg2-binary==2.9.1',
        'requests==2.26.0',
        'ruptures==1.1.5',
        'scikit-learn==1.0.1',
        'scipy==1.7.1',
        'seaborn==0.11.2',
        'slacker==0.14.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',              # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',              # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',       # Again, pick a license
        'Programming Language :: Python :: 3.7',        # Specify which pyhton versions that you want to support
    ],
)
