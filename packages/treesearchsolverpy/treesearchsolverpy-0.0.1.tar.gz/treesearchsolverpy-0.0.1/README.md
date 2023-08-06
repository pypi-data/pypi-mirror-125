# Tree Search Solver (Python)

A solver based on heuristic tree search.

This is the Python version of [fontanf/treesearchsolver](https://github.com/fontanf/treesearchsolver).

![treesearch](img/treesearch.jpg?raw=true "treesearch")

[image source](https://commons.wikimedia.org/wiki/File:Saint-L%C3%A9ger-l%C3%A8s-Domart,arbre_de_la_croix_Notre-Dame_14.jpg)

## Description

The goal of this repository is to provide a simple framework to quickly implement algorithms based on heuristic tree search.

Solving a problem only requires a couple hundred lines of code (see examples).

Algorithms:
* Iterative Beam Search `iterative_beam_search`

## Examples

[Travelling Salesman Problem](examples/travellingsalesman.hpp)

## Usage, running examples from command line

```shell
python3 -m examples.travellingsalesman -a generator -i data/travellingsalesman/instance
python3 -m examples.travellingsalesman -a iterative_beam_search -i data/travellingsalesman/instance_50.json
```

## Usage, Python library

See examples.

