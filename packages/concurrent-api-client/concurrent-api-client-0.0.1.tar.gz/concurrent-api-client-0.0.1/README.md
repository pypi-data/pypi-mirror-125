# Python API Client

An example for API client using python [request](https://docs.python-requests.org/) library. 

`tests` directory has an example to call an weather reporting API(https://weather.tsukumijima.net/), an API that returns Japanese weather prediction data reported by Meteorological Agency in Japan, compatible with deprecated livedoor API. 

---

## Usage (by running test)

### case1: run by python venv

```bash
$ cd concurrent-api-client
$ python -m venv venv
$ source venv/bin/activate
$ (venv) pytest -s # -s option returns standard output.
$ (venv) deactivate
$
```



### case2: run by tox with testing with multiple python versions

`tox.ini` has some python interpreters definition (e.g. py37, py38, py39)
You can setup multiple python versions by [`pyenv`](https://github.com/pyenv/pyenv). Install pyenv and setup python versions (e.g. `pyenv install 3.7.8 3.8.6 3.9.7`)
`

```bash
$ cd concurrent-api-client
$ pyenv local 3.7.8 3.8.6 3.9.7 # you need to setup multiple versions that are relevant with `envlist` in `tox.ini`
$ tox -r # -r option recreates virtual environment. Once you configure it, you can just run `tox` for later test. 
```

You can see output in `log/api_clint.log`

---

## Workflow with pip and pip-tools (on package update)

Please see [note](https://note.hommalab.io/posts/python/python-dependency-management/)