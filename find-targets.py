import argparse
import json

from pathlib import Path


def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description="Generate a targets import file for batch imports, to be run in the repository to be imported"
    )
    parser.add_argument(
        "--project-files",
        help="what is the filename you use for projects (pom.xml)",
        required=True,
        nargs="+",
    )
    parser.add_argument(
        "--template",
        help="file to use as a targets template, default: target-template.json",
    )
    parser.add_argument(
        "--output",
        help="path to save templated targets file, default: templated-import-targets.json",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="The folder containing the files to search (usually the reponame",
    )
    parser.add_argument(
        "--ignore", nargs="+", help="which folder names (not paths) should we exclude"
    )
    parser.add_argument(
        "--compact",
        dest="oneliner",
        action="store_true",
        help="Save target file as compact as possible (enforced regardless for target with more than 10 files)",
    )
    parser.add_argument(
        "--print",
        dest="no_save",
        action="store_true",
        help="Pretty print target content, overrides the compact/saving options",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command_line_args()
    project_files: list = args.project_files
    ignore: list = args.ignore or list()
    oneline: bool = args.oneliner or False
    no_save: bool = args.no_save or False
    target: str = args.target or ""
    template_file: str = args.template or "target-template.json"
    output_file: str = args.output or "templated-import-targets.json"

    template_contents = Path(template_file)
    output_contents = Path(output_file)

    output = {}
    targets = []

    template = json.loads(template_contents.read_text())

    the_target = template["targets"][0]

    repo = Path(f"{target}")

    # include .git directories
    ignores = ignore + [".git"]

    projects = []

    for filename in project_files:
        for proj in repo.rglob(f"*{filename}"):
            rpath = proj.relative_to(repo)
            folders = str(rpath).split("/")
            if not any(item in ignores for item in folders):
                a_proj = {}
                a_proj["path"] = str(rpath)
                projects.append(a_proj)

    a_target = the_target

    a_target["files"] = projects
    targets.append(a_target)

    output["targets"] = targets

    if oneline is True or len(projects) > 10 and no_save is False:
        json_output = json.dumps(output, separators=(",", ":"))
    else:
        json_output = json.dumps(output, indent=2)

    if no_save:
        print(
            f"Found: {len(projects)} projects that aren't on paths containing: {ignores}"
        )

        print(json_output)

    else:
        with output_contents.open("w", encoding="utf-8") as f:
            f.write(json_output)

        print(f"Total of {len(projects)} possible projects saved to {output_contents}")
