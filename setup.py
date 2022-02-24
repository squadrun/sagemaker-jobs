from setuptools import setup

install_requires = [
    'boto3==1.14.60', 'sagemaker==2.5.5'
]

setup(install_requires=install_requires, long_description_content_type='text/x-rst')

