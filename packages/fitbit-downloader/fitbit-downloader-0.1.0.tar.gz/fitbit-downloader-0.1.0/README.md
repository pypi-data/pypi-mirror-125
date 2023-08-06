
[![](https://codecov.io/gh/nickderobertis/fitbit-downloader/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/fitbit-downloader)

#  fitbit-downloader

## Overview

A CLI and Python tool for downloading Fitbit data

## Getting Started

Install `fitbit-downloader`:

```
pip install fitbit-downloader
```

A simple example:

```python
import fitbit_downloader

# Do something with fitbit_downloader
```

## Links

See the
[documentation here.](
https://nickderobertis.github.io/fitbit-downloader/
)

## Development

Run all commands in `pipenv shell`.

### Download Sample Responses

Run `python -m fitbit_downloader.download_samples` to output JSON files 
with the responses.

### Generate Response Models

Run `python -m fitbit_downloader.gen_models` to output response models 
in `fitbit_downloader.models` from the sample responses.

## Author

Created by Nick DeRobertis. MIT License.