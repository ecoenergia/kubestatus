# Kubernetes Namespace Status Viewer

This Python script provides a continually updating display of the status of various Kubernetes objects within a specified namespace. The script uses `kubectl` to fetch data and displays it in a formatted table using the `rich` library.

## Features

- Display status of Pods, Services, Deployments, and Container Image Counts.
- Auto-refreshes every 5 seconds for real-time status updates.
- Option to specify a Kubernetes namespace or auto-select the namespace of the first pod.

## Requirements

- Python 3
- `kubectl` configured for access to a Kubernetes cluster
- `rich` library installed (install via `pip install rich`)

## Usage

1. **Running the Script:**
   - To specify a namespace: `python kube_status.py -n <your_namespace>`
   - To use the default namespace (the namespace of the first pod from the current context): `python kube_status.py`

2. **Stopping the Script:** Press `Ctrl+C` to exit the continuous update loop.

## Distribution

The package can be built and distributed using the provided `Makefile`. `setuptools`, `twine` and `wheel` should already be installed locally. The following commands are available:

- `make clean`: Clean up previous build artifacts.
- `make build`: Build the package into a distributable format.
- `make upload`: Upload the package to PyPI.
- `make dist`: Run the `clean` and `build` steps sequentially.
- `make all`: Clean, build, and upload the package to PyPI.

Before running `make upload`, ensure that you have registered an account on [PyPI](https://pypi.org/) and configured your `.pypirc` file with your credentials.

## Functions

- `get_kubectl_output`: Executes a kubectl command and returns its output.
- `get_default_namespace`: Determines the default namespace based on the first pod's namespace.
- `create_pods_table`: Creates a table displaying the status of Pods.
- `create_services_table`: Creates a table displaying the status of Services.
- `create_deployments_table`: Creates a table displaying the status of Deployments.
- `create_image_count_table`: Creates a table displaying the count of unique container images.
- `main`: The main loop of the script, updating and displaying status tables.

## License

This script is released under the MIT License.

