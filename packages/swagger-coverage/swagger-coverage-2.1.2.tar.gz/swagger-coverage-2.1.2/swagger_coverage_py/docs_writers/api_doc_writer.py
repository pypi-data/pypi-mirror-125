import json

from swagger_coverage_py.configs import API_DOCS_TYPE


def write_api_doc_to_file(file_path: str, api_doc_data: dict):
    if API_DOCS_TYPE == "swagger" and not api_doc_data.get("swagger", None):
        api_doc_data["swagger"] = "2.0"

    with open(file_path, "w+") as file:
        file.write(json.dumps(api_doc_data))
