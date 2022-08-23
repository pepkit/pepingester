import argparse
import os
import yaml
import pathlib


def build_argparser() -> argparse.ArgumentParser:
    """Build the cli arg parser"""
    parser = argparse.ArgumentParser(description="Upload directory of PEPs")
    parser.add_argument(
        "-d",
        "-db-url",
        dest="db_url",
        default=None,
        type=str,
        help="Database connection string.",
    )
    parser.add_argument(
        "--username",
        dest="username",
        default="postgres",
        type=str,
        help="Username for postgresql instance",
    )
    parser.add_argument(
        "--password",
        dest="password",
        type=str,
        default="docker",
        help="Password for postgresql instance",
    )
    parser.add_argument(
        "-o", "--port", dest="port", default="5432", help="Port for postgresql instance"
    )
    parser.add_argument(
        "-s",
        "--hostname",
        dest="hostname",
        default="localhost",
        help="Hostname of postgresql instance",
    )
    parser.add_argument(
        "-b", "--database", dest="dbname", default="pep-base-sql", help="Database name"
    )
    parser.add_argument("-n", "--namespace", dest="namespace", required=True)
    parser.add_argument("-p", "--project", dest="project", required=True)
    parser.add_argument("-t", "--tag", dest="tag")
    parser.add_argument("pep", type=str, help="Path to PEP or GEO accession")
    return parser


def build_connection_string(args: argparse.Namespace) -> str:
    """Build a connection string using the cli args"""
    return f"postgresql://{args.user}:{args.password}@{args.hostname}:{args.port}/{args.name}"


def extract_project_file_name(path_to_proj: str) -> str:
    """
    Take a given path to a PEP/project inside a namespace and
    return the name of the PEP configuration file. The process
    is completed in the following steps:
        1. Look for a .pep.yaml file
            if exists -> check for config_file attribute
            else step two
        2. Look for project_config.yaml
            if exists -> return path
            else step 3
        3. If no .pep.yaml file with config_file attribute exists AND
        no porject_config.yaml file exists, then return None.

    :param str path_to_proj - path to the project
    """
    try:
        with open(f"{path_to_proj}/.pep.yaml", "r") as stream:
            _pephub_yaml = yaml.safe_load(stream)

        # check for config_file attribute
        if "config_file" in _pephub_yaml:
            # check that the config file exists
            if not os.path.exists(f"{path_to_proj}/{_pephub_yaml['config_file']}"):
                print(
                    f"Specified pep config file '{_pephub_yaml['config_file']}'\
                    not found in directory, '{path_to_proj}'. This pep will be unloadable by pephub. "
                )
        return _pephub_yaml["config_file"]

    # catch no .pep.yaml exists
    except FileNotFoundError:
        if not os.path.exists(f"{path_to_proj}/project_config.yaml"):
            print(
                f"No project config file found for {path_to_proj}.\
                This project will not be accessible by pephub. "
            )
        return "project_config.yaml"


def detect_input_type(pep_input: str) -> str:
    """
    The pipeline requires an input: either a path to a PEP
    or a GEO accession. This function attempts to determine
    which one it was.
    """
    path = pathlib.Path(pep_input)
    if path.exists():
        return "path"
    else:
        return "geo"
