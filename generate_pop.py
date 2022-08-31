import pathlib
import os
import argparse
from typing import IO

from tqdm import tqdm

from utils import (
    extract_project_file_name,
    is_valid_namespace,
    is_valid_project,
    write_pop_cfg,
)

PEP_VERSION = "2.0.0"
DELIM = ","
HEADER_COLS = ["sample_name", "namespace", "project_name", "type", "location"]


def build_argparser():
    parser = argparse.ArgumentParser(
        description="Generate a POP (a PEP of PEPs) given a directory."
    )
    parser.add_argument("-o", "--out", type=str, default=".", help="path to POP output")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        dest="config_file_name",
        default="pop.yaml",
        help="name of POP configuration file",
    )
    parser.add_argument(
        "-s",
        "--samples",
        type=str,
        dest="samples_file_name",
        default="peps.csv",
        help="name of sample table file",
    )
    parser.add_argument(
        "-p",
        "--peps",
        type=str,
        dest="path_to_peps",
        help="Path to a folder/repository of PEPs",
    )
    parser.add_argument(
        "-g",
        "--geo",
        type=str,
        dest="path_to_geo",
        help="Path to a file that contains geo accession ids",
    )
    return parser


def parse_pep_dir(path_to_peps: str, fh: IO):
    """Parse a given directory of PEPs"""
    # traverse directory
    for name in tqdm(os.listdir(path_to_peps), desc="Analyzing repository", leave=True):
        # build a path to the namespace
        path_to_namespace = f"{path_to_peps}/{name}"

        if is_valid_namespace(path_to_namespace):
            # traverse projects
            for proj in tqdm(
                os.listdir(path_to_namespace), desc=f"Analyzing {name}", leave=True
            ):
                # build path to project
                path_to_proj = f"{path_to_namespace}/{proj}"

                if is_valid_project(path_to_proj):
                    # build cfg file
                    cfg_file = (
                        f"{path_to_proj}/{extract_project_file_name(path_to_proj)}"
                    )

                    sample_table_row = DELIM.join(
                        [f"{name}-{proj}", name, proj, "path", cfg_file]
                    )
                    fh.write(sample_table_row + "\n")


def parse_geo_list(path_to_geo: str, fh: IO):
    """Parse a list of geo accession IDs given a path to a list of them"""
    with open(path_to_geo) as geo_f:
        accession_ids = geo_f.read().splitlines()

    for accession in accession_ids:
        sample_table_row = DELIM.join(
            [f"geo-{accession}", "geo", accession, "geo", accession]
        )
        fh.write(sample_table_row + "\n")


def generate_pop(
    path_to_peps: str = None,
    path_to_geo: str = None,
    cfg_name: str = "pop.yaml",
    sample_table_path: str = "peps.csv",
):
    """
    Given a directory of PEPs in the namespace/project format, generate one unifying PEP of PEPs (POP)
    to be used as input to looper for indexing.
    """
    if all([path_to_peps is None, path_to_geo is None]):
        raise ValueError(
            "A path to peps **or** path to a file with geo accession ids must be supplied"
        )

    # check path to peps exists
    if path_to_peps and not os.path.exists(path_to_peps):
        raise FileNotFoundError(f"Path to PEPs does not exist: '{path_to_peps}'")

    # check path to geo exists
    if path_to_geo and not os.path.exists(path_to_geo):
        raise FileNotFoundError(
            f"Path to geo accesion list does not exist: '{path_to_geo}'"
        )

    # create a path to cfg if necessary
    if not os.path.exists(cfg_name):
        filepath = pathlib.Path(cfg_name)
        filepath.parent.mkdir(parents=True, exist_ok=True)

    # create a path to the sample table if necessary
    if not os.path.exists(sample_table_path):
        filepath = pathlib.Path(sample_table_path)
        filepath.parent.mkdir(parents=True, exist_ok=True)

    # init the cfg file
    write_pop_cfg(cfg_name, sample_table_path)

    with open(sample_table_path, "w") as fh:
        # write the csv header
        fh.write(DELIM.join(HEADER_COLS) + "\n")

        # if a path to peps was supplied, parase it
        if path_to_peps:
            print("Parsing peps")
            parse_pep_dir(path_to_peps, fh)

        if path_to_geo:
            print("Parsing geo accessions")
            parse_geo_list(path_to_geo, fh)


def main():
    parser = build_argparser()
    args = parser.parse_args()

    if not os.path.exists(args.out):
        filepath = pathlib.Path(args.out)
        filepath.parent.mkdir(exist_ok=True)

    cfg_file_name = f"{args.out}/{args.config_file_name}"
    samples_file_name = f"{args.out}/{args.samples_file_name}"

    generate_pop(args.path_to_peps, args.path_to_geo, cfg_file_name, samples_file_name)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye.")
