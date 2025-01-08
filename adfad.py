import os
import yaml
from dotenv import load_dotenv
from lycheesh.eve.processor.prefect_processor import PrefectProcessor
from lycheesh.eve.parser import parse_yaml
import sys
from pathlib import Path
from lycheesh.eve.processor.prefect_server_utils import start_prefect_server, stop_prefect_server
import subprocess

load_dotenv()


class LycheeCLIInterface:
    """This is a helper class that wraps functions for agent classes to communicate with the user.
    In the first iteration, this will just be handled via print and input functions, but later
    once we integrate with a terminal, we will need to edit this class. When we convert Lychee to
    an API-based solution, much more of the code will have to be rewritten.
    """

    def __init__(self, lychee_path=None):
        if lychee_path is None:
            self.lychee_path = os.getcwd() + "/lychee/"
        else:
            self.lychee_path = lychee_path + "/lychee/"
    def lychee_file_exists(self) -> bool:
        """This function checks whether a lychee project has been initialized, and returns a bool
        based on the value determined. Initially, this will likely be done via os.path.exists

        POTENTIAL ISSUES:
            - may have issues with python's os and pwd, pwd for this function could differ from what we actually want

        ARGS:

        RETURNS:
            bool: whether a lychee project exists in the pwd
        """

        exists = os.path.exists(self.lychee_path)
        if os.getenv("debug_mode") == "true":
            print(f"Lychee file existence checked: {exists}")
        return exists

    def init_lychee(self):
        """This file initializes a lychee folder on the user's device in lychee_path. This is called by the
        PrimaryAgent.
        """
        if os.getenv("debug_mode") == "true":
            print(f"Creating lychee file")
        print("Here")
        os.mkdir(self.lychee_path)
        os.mkdir(self.lychee_path + "functions")
        os.mkdir(self.lychee_path + "pipelines")
        os.mkdir(self.lychee_path + "builds")

    def update_yaml(self, pipeline, content):
        if os.getenv("debug_mode") == "true":
            print(f"Yaml updated: {content}")
        with open(self.lychee_path + "pipelines/" + pipeline + ".yaml", "x") as f:
            f.write(content)

    def get_yaml(self, pipeline) -> str:
        """This function retrieves the yaml file representing the pipeline, stored in the
        .lychee directory of the lychee project file.

        This NEEDS to be updated depending on the file structure we actually end up deciding
        to use.
        This also might be broken because of python os things.
        """
        if os.getenv("debug_mode") == "true":
            print(f"Yaml read: {pipeline}")
        with open(self.lychee_path + "pipelines/" + pipeline + ".yaml", 'r') as file:
            content = file.read()

        return content

    def list_pipelines(self):
        """This function lists all the pipelines within the lychee file.

        Args:

        Returns:
            [str]: list of pipeline names (without the .yaml suffix)
        """
        if os.getenv("debug_mode") == "true":
            print("Pipelines listed")
        pipelines = [filename[:-5] for filename in os.listdir(self.lychee_path + "pipelines") if filename.endswith('.yaml')]
        if len(pipelines) == 0:
            return "No Pipelines Exist Yet"
        else:
            return pipelines
    def to_user(self, message: str) -> str:
        """This method sends a message to a user, and retrieves input they provide. This version
        simply uses python's built-in input function, and is for testing via the CLI MVP.

        ARGS:
            message (str)
        """

        response = input(message + "\n")
        return response

    def read_function(self, function) -> str:
        """This method reads code from a specified file, simply using read().

        ARGS:
            file (str): the name of the file to read from

        RETURNS:
            str: content of the file read
        """
        if os.getenv("debug_mode") == "true":
            print(f"Code Read at {function}")

        with open(self.lychee_path + "functions/" + function + ".py", "r") as f:
            # Read the entire content of the file
            content = f.read()
        return content

    def write_function(self, function, content):
        """This method writes code to a function file

        ARGS:
            function (str): the name of the function to write to
            content (str): the content to write to the function
        """
        if os.getenv("debug_mode") == "true":
            print(f"Code Written to {function}")
        with open(self.lychee_path + "functions/" + function + ".py", "w") as f:
            # Write the content to the file
            f.write(content)

    def list_functions(self):
        """Lists all the functions contained in the lychee folder.

        Args:

        Returns:
            [str]: all the function names (without the .py suffix)
        """
        if os.getenv("debug_mode") == "true":
            print("Functions listed")
        functions = [filename[:-3] for filename in os.listdir(self.lychee_path + "functions") if filename.endswith('.py')]

        if len(functions) == 0:
            return "No Functions Exist Yet"
        else:
            return functions

    def load_yaml(self, pipeline):
        return yaml.safe_load(self.get_yaml(pipeline))

    def write_build(self, pipeline: str, code: str):
        if os.getenv("debug_mode") == "true":
            print(f"{pipeline} build written")
        with open(self.lychee_path + "builds/" + pipeline + "_build.py", "w") as f:
            f.write(code)

    def run_build(self, pipeline: str):
        """ runs the pipeline_build.py
        TODO:
            call update requirement txt
            call download dependencies
            activate virtual environment
            command call :  (once venv is initialized)
                - prefect server start &
                - python3 pipeline_build.py

        Args:
            pipeline (str): Name of the pipeline to edit.

        Output:
            None: but prefect default logs and opens up server.

        """
        return "TODO"


    def install_requirements(self, *packages, **version_specs):
        """Installs dependencies from requirements.txt file.

        Installs dependencies based on provided arguments. If no arguments given,
        installs all dependencies from requirements.txt.

        Args:
            *packages: Variable number of package names to install
                (e.g., "numpy", "pandas")
            **version_specs: Keyword arguments for specific versions
                (e.g., python="3.1.1", numpy="1.21.0")

        Returns:
            bool: True if installation successful, False otherwise

        Examples:
            # Install all requirements
            install_requirements()

            # Install specific packages without version
            install_requirements("numpy", "pandas")

            # Install with specific versions
            install_requirements(python="3.1.1", numpy="1.21.0")

            # Mix of both
            install_requirements("requests", "urllib3", python="3.1.1")
        """
        try:
            if not packages and not version_specs:
                # Install all requirements from file
                # TODO: Add your full requirements installation logic here
                return True

            # Handle specific packages without version
            for package in packages:
                # TODO: Add logic to install package
                pass

            # Handle packages with specific versions
            for package, version in version_specs.items():
                # TODO: Add logic to install package with version
                pass

            return True
        except Exception as e:
            print(f"Error installing requirements: {e}")
            return False

    def requirements_update(self, *packages, **version_specs):
        """Updates requirements.txt file with current dependency versions.

        Updates package versions in requirements.txt based on provided arguments.
        If no arguments given, updates all package versions.

        Args:
            *packages: Variable number of package names to update
                (e.g., "numpy", "pandas")
            **version_specs: Keyword arguments for specific versions
                (e.g., python="3.1.1", numpy="1.21.0")

        Returns:
            bool: True if update successful, False otherwise

        Examples:
            # Update all requirements
            requirements_update()

            # Update specific packages
            requirements_update("numpy", "pandas")

            # Update with specific versions
            requirements_update(python="3.1.1", numpy="1.21.0")

            # Mix of both
            requirements_update("requests", "urllib3", python="3.1.1")
        """
        try:
            rtxt_loc = self.lychee_path + "builds/"

            if not packages and not version_specs:
                # Update all packages in requirements.txt
                # TODO: Add logic to update all package versions
                return True

            # Update specific packages without version
            for package in packages:
                # TODO: Add logic to update package in requirements.txt
                pass

            # Update packages with specific versions
            for package, version in version_specs.items():
                # TODO: Add logic to update package with version in requirements.txt
                pass

            return True
        except Exception as e:
            print(f"Error updating requirements: {e}")
            return False





if __name__ == "__main__":
    interface = LycheeCLIInterface()

    interface.run_build("text_extraction_pipeline")
