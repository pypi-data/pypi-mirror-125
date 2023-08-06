from distutils.core import setup

setup(
    name='gcm_common',
    packages=['gcm_common'],
    version='0.1.9',
    license='MIT',
    description='GCM common package',
    author='Batkhishig Dulamsurankhor',
    author_email='batkhishign55@gmail.com',
    keywords=['gcm', 'common'],
    install_requires=[
        'flask',
        'PyYAML',
    ]
)
