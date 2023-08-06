# pygithubapi

python3 module to call github apis in command line or inside a module and export result into mysql and later Grafana.

[The source for this project is available here][src].

---

It's a python module that you can include in your python module or can be used in command line.

    python3 pygithubapi.py --help
    usage: pygithubapi.py [-h] [-V] [-U USER] [-t TOKEN] [-u URL] [-a API] [-m METHOD]
                        [-J JSONFILE]

    pygithubapi is a python3 program that call github apis in command line or imported as
    a module

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pygithubapi
    -U USER, --user USER  github user
    -t TOKEN, --token TOKEN
                            github token
    -u URL, --url URL     github url
    -a API, --api API     github api should start by a slash
    -m METHOD, --method METHOD
                            should contain one of the method to use : ['DELETE', 'GET',
                            'POST', 'PUT']
    -J JSONFILE, --jsonfile JSONFILE
                            json file needed for POST method

---

[packaging guide]: https://packaging.python.org
[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[src]: https://github.com/stormalf/pygithubapi
[rst]: http://docutils.sourceforge.net/rst.html
[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"
[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

# release notes

1.0.0 initial version

1.0.1 fixing issue with wrong json dependency

1.0.2 fixing issue with UnboundLocalError: local variable 'response' referenced before assignment

1.0.3 fixing issue with response.json()
