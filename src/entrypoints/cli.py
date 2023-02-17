import argparse
import sys
from dotenv import load_dotenv
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent))
load_dotenv(str(Path(__file__).parent.parent.parent) + "/.env")


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    from src.adapters.data.sql import SQLUnitOfWorkManager
    from src.services.operating_systems import AddOperatingSystemHandler
    from settings import Settings

    session_factory = sessionmaker(bind=Settings.database_engine)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Possible options', dest="command")

    parser_add_img = subparsers.add_parser('add_img', help='Allows to add Golden image')
    parser_add_img.add_argument("--system_name", type=str, help="Name for new golden Image")
    parser_add_img.add_argument('--system_src', type=str, help='Source directory for system files')

    parser_add_img.add_argument('--boot_src', type=str, help="Source directory for boot files.")

    args = parser.parse_args()

    if args.command == "add_img":
        db_manager = SQLUnitOfWorkManager(session_factory)
        handler = AddOperatingSystemHandler(db_manager)
        handler.handle(args.system_name, args.system_src, args.boot_src)
