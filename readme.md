# Samples for using RevoScalePy and MicrosoftML packages

Please use Docker on DSVM to try these samples. 

First, create a DSVM compute target
```
$ az ml computecontext attach -n myvm -a <IPAddr> -u username -w password
```

Next, edit the _myvm.runconfig_ file under _aml_config_ folder and change Framework to Python:
```
...
"Framework": "Python"
...
```
Then, execute against Docker on the remove DSVM 
```
$ az ml execute start -c myvm  adult_census.py
```

Check run history details to see plotted ROC graph.
