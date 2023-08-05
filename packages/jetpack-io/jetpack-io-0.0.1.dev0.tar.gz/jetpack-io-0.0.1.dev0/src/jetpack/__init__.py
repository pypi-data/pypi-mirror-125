#__version__ gets set in the build/publish process (publish_with_credentials.sh)
__version__ = ""

from jetpack._job.interface import job
from jetpack._remote.interface import remote
from jetpack.cli import handle as init
from jetpack.cmd import root
from jetpack.redis import redis


def run() -> None:
    root.cli()
