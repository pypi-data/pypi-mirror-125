<p align="center">
  <a href="https://github.com/kunal-bhar/probplotlib"><img alt="probplotlib" src="https://i.ibb.co/tCHqmCN/probplotlib-logo-bg.png" width="55%"></a>
  <p align="center">Probability Distributions for Python</p>
</p>

![GitHub](https://img.shields.io/github/license/kunal-bhar/probplotlib)

### The Statistical Void

Stats can get tricky in the transition from plotting fun graphs to advanced algebraic
equations. A classic example is the given sum:

```
1.0e14 + 1.0 - 1.0e14
```

The actual result is `1.0` but in double precision, this will result in `0.0`.
While in this example the failure is quite obvious, it can get a lot trickier 
than that. Instances like these hinder the community from exploring the 
inferential potential of complex entities.

```python
p=Gaussian(a,b)
q=Gaussian(x,y)
p+q
```
This snippet would be close to useless as python addition doesn't isn't attributed for
higher-level declarables such as Gaussian variables. probplotlib provides simple solutions 
for probability distributions; posing a highly-optimized alternative to `numpy` and `math`,
in a niche that is scarce in options.


### Usage

probplotlib has the following operative methods:

- ` + `: uses [Dunder Methods](https://docs.python.org/3/reference/datamodel.html#special-method-names) for facilitating dist-additions.


- `calculate_mean()`: returns the mean of a distribution.

```python
gaussianex = Gaussian()
calculate_mean(gaussianx)
```

- `calculate_stdev()`: returns the standard deviation of a distribution.

```python
binomialex = Binomial()
calculate_stdev(binomialex)
```

- `read_dataset()`: reads an external .txt dataset directly as a distribution.

```python
gaussianex.read_dataset('values.txt')
binomialex.read_dataset('values.txt')
```

- `params()`: retrieves the identity parameters of an imported dataset.

```python
gaussianex.params()
binomialex.params()
```

- `pdf()`: returns the probability density function at a given point.

```python
pdf(gaussianex, 2)
```


functions unique to *Gaussian Distributions*:

- `plot_histogram()`: uses matplotlib to display a histogram of the Gaussian Distribution.

```python
gaussianex.plot_histogram()
```

- `plot_histogram_pdf()`: uses matplotlib to display a co-relative plot along with the Gaussian probability density function.

```python
gaussianex.plot_histogram_pdf()
```



functions unique to *Binomial Distributions*:

- `plot_bar()`: uses matplotlib to display a bar graph of the Binomial Distribution.

```python
binomialex.plot_bar()
```

- `plot_bar_pdf()`: uses matplotlib to display a co-relative plot along with the Binomial probability density function.

```python
binomialex.plot_bar_pdf()
```

###  Data Visualization

probplotlib therefore allows you to analyze raw numerical data graphically in minimial
lines of code. The example below makes for better understanding.

![TXT file](https://i.ibb.co/cyx1xKy/probplotlib-numtxt.png)

a bag of numbers in a `.txt` file corresponds to the following plots:

*histogram plot:*

![Histogram Plot](https://i.ibb.co/hWyNvrY/probplotlib-hist.png)

*bar plot:*

![Bar Plot](https://i.ibb.co/Rv8VCzG/probplotlib-bar.png)

*histogram plot with pdf:*

![Histogram Plot With PDF](https://i.ibb.co/wc34xy6/probplotlib-histpdf.png)


### References

[Stanford Archives: CS109- The Normal(Gaussian) Distribution](https://web.stanford.edu/class/archive/cs/cs109/cs109.1216/lectures/10_normal_gaussian.pdf)

[A Practical Overview on Probability Distributions: Andrea Viti, Alberto Terzi, Luca Bertolaccini](https://dx.doi.org/10.3978%2Fj.issn.2072-1439.2015.01.37)

[Awesome Scientific Computing: Nico Schlömer, GitHub Repository](https://github.com/nschloe/awesome-scientific-computing)

[math.statistics: Python 3.10 Source Code](https://github.com/python/cpython/blob/3.10/Lib/statistics.py)

[Stack Overflow](https://stackoverflow.com/)


### Dependencies

probplotlib depends on the `matplotlib`  library on top of your regular python installation. 

```
pip install matplotlib
```
or
```
conda install matplotlib
```

### Installation

probplotlib is available on the [Python Package Index](https://pypi.org/project/probplotlib/). You can install it directly using pip.

```
pip install probplotlib
```

### Testing

To run the tests, simply check to this directory and run the code below.

```
python -m unittest test_probplotlib
```











