# Samples for using RevoScalePy and MicrosoftML packages
'revoscalepy' and 'microsoftml' are machine learning libraries provided by Microsoft. They contains many battled tested and high performance machine learning algorithms. 

This gallery will showcase how to use 'revoscalepy" and 'microsoftml' for predictive analytics. There are 2 samples in this gallery:
1. Wine quality prediction with revoscalepy functions (Notebook file" 'revoscalepy_wine_prediction.ipynb'; Python script: 'revoscalepy_wine_prediction.py')
2. Adult census analysis with microsoftml functions (Notebook file: 'microsoftml_adult_census.ipynb'; Python script: 'adult_census.py')

Please note, 'revoscalepy' and 'microsoftml' don't support Mac OS yet, therefore these samples won't work in Mac OS.

# Wine quality prediction sample using 'revoscalepy' package

Please 'pip install matplotlib' before try this sample, if it has not been installed.  

## QuickStart
Navigate to the "Notebooks", open `revoscalepy_wine_prediction.ipynb`, click **Start the Notebook Server** button, and execute the script to run through the sample.

## Quick CLI references
If you want to try exercising this sample from the command line, here are some things to try:

First, launch the Command Prompt or Powershell from the **File** menu.

Run in local Python environment.
```
$ az ml experiment submit -c local revoscalepy_wine_prediction.py
```

Run in a local Docker container.
Please ensure your Docker engine allows at least 4 GB or RAM in order for this sample to run in Docker.
```
$ az ml experiment submit -c docker-python revoscalepy_wine_prediction.py
```

Create `myvm` run configuration to point to a Docker container on a remote VM
```
$ az ml computetarget attach --name myvm --address <ip address or FQDN> --username <username> --password <pwd> --type remotedocker

# prepare the environment
$ az ml experiment prepare -c myvm
```

Run `revoscalepy_wine_prediction.py` script in a Docker container in a remote VM:
```
$ az ml experiment submit -c myvm revoscalepy_wine_prediction.py
```

# Adult census sample using 'microsoftml' package
'microsoftml' is not bundled with Workbench installer, to run this sample, please first install the package.
- For Windows: 'pip install https://rserverdistribution.azureedge.net/production/revoscalepy/9.2.1/wb/1033/d282048eb04046999211535f7368a0a4/windows/microsoftml-1.5.0-py3-none-any.whl'
- For Linux (used in Docker): 'pip install https://rserverdistribution.azureedge.net/production/revoscalepy/9.2.1/wb/1033/d282048eb04046999211535f7368a0a4/linux/microsoftml-1.5.0-py3-none-any.whl'

Please 'pip install matplotlib' before try this sample, if it has not been installed.  

## QuickStart
Navigate to the "Notebooks", open `microsoftml_adult_census.ipynb`, click **Start the Notebook Server** button, and execute the script to run through the sample.

## Quick CLI references
If you want to try exercising this sample from the command line, here are some things to try:

First, launch the Command Prompt or Powershell from the **File** menu.

Run in local Python environment.
```
$ az ml experiment submit -c local adult_census.py
```

Run in a local Docker container.
**This sample doesn't support running in local docker yet. The support will come soon**


Run in a Remove VM
Create `myvm` run configuration to point to a Docker container on a remote VM
```
$ az ml computetarget attach --name myvm --address <ip address or FQDN> --username <username> --password <pwd> --type remotedocker

# prepare the environment
$ az ml experiment prepare -c myvm
```

Run `adult_census.py` script in a Docker container in a remote VM:
```
$ az ml experiment submit -c myvm adult_census.py
```

For more information:
- [MicrosoftML package](https://docs.microsoft.com/en-us/sql/advanced-analytics/using-the-microsoftml-package)
- [RevoScalePy package](https://docs.microsoft.com/en-us/sql/advanced-analytics/python/what-is-revoscalepy)
