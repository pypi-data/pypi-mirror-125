from setuptools import setup, find_packages

setup(
        name='passbolt',
        version='1.01',
        description='Passbolt python module',
        author='Daniel Lynch',
        author_email='daniel.lynch2016@gmail.com',
        url='https://djlynch.us',
        license='MIT',
        # package_dir=["src"],
        packages=find_packages(),
        install_requires=["requests", "python-gnupg", "argparse"],
        data_files=[]
    )
