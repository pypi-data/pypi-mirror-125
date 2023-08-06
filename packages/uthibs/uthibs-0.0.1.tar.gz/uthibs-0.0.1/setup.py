import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='uthibs',                   # How you named your package folder (MyLib)
    packages=['uthibs'],             # Chose the same as "name"
    version='0.0.1',                 # Start with a small number and increase it with every change you make
    author='Thibaud Lamothe',        # Type in your name
    author_email='hello@etomal.com', # Type in your E-Mail
    license='MIT',                   # https://help.github.com/articles/licensing-a-repository
    description='Re-usable functions from my different projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/user/reponame',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[
        'datetime',
        'numpy',
        'pandas==0.24.0',
        'slacker',
        'sklearn',
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',              # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',              # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',       # Again, pick a license
        'Programming Language :: Python :: 3.7',        # Specify which pyhton versions that you want to support
    ],
)
