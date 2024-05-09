import json
import os
import sys
import yaml

payload = json.loads(os.getenv('PORT_PAYLOAD'))

trigger = payload['payload']['action']['trigger']
name = payload['payload']['properties'].get('name', None) or payload['payload']['entity'].get('identifier', None)
api_version = payload['payload']['properties']['apiVersion']
kind = payload['payload']['properties']['kind']
specificationWithoutNameKindApiVersion = {k:v for k,v in payload['payload']['properties'].items() if k not in ['name', 'namespace', 'kind', 'apiVersion']}
namespace = payload['payload']['properties'].get('namespace', None)

metadata = {"name": name}

if namespace:
    metadata['namespace'] = namespace

if len(sys.argv) < 2:
    print("Please provide delete flag")
    sys.exit(1)

should_delete = sys.argv[1].lower() == 'true'

if trigger == "CREATE":
    print(f"Creating resource with name {name}")
    with open(os.path.join(os.getenv('INPUTS_FOLDER'), f"{name}.yaml"), 'w') as f:
        yaml.dump({"metadata": metadata, "apiVersion": api_version, "kind": kind, "spec": specificationWithoutNameKindApiVersion}, f)

elif trigger == "DAY-2":
    print(f"Updating resource with name {name}")
    with open(os.path.join(os.getenv('INPUTS_FOLDER'), f"{name}.yaml"), 'w') as f:
        yaml.dump({"metadata": metadata, "apiVersion": api_version, "kind": kind, "spec": specificationWithoutNameKindApiVersion}, f)

elif trigger == "DELETE" and should_delete:
    print(f"Deleting resource with name {name}")
    if os.path.exists(os.path.join(os.getenv('INPUTS_FOLDER'), f"{name}.yaml")):
        os.remove(os.path.join(os.getenv('INPUTS_FOLDER'), f"{name}.yaml"))

elif trigger == "DELETE" and not should_delete:
    print(f"Deleting resource with name {name}")
    with open(os.path.join(os.getenv('INPUTS_FOLDER'), f"{name}.yaml"), 'w') as f:
        yaml.dump({"metadata": metadata, "apiVersion": api_version, "kind": kind, "spec": specificationWithoutNameKindApiVersion}, f)
