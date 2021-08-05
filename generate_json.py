import json
import pprint
from pathlib import Path

sensentive_info_keywords = ["auth", "user", "email", "address"]
pii_info_keywords = ["user", "email", "address"]
require_admin_keywords = ["admin", "manage", "delete"]
read_only_keywords = ["read", "info"]

EXCLUDED = [Path("api-list.json"), Path("out.json")]

result = list(Path(".").rglob("*.json"))

scopes_in_tagena_format = []
for json_api_desc_file_path in result:
    if json_api_desc_file_path in EXCLUDED:
        continue
    file_name = str(json_api_desc_file_path).split("/")[-1]
    with open(json_api_desc_file_path) as api_desc_file_descriptor:
        api_desc = json.load(api_desc_file_descriptor)
    api_auth_desc = api_desc.get("auth")
    if api_auth_desc:
        api_auth_scopes_desc = api_auth_desc.get("oauth2", {}).get("scopes", {})
        for scope_name, scope in api_auth_scopes_desc.items():
            scopes_in_tagena_format.append({
                "name": scope_name,
                "requiresAdminConsent": any([keyword in scope_name.split(".") for keyword in require_admin_keywords]),
                "tenantScope": True,
                "readOnly": any([keyword in scope_name for keyword in read_only_keywords]),
                "sensitiveData": any([keyword in scope_name for keyword in sensentive_info_keywords]),
                "pii": any([keyword in scope_name for keyword in pii_info_keywords]),
                "shortDescription": scope["description"],
                "longDescription": scope["description"],
                "vendor": "Google Workspace",
                "apis": [file_name]
            })

with open("out.json", "w") as f:
    f.write(json.dumps(scopes_in_tagena_format, indent=2))
