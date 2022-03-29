# Quickbase interview task solution

## Run instructions

In requirements.txt you can find described the needed dependencies to run and test the script.

First you will need to provide API tokens for Freshdesk and Github APIs by exporting the following environment variables:

```
export FRESHDESK_TOKEN=<your_token>
export GITHUB_TOKEN=<your_token>
```

Then run main.py and provide the Github user and Freshdesk subdomain as command line arguments:
```
python main.py --github-username=<usernmae> --freshdesk-subdomain=<subdomain>
```

## Test instructions
Add the src/ folder to the PYTHONPATH and then run the tests as follows:
```
python -m unittest tests/utils_test.py
python -m pytest tests/github_client_test.py
python -m pytest tests/freshdesk_client_test.py
```