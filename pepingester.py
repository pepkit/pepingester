import sys
import peppy
from pepdbagent import Connection
from pepdbagent.const import DEFAULT_TAG
from geofetch import Geofetcher
from const import INPUT_TYPES
from utils import build_argparser, detect_input_type


def main():
    # build and parse args
    parser = build_argparser()
    args = parser.parse_args()

    # init pep agent
    pagent = Connection(
        host=args.hostname,
        port=args.port,
        database=args.dbname,
        user=args.username,
        password=args.password,
    )

    # init geofetcher
    geofetcher = Geofetcher(processed=True, data_source="all")

    # get PEP input type
    input_type = args.type or detect_input_type(args.pep)

    if input_type not in INPUT_TYPES:
        raise ValueError(
            f"Input type couldnt be detected. Please ensure a valid path to a PEP or GEO accession was supplied."
        )

    if input_type == "path":
        p = peppy.Project(args.pep)
        p.name = args.project_name
        pagent.upload_project(
            p,
            namespace=args.namespace,
            name=args.project_name,
            tag=(args.tag or DEFAULT_TAG),
        )
        return 0

    if input_type == "geo":
        # here I will use the geofetch.Geofetcher object to create a
        # peppy.Project object from an accession id and then
        # upload it to the database
        projects = geofetcher.get_project(args.pep)
        for d_type, project in projects.items():
            tag = d_type.replace("_", "")
            print(f"PROJECT_NAME: {args.project_name}")
            if project: # verify that there was no error (False) or the datatype existed (not None)
                project.name = args.project_name
                pagent.upload_project(
                    project,
                    namespace=args.namespace,
                    name=args.project_name,
                    tag=tag,
                )
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Canceling pipeline.")
        sys.exit(1)
