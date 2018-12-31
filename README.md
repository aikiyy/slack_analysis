# SLACK ANALYSIS
## Dependencies
```
$ cat requirements.txt
Package    Version   
---------- ----------
certifi    2018.11.29
chardet    3.0.4     
Click      7.0       
idna       2.8       
pip        18.1      
requests   2.21.0    
setuptools 40.6.3    
urllib3    1.24.1    
wheel      0.32.3    
```
## Usage
### Cloning the repository

### Set legacy SLACK API TOKEN
```
$ export SLACK_API_TOKEN=${your token}
```

### 1. Download Channel List
```
$ python download.py channel-list
```

### 2. Download User List
```
$ python download.py user-list
```

### 3. Download All Channel History
```
$ python download.py all-channel-hist
```
