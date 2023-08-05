import argparse
from enum import Enum
from fakts import Fakts
from fakts.beacon.beacon import FaktsEndpoint
from fakts.grants.beacon import BeaconGrant
from fakts.grants.endpoint_grant import EndpointGrant
from fakts.grants.yaml import YamlGrant
from rich.console import Console
#importing the os module
import os

#to get the current working directory
directory = os.getcwd()


class ArkitektOptions(str, Enum):
    INIT = "init"
    DEV = "dev"


init_script = f"""
from arkitekt.agents.script import ScriptAgent

agent = ScriptAgent()

@agent.register()
def test_show(name: str)-> str:
    raise NotImplementedError("DD")

agent.provide()

"""






def main(script = ArkitektOptions.INIT, name=None, refresh=False):
    
    console = Console()

    if not name:
        name = console.input("What is [i]your[/i] Apps [bold red]name[/]? :smiley: ")



    if script == ArkitektOptions.INIT:
        fakts = Fakts(grants=[EndpointGrant(endpoint=FaktsEndpoint(url="http://localhost:3000/setupapp", name="test"))], name=name)#
        if not fakts.loaded or refresh:
            with console.status("Please check your browser window"):
                fakts.load()


        with open(os.path.join(directory, "run.py"), "w") as f:
            f.write(init_script)









    print(name)


def entrypoint():
    parser = argparse.ArgumentParser(description = 'Say hello')
    parser.add_argument('script', type=ArkitektOptions, help='The Script Type')
    parser.add_argument('--name', type=str, help='The Name of this script')
    parser.add_argument('--refresh', type=bool, help='Do you want to refresh')
    args = parser.parse_args()

    main(script=args.script, name=args.name, refresh=args.refresh)


if __name__ == "__main__":
    entrypoint()
