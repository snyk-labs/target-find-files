# Find Targets Script

This is a simple script meant to search a local file system for possible project files to be imported into Snyk.

This works in conjunction with [snyk-api-import](https://github.com/snyk-tech-services/snyk-api-import). find-targets.py creates the file that snyk-api-import can than use to trigger an import and evaluation of those files via the Snyk API.

## Generating a target file with find-targets.py

- Checkout this repository
- Modify `target-template.json` to contain the details specific to your organizations settings for the integration you want to generate projects for, the provided template is for GitHub(+Enterpise), BitBucket Cloud, and Azure Repos. The integration ID and org ID values are in their settings pages.
- Checkout the target repository into this folder or just use the slice-import target that exists here already as a practice folder
- Run the command, specifying the target (the repo name) and the project files to be imported, use --print to just output to screen instead of saving a file:

```shell
> python3 find-targets.py --target slice-import --project-files requirements.txt --print
```

- In this example we found only one requirements.txt file, so the output to screen (or templated-import-targets.json) looks like this:

```json
{
  "targets": [
    {
      "target": {
        "fork": false,
        "name": "slice-import",
        "owner": "mrzarquon",
        "branch": "main"
      },
      "integrationId": "fe9e5717-f6fb-4308-aa25-adbd776e2852",
      "orgId": "1b48e2c4-6ca8-455f-a73f-d2f6f2a6b225",
      "files": [
        {
          "path": "very/deep/folder/requirements.txt"
        }
      ]
    }
  ]
}
```

- Adjust the command, you can add folder names (not paths) with `--ignore FOLDERA FOLDERB` to tune the files you think you should be importing
- Run the command without `--print` to save the file to the output file specified (the default is templated-import-targets.json)

## Importing Targets with snyk-api-import

- Download, unzip, and make executable the Snyk Api Import binary from the [releases page](https://github.com/snyk-tech-services/snyk-api-import/releases)
- Set a SNYK_TOKEN environment variable for an account that has import privileges for the repository in question (if you can perform the import in the UI, you can use your personal token found in your Settings page)
- Ensure you set a log directory for API import to store its logs
- Run the snyk-api-import command with the import directive along with the file to be imported:

```shell
> export SNYK_LOG_PATH="logs"
> mkdir -p $SNYK_LOG_PATH
> export SNYK_TOKEN=7668AA46-CEC6-440C-9269-F18504E05C24
> snyk-api-import import --file "templated-import-targets.json"
```

- Wait - depending on the number of files detected the import can take a while, snyk-api-import will update the screen with the status of the various attempts to import files
