# cpu

This is a CPU simulator, it doesn't aim to emulate any particular CPU, although it does take some inspiration from the M68K design, it is principally aimed at students learning about computing and wanting to have a reasonably easy project to follow, both to write simple assembly programs and understand, in an abstract way, how a CPU might work.

There is a compiler that will compile a file into an intermediary format that the CPU can load.

```
poetry run python cpu/tools/compiler --file examples/6.bin --output examples/6.out
```

And to run a compiled example:

```
poetry run python cpu/main --load examples/6.out
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

Setting up a Flint project should be as simple as:

```
make env
```

## Running the tests

```
make tests
```

## Generating the documentation

```
make docs
```

## Authors

* Neil Munro (neilmunro@gmail.com)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

