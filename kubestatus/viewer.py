import argparse
import json
import os
import subprocess
import time
from rich.console import Console
from rich.table import Table

import os

def clear_screen():
    """
    Clears the console screen. Performs more reliably than rich.console.clear()

    This function uses system-specific commands ('cls' for Windows, 'clear' for Unix/Linux)
    to clear the console screen. It's an alternative to the console.clear() method from the rich library,
    useful in environments where console.clear() might not function as expected.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_kubectl_output(command):
    """
    Executes a given kubectl command and returns the output.

    Args:
    command (str): The kubectl command to execute.

    Returns:
    str: The output of the command or an error message.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e}"

def get_default_namespace():
    """
    Gets the default Kubernetes namespace by querying the first pod's namespace.

    Returns:
    str: The default namespace or 'default' if an error occurs.
    """
    output = get_kubectl_output("kubectl get pods -o json")
    try:
        return json.loads(output)['items'][0]["metadata"]["namespace"]
    except (KeyError, IndexError, json.JSONDecodeError):
        return "default"

def create_pods_table(namespace):
    """
    Creates a table of the current status of pods in the specified namespace.

    Args:
    namespace (str): The Kubernetes namespace.

    Returns:
    Table: A table object from the rich library.
    """
    pods = get_kubectl_output(f"kubectl get pods -n {namespace}")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Ready")
    table.add_column("Status")
    table.add_column("Restarts")
    table.add_column("Age")

    for line in pods.splitlines()[1:]:
        table.add_row(*line.split())

    return table

def create_services_table(namespace):
    """
    Creates a table of the current status of services in the specified namespace.

    Args:
    namespace (str): The Kubernetes namespace.

    Returns:
    Table: A table object from the rich library.
    """
    services = get_kubectl_output(f"kubectl get services -n {namespace}")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Cluster-IP")
    table.add_column("External-IP")
    table.add_column("Ports")
    table.add_column("Age")

    for line in services.splitlines()[1:]:
        table.add_row(*line.split())

    return table

def create_deployments_table(namespace):
    """
    Creates a table of the current status of deployments in the specified namespace.

    Args:
    namespace (str): The Kubernetes namespace.

    Returns:
    Table: A table object from the rich library.
    """
    deployments = get_kubectl_output(f"kubectl get deployments -n {namespace}")
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Name")
    table.add_column("Ready")
    table.add_column("Up-to-date")
    table.add_column("Available")
    table.add_column("Age")

    for line in deployments.splitlines()[1:]:
        table.add_row(*line.split())

    return table

def create_image_count_table(namespace):
    """
    Creates a table showing the count of unique container images in the specified namespace.

    Args:
    namespace (str): The Kubernetes namespace.

    Returns:
    Table: A table object from the rich library.
    """
    command = f"kubectl get pods -n {namespace} -o jsonpath='{{.items[*].status.containerStatuses[*].imageID}}' | tr -s '[[:space:]]' '\\n' | sort | uniq -c"
    output = get_kubectl_output(command)
    table = Table(show_header=True, header_style="bold yellow")
    table.add_column("Count")
    table.add_column("Image ID")

    for line in output.strip().split('\n'):
        count, image_id = line.strip().split(maxsplit=1)
        table.add_row(count, image_id)

    return table

def main():
    """
    Main function that continually updates and displays Kubernetes status tables.

    Args:
    namespace (str): The Kubernetes namespace to monitor.
    """
    parser = argparse.ArgumentParser(description="Display Kubernetes namespace status", allow_abbrev=False)
    parser.add_argument("--namespace", help="Specify the Kubernetes namespace", default="", type=str)
    parser.add_argument("--refresh", help="Number of seconds between screen refreshes", default=5, type=int)
    args = parser.parse_args()

    namespace = args.namespace if args.namespace else get_default_namespace()

    console = Console()

    while True:
        pods_table = create_pods_table(namespace)
        services_table = create_services_table(namespace)
        deployments_table = create_deployments_table(namespace)
        image_count_table = create_image_count_table(namespace)

        clear_screen()
        console.print("Pods Status:", style="bold green")
        console.print(pods_table)
        console.print("\nServices Status:", style="bold blue")
        console.print(services_table)
        console.print("\nDeployments Status:", style="bold magenta")
        console.print(deployments_table)
        console.print("\nContainer Image Counts:", style="bold yellow")
        console.print(image_count_table)

        time.sleep(args.refresh)

if __name__ == "__main__":
    main()