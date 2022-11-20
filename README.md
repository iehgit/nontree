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
    <img src="https://raw.githubusercontent.com/iehgit/nontree/master/README.images/logo.png" alt="9&#x1F333;" width="78" height="78">
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
      <ul>
        <li><a href="#data-types">Data Types</a></li>
        <li><a href="#constructing-a-treemap">Constructing A TreeMap</a></li>
        <li><a href="#adding-data-points-to-a-treemap">Adding Data Points To A TreeMap</a></li>
        <li><a href="#collision-detection">Collision Detection</a></li>
      </ul>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#project-links">Project Links</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

![NonTree pyplot][product-screenshot]

This package implements quadtree-like data structures in the classes `NonTree`, `QuadTree` and `BiTree`.
More precisely speaking, **point-region (PR) quadtrees** and variants thereof are implemented.
It also provides the class `TreeMap` to map points from the tree to arbitrary payload data, with a dictionary-like interface.

A point-region quadtree is a recursive data structure to contain points that lie on a two dimensional surface.
It allows for efficient collision detection between the containend points and an area.
Thus it can answer the question "Which points are within that rectangular area?".

In comparision to looping over all points and comparing the location of each point with the rectangular boundaries,
a quadtree delivers the answer in _O_(log(n)) instead of _O_(n).

This implementation also provides methods for circular collision detection.

An exemplary application could be to test elements on a map of a 2D game, before rendering each frame, whether they are in the screen area and thus must be drawn,
or if the time of drawing them can be saved due to them not beeing in a visible area anyway.

For more information about quadtrees in general, see the [Wikipedia article](https://en.wikipedia.org/wiki/Quadtree).
Or more specifically the [paragraph](https://en.wikipedia.org/wiki/Quadtree#Point-region_(PR)_quadtree) about point region quadtrees.

A quadtree (4-tree) is split into 4 subtrees, if its bucket capacity is full and additional points are added. Thus, it's area gets split into 4 quadrants.
The points then are stored in the subtrees, until they are at capacity and get split as well.
That's the well known quadtree data structure.
This package also implements two unusual variants thereof: The non-tree (9-tree) and the alternating bi-tree (2-tree).

The quadtree splits each tree into 9 segments in a 3 by 3 grid.
Due to reduced nesting depth, the retrieval of colliding points can be faster on a densely populated surface.

The bitree splits each tree in only 2 segments, alternatingly horizontally or vertically.
This tends to result in a higher nesting depth. But at each level, only two instead of four or nine subtrees have to be considered.
Thus it can be faster on a very sparsely populated surface.

The class `TreeMap` internally contains a `NonTree` (the default) or a `QuadTree` or `BiTree`.
It maps the points of the tree to payload data. This allows the retrieval of objects that lie in the searched area.

If no payload data is needed, and only the bare points are of interest, the tree classes can be used directly.

Additionally, a module `visualize` exists, to plot a graph of the layout of a tree with the help of `matplotlib`.

<!-- GETTING STARTED -->
## Getting Started
Install the package, import a module, and call a function.

### Prerequisites
This is a package for python3 (>=3.10). Slightly older versions of python3 might work, but are entirely untested.

The package has no mandatory dependencies of other external packages, but it optionally can make use of the follwing, if present:
- [matplotlib](https://pypi.org/project/matplotlib/) to plot graphs of the tree layout, such as the one shown above.
It is used by the module `visualize`.
- [numba](https://pypi.org/project/numba/) to speed up (jit-compile) some of the calculations for circular collision detection.
It gets detected/used automatically, without need for configuration or passing options.

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

### Data Types
Points are defined as tuples in the shape of (x, y).  
Data points are defined as tuples in the shape of (point, data), i.e. ((x, y), data), with data beeing any arbitrary object.  
Rectangular areas are defined as tuples in the shape of (x, y, width, height), or anything that can be indexed in the same way.
This allows the use of [pygame.Rect](https://www.pygame.org/docs/ref/rect.html).  
Circular areas are defined as tuples in the shape of (x, y, radius).

### Constructing A TreeMap
A `TreeMap` can be constructed like this, with a rectangle as its first parameter to specify its surface:
```python
from nontree.TreeMap import TreeMap

tree_map = TreeMap((0, 0, 100, 100))
```

Per default, it contains a `NonTree`. To specify the tree type, you can use the keyword argument `mode`, like this:
```python
from nontree.TreeMap import TreeMap

tree_map_foo = TreeMap((0, 0, 100, 100), mode=9)  # NonTree
tree_map_bar = TreeMap((0, 0, 100, 100), mode=4)  # QuadTree
tree_map_baz = TreeMap((0, 0, 100, 100), mode=2)  # BiTree
```

### Adding Data Points To A TreeMap
To add multiple data points:
```python
from nontree.TreeMap import TreeMap

a_lot_of_datapoints = [((2, 3), 'dog'), ((17, 80), 'cat'), ((45, 13), 'fish'), ((99, 77), 'rat')]

tree_map = TreeMap((0, 0, 100, 100))
tree_map.add_datapoints(a_lot_of_datapoints)
```

To add a single data point, the dict-like interface is convenient:
```python
from nontree.TreeMap import TreeMap

tree_map = TreeMap((0, 0, 100, 100))
tree_map[(55, 89)] = 'goat'
```


### Collision Detection
To query the data within an rectangular area of the surface, you can use the method `get_rect`, which takes a rectangle as its parameter:
```python
from nontree.TreeMap import TreeMap

a_lot_of_datapoints = [((2, 3), 'dog'), ((17, 80), 'cat'), ((45, 13), 'fish'), ((99, 77), 'rat')]

tree_map = TreeMap((0, 0, 100, 100))
tree_map.add_datapoints(a_lot_of_datapoints)
tree_map[(55, 89)] = 'goat'

result = tree_map.get_rect((4, 4, 80, 80))
print(result)
```
Output of the above:
```
['fish', 'cat']
```

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
......................................
-------------------------------------------------------------------------------
Ran 38 tests in 0.308s

PASSED (successes=38)
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
