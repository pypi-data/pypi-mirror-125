# colorsplash-common

## Description

colorsplash-common (CSC) is a component of the overarching ColorSplash web application that can be found at https://thurau.io/colorsplash/. ColorSplash allows users to browse royalty free images that have colors within a certain Euclidean distance of a provided HEX code. CSC is a python library hosted on PyPi to allow common features to be included as dependencies within the other python componenets.

You can see other components of this project in the following Github repos
- [ColorSplashPhotoRetrieval](https://github.com/DanielThurau/ColorSplashPhotoRetrieval)
- [ColorSplashPhotoProcessor](https://github.com/DanielThurau/ColorSplashPhotoProcessor)
- [ColorSplashColorDetector](https://github.com/DanielThurau/ColorSplashColorDetector)
- [thurau.io](https://github.com/DanielThurau/thurau.io)

## Motivation

A friend was facing issues when trying to create social media posts for an ecommerce company we recently launched. She had developed a branding guide and had chosen what colors she wanted to include in the website, logos, and eventual marketing material. But when it was time to make marketing posts, trying to apply that style guide was difficult. For all the tools on the internet she used, none were able to query royalty free images that were close to the HEX color codes she had selected. This project was born to remedy this issue.

I wanted to provide a clean minimal interface on a website that would have a form for a HEX code, and query a REST API that would return royalty free images that had a subset of colors within close to the original HEX code.

## Tech Used

CSC is a very simple python library that tightly couples integration with the various DynamoDB tables in the project. It uses boto3 as the client library.

## Installation

### Cloning The Project

You can either fork the repo or clone it directly with

```shell
$ git clone https://github.com/DanielThurau/colorsplash-common.git
$ cd colorsplash-common
```

### Developing

This project uses [poetry](https://python-poetry.org/) to build, test, and publish.

To install dependencies run

```shell
$ poetry install
```

To run the unit tests run

```shell
$ poetry run pytest
```


## Usage

CSC is hosted on PyPi so you can use any tool that integrates with PyPi to bring it in as a dependency. The easiest way is with pip. For example

```shell
$ pip install colorsplash-common
```

// TODO link a Github gist showing the use of the library

## Contribute

If you'd like to contribute, fork the project and submit a Pull Request.

## License

See LICENSE.md

> MIT License
>
> Copyright (c) 2021 Daniel Thurau