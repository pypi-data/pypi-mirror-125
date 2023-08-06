from setuptools import find_packages, setup

with open('README.md','r') as fh:
  long_description=fh.read()

setup(name='probplotlib',
      version='1.0',
      description='Probability Distributions for Python.',
      author='Kunal Bhargava',
      author_email='kunal21102@gmail.com',
      url='https://github.com/kunal-bhar/probplotlib',
      packages=find_packages("src"),  
      package_dir={"": "src"},   
      package_data={
       "": ["*.txt"]
       },
      license='MIT',      
      long_description=long_description,
      long_description_content_type='text/markdown',    
      zip_safe=False,
      classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Matplotlib',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='math mathematics python visualization plot',
      install_requires=['matplotlib'],     
      )
