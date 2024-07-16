# Screw data loading 

This project aims to support loading screw driving data from json files by performing the necessary steps for data 
preprocessing and providing the data in a form suitable for further analysis (e.g. classification of the results).

The project is designed to be added as a local package for ease of development and usage across multiple scripts and 
projects.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)

## Installation

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Steps

1. **Clone the repository** to your local machine:
    ```bash
    git clone https://github.com/nikolaiwest/screw_data_loading.git

    cd yourproject
    ```

2. **Create a virtual environment** (optional but recommended):

    Either use venv: 
    ```bash
    python -m venv venv

    source venv/bin/activate  
    # On Windows, use `venv\Scripts\activate`
    ```

    Or use conda: 
    ```bash
    conda create --name yourenvname python=3.8

    conda activate yourenvname
    ```
3. **Install the package** in editable mode using `pip` (please note the `.`):
    ```bash
    pip install -e .
    ```


This command will install the project in editable mode, meaning any changes made to the source code will immediately reflect when the package is used.


## Usage

Once the package is installed, you can use it in your Python scripts as follows:

```python
import screw_data_loading as sdl 

# Example usage
x_train, x_test, y_train, y_test  = sdl.get_data(**sdl.DEFAULT_PARAMS)
```

### Project Structure

Here's a brief overview of the project structure:

```bash
yourproject/
│
├── data/       # Unpack and insert your json data here 
|
├── screw_data_loading/          
│   ├── connect/        # Build for live processing (not supported)
│   ├── json/       
│   ├── load/
│   ├── logs/
│   ├── prep/
│   ├── sqlite/         # Moved to a monitoring fork 
│   ├── __init__.py
│   ├── config.py
│   └── get_data.py
│
├── tests/      # Unit tests
│   ├── __init__.py
│   ├── test_equidistancing.py
│   ├── test_get_data.py
│   ├── test_padding.py
│   ├── test_splitting.py
│   └── test_truncating.py
│
├── README.md             # Project documentation
├── setup.py              # Installation script
└── requirements.txt      # List of dependencies
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes.
4. Run tests to ensure everything is working.
5. Commit your changes:
    ```bash
    git commit -m "Description of the feature or fix"
    ```
6. Push to your branch:
    ```bash
    git push origin feature-name
    ```
7. Create a Pull Request on GitHub.


## License

This project is licensed under the MIT License. See the LICENSE file for details.