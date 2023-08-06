# resemble.ai API

[resemble.ai](https://resemble.ai) is a state-of-the-art natural voice cloning and synthesis provider. Best of all, the platform is accessible by using our public API! Sign up [here](https://app.resemble.ai) to get an API token!

This repository hosts a Python library for convenient usage of the [Resemble API](https://docs.resemble.ai).


# Quick start

```python
from resemble import Resemble

Resemble.api_key('your_api_key')

project = Resemble.v2.projects.get('project_uuid')
voice = Resemble.v2.voices.get('voice_uuid')

clip = Resemble.v2.clip.create_sync('project_uuid', 'voice_uuid', 'This is a test')
```

# Development

The library files are located in `resemble/`

# Testing

Install nose (`pip install nose`), then run tests like so:

```bash
$ TEST_API_KEY=<...> TEST_BASE_URL=<...> nosetests
```

Note: To see `print()` output, add `--nocapture` like so: `nosetests --nocapture`

# Publishing new versions

1. `git status`: Make sure your working directory has no pending changes.
2. Update the version attribute in `setup.cfg`.
3. `git commit`: Commit this version change.
4. Remove previous builds: `rm -rf ./dist/`.
5. Build the package: `python3 -m build`.
6. (optional) Publish to the test index:
  ```sh
  python3 -m twine upload --repository testpypi dist/*
  ```
7. Publish to the index
  ```sh
  python3 -m twine upload dist/*
  ```
