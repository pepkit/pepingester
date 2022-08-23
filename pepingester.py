import sys
import peppy
from pepagent import PepAgent
from const import DEFAULT_TAG, INPUT_TYPES
from utils import build_argparser, detect_input_type

def main():
    # build and parse args
    parser = build_argparser()
    args = parser.parse_args()

    # init pep agent
    pagent = PepAgent(
        host=args.hostname,
        port=args.port,
        database=args.dbname,
        user=args.username,
        password=args.password,
    )

    input_type = detect_input_type(args.pep)

    if input_type not in INPUT_TYPES:
        raise ValueError(
            f"Input type couldnt be detected. Please ensure a valid path to a PEP or GEO accession was supplied."
        )

    if input_type == "path":
        p = peppy.Project(args.pep)
        pagent.upload_project(
            p, namespace=args.namespace, project=args.project, tag=(args.tag or DEFAULT_TAG)
        )
        return 0
    
    if input_type == "geo":
        # download geo
        return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Canceling pipeline.")
        sys.exit(1)