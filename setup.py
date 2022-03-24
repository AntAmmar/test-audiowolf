from setuptools import setup, find_packages

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
    name='audiowolf-pipeline-manager',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='midhat',
    author_email='midhat.sibonjic@antcolony.io',
    packages=find_packages(),
    url='',
    description='',
    long_description=long_description,
    include_package_data=True,
    keywords='',
    zip_safe=False,
    license='',
    platforms=['any'],
    install_requires=[
        'django==3.2.12',
        'celery',
        'django-celery-results',
        'django-celery-beat',
        'boto3',
        'requests',
        'django-storages',
        'pyacrcloud @ git+https://github.com/acrcloud/acrcloud_sdk_python',
        'ffmpeg-python==0.2.0',
        'openpyxl==3.0.9',
        'pytube==12.0.0',
        'selenium==4.1.0',
        'webdriver-manager==3.5.2',
        'torch==1.11.0',
        'torchlibrosa==0.0.9',
        'numpy==1.21',

        'djangorestframework==3.13.1',
        'drf-yasg==1.20.0',
        'djangorestframework-camel-case==1.3.0',
        'django-environ==0.8.1',
    ],
)
