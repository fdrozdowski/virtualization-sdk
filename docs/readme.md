# Virtualization SDK Repository

This is the Markdown-based documentation for the Virtualization SDK.

## Local Testing
Create a `virtualenv` using Python 3 and run `pipenv run mkdocs serve`

```
$ virtualenv -p /usr/local/bin/python3 .
Running virtualenv with interpreter /usr/local/bin/python3
Using base prefix '/usr/local/Cellar/python/3.7.2_1/Frameworks/Python.framework/Versions/3.7'
New python executable in /Users/asarin/Documents/repos/virt-sdk-docs/env/bin/python3.7
Also creating executable in /Users/asarin/Documents/repos/virt-sdk-docs/env/bin/python
Installing setuptools, pip, wheel...
done.

$ source bin/activate

$ pipenv run mkdocs serve
INFO    -  Building documentation... 
INFO    -  Cleaning site directory 
[I 200424 15:54:06 server:292] Serving on http://127.0.0.1:8000
[I 200424 15:54:06 handlers:59] Start watching changes
[I 200424 15:54:06 handlers:61] Start detecting changes
```

The docs would be served up at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Debugging

#### mkdocs not found
```
$ pipenv run mkdocs serve
Error: the command mkdocs could not be found within PATH or Pipfile's [scripts].
```
Run `pipenv install` to make sure all the dependencies are installed from the Pipfile.

#### setuptools incompatibility
```
$ pipenv install
Installing dependencies from Pipfile.lock (65135d)…
An error occurred while installing markupsafe==1.0 --hash=sha256:a6be69091dac236ea9c6bc7d012beab42010fa914c459791d627dad4910eb665! Will try again.
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 14/14 — 00:00:10
Installing initially failed dependencies…
[pipenv.exceptions.InstallError]:   File "/usr/local/lib/python3.7/site-packages/pipenv/core.py", line 1874, in do_install
[pipenv.exceptions.InstallError]:       keep_outdated=keep_outdated
[pipenv.exceptions.InstallError]:   File "/usr/local/lib/python3.7/site-packages/pipenv/core.py", line 1253, in do_init
[pipenv.exceptions.InstallError]:       pypi_mirror=pypi_mirror,
[pipenv.exceptions.InstallError]:   File "/usr/local/lib/python3.7/site-packages/pipenv/core.py", line 859, in do_install_dependencies
[pipenv.exceptions.InstallError]:       retry_list, procs, failed_deps_queue, requirements_dir, **install_kwargs
[pipenv.exceptions.InstallError]:   File "/usr/local/lib/python3.7/site-packages/pipenv/core.py", line 763, in batch_install
[pipenv.exceptions.InstallError]:       _cleanup_procs(procs, not blocking, failed_deps_queue, retry=retry)
[pipenv.exceptions.InstallError]:   File "/usr/local/lib/python3.7/site-packages/pipenv/core.py", line 681, in _cleanup_procs
[pipenv.exceptions.InstallError]:       raise exceptions.InstallError(c.dep.name, extra=err_lines)
[pipenv.exceptions.InstallError]: ['Collecting markupsafe==1.0', '  Using cached MarkupSafe-1.0.tar.gz (14 kB)']
[pipenv.exceptions.InstallError]: ['ERROR: Command errored out with exit status 1:', '     command: /Users/asarin/Documents/repos/github/virtualization-sdk/docs/env/bin/python3.7 -c \'import sys, setuptools, tokenize; sys.argv[0] = \'"\'"\'/private/var/folders/fg/d4zl41bs6wv97zpzq9gckxsm0000gn/T/pip-install-txi66ppe/markupsafe/setup.py\'"\'"\'; __file__=\'"\'"\'/private/var/folders/fg/d4zl41bs6wv97zpzq9gckxsm0000gn/T/pip-install-txi66ppe/markupsafe/setup.py\'"\'"\';f=getattr(tokenize, \'"\'"\'open\'"\'"\', open)(__file__);code=f.read().replace(\'"\'"\'\\r\\n\'"\'"\', \'"\'"\'\\n\'"\'"\');f.close();exec(compile(code, __file__, \'"\'"\'exec\'"\'"\'))\' egg_info --egg-base /private/var/folders/fg/d4zl41bs6wv97zpzq9gckxsm0000gn/T/pip-pip-egg-info-cl5ykzbs', '         cwd: /private/var/folders/fg/d4zl41bs6wv97zpzq9gckxsm0000gn/T/pip-install-txi66ppe/markupsafe/', '    Complete output (5 lines):', '    Traceback (most recent call last):', '      File "<string>", line 1, in <module>', '      File "/private/var/folders/fg/d4zl41bs6wv97zpzq9gckxsm0000gn/T/pip-install-txi66ppe/markupsafe/setup.py", line 6, in <module>', '        from setuptools import setup, Extension, Feature', "    ImportError: cannot import name 'Feature' from 'setuptools' (/Users/asarin/Documents/repos/github/virtualization-sdk/docs/env/lib/python3.7/site-packages/setuptools/__init__.py)", '    ----------------------------------------', 'ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.']
ERROR: ERROR: Package installation failed...
```

Install `setuptools==45` to get around a deprecated API in version 46.

```
$ pip install setuptools==45
Collecting setuptools==45
  Downloading setuptools-45.0.0-py2.py3-none-any.whl (583 kB)
     |████████████████████████████████| 583 kB 2.7 MB/s 
Installing collected packages: setuptools
  Attempting uninstall: setuptools
    Found existing installation: setuptools 46.1.3
    Uninstalling setuptools-46.1.3:
      Successfully uninstalled setuptools-46.1.3
Successfully installed setuptools-45.0.0
(env) ~/Documents/repos/github/virtualization-sdk/docs$ pipenv install
Installing dependencies from Pipfile.lock (65135d)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 14/14 — 00:00:03
```

## Live Testing and Reviews
The command `git docsdev-review` will handle publishing reviews, and putting your changes on a live docs server. For example, you can clone the `docsdev-server` image on DCOA, and then run `git docsdev-review -m <yourvm.dlpxdc.co>`. This will:

- Push your doc changes to your VM
- Give you a link to the docdev server so you can test your changes live in a browser
- Publish a review

## Workflow diagrams
We create workflow diagrams using a tool called `draw.io` which allows us to import/export diagrams in html format. If you want to add a diagram or edit an existing one, simply create or import the html file in `docs/References/html` into `draw.io` and make your desired changes. When you are done, select your diagram and export it as a png file. You can think of the html files as source code, and the png files as build artifacts. After this step, you will be prompted to crop what was selected. You'll want this box checked to trim the whitespace around the diagram. After the diagrams are exported, check in the updated html file to `docs/References/html` and png file to `docs/References/images`.
