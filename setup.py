from setuptools import setup

setup(
    name='ctman',
    version="0.1",
    author='Mario Balibrera',
    author_email='mario.balibrera@gmail.com',
    license='MIT License',
    description='Manual generation plugin for cantools (ct)',
    long_description='Manual generation framework.',
    packages=[
        'ctman'
    ],
    zip_safe = False,
    install_requires = [
        "condox >= 0.1.1"
    ],
    entry_points = '''''',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
