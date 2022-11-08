<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iehgit/nontree">
    <img src="https://raw.githubusercontent.com/iehgit/nontree/master/README.images/logo.png" alt="9&#x1F333;" width="80" height="80">
  </a>

<h3 align="center">nontree</h3>

  <p align="center">
    A python package for n-tree 2D data structures similar to and including quadtree, with mapping to payload data
    <br />
    <a href="https://pydocs.sedf.de/nontree"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/iehgit/nontree/issues">Report Bug</a>
    ·
    <a href="https://github.com/iehgit/nontree/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#demo">Demo</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#project-links">Project Links</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![NonTree pyplot][product-screenshot]

TODO

<!-- GETTING STARTED -->
## Getting Started
Install the package, import a module, and call a function.

### Prerequisites
This is a package for python3 (>=3.10). Slightly older versions of python3 might work, but are entirely untested.

The package has no mandatory dependencies of other external packages, but it optionally can make use of the follwing, if present:
- [matplotlib](https://pypi.org/project/matplotlib/) to plot graphs of the tree layout, such as the one shown above.
It is used by the module `visualize`.
- [numba](https://pypi.org/project/numba/) to speed up (jit-compile) some of the calculations for circular collision detection.
It get's detected/used automatically, without need for configuration or passing options.

### Installation
You can get the raw files from the git repository:

```sh
git clone https://github.com/iehgit/nontree.git
```

It's easier to install the package with [pip](https://pypi.org/project/pip/):

```sh
pip install nontree
```

### Demo
To see that the package has been installed and is accessible, you could plot a demo graph, if you also have `matplotlib` available:

```pycon
>>> from nontree import visualize
>>> visualize.plot_demo()
>>>
```

Or you could simply construct a TreeMap, set a datapoint, and get back its data:

```pycon
>>> from nontree.TreeMap import TreeMap
>>> tree_map = TreeMap((0, 0, 100, 100))
>>> tree_map[(50, 50)] = 'Hello World!'
>>> tree_map[(50, 50)]
'Hello World!'
>>>
```

<!-- USAGE EXAMPLES -->
## Usage

TODO

_For more details, please refer to the [Documentation](https://pydocs.sedf.de/nontree)._

<!-- CONTRIBUTING -->
## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. Please make sure that all unit tests still pass after any changes.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

You can also simply open an issue with the tag "enhancement".

<!-- TESTING -->
## Testing
To run the unit tests:

```sh
cd tests
PYTHONPATH=../src python3 utest.py 
```

The output should look roughly similar to this:

```    
.................................
----------------------------------------------------------------------
Ran 33 tests in 0.319s

OK
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- PROJECT LINKS -->
## Project Links

[Github](https://github.com/iehgit/nontree/)

[PyPI](https://pypi.org/project/nontree/)

[API documentation](https://pydocs.sedf.de/nontree/)

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/iehgit/nontree.svg?style=for-the-badge
[contributors-url]: https://github.com/iehgit/nontree/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/iehgit/nontree.svg?style=for-the-badge
[forks-url]: https://github.com/iehgit/nontree/network/members
[stars-shield]: https://img.shields.io/github/stars/iehgit/nontree.svg?style=for-the-badge
[stars-url]: https://github.com/iehgit/nontree/stargazers
[issues-shield]: https://img.shields.io/github/issues/iehgit/nontree.svg?style=for-the-badge
[issues-url]: https://github.com/iehgit/nontree/issues
[license-shield]: https://img.shields.io/github/license/iehgit/nontree.svg?style=for-the-badge
[license-url]: https://github.com/iehgit/nontree/blob/master/LICENSE
[product-screenshot]: https://raw.githubusercontent.com/iehgit/nontree/master/README.images/myplot.png
