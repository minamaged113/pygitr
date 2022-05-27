# CONTRIBUTE

1. Clone the source code and then follow the next steps
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .
    ```
1. Write tests for the freature you wish to implement
1. Implement the feature logic
1. Execute the tests
    ```bash
    tox --recreate --parallel all
    ```
    * The test suite can run all tests for 3 python versions **3.7**, **3.8**, **3.9**]
    * The CI will run against the previous versions and **3.10**
    * If a specific version fails during local testing, you can run it specifically by adding the following flag to the `tox` command:
        ```bash
        -e pyXY # where XY is the failing build for python version. e.g. py38
        ```
1. If all goes well, commit and create a pull-request.
1. Please also check `-e static` for running tox to get all SCA findings.