# DIM - Docker Image Monitor

Listen on docker events and register image usage time.

## Installation
```
sudo pip install dim
```
The installation will add the dim service to systemd, make sure you reload it.
```
systemctl daemon-reload
systemctl enable dim.service
systemctl start dim.service
```

## Usage

To display the images last start time run
```
dim-display
``` 
example output

```
+-----------------------------------------------------------------------------------+-------------------+
| Image                                                                             | Last Start Time   |
+===================================================================================+===================+
| fakes3:latest                                                                     | 7 hours ago       |
+-----------------------------------------------------------------------------------+-------------------+
| mariadb:10.1.19                                                                   | 7 hours ago       |
+-----------------------------------------------------------------------------------+-------------------+
| consul:0.9.2                                                                      | 7 hours ago       |
+-----------------------------------------------------------------------------------+-------------------+
| dynamodb:latest                                                                   | 7 hours ago       |
+-----------------------------------------------------------------------------------+-------------------+
| postgres:latest                                                                   | 2 days ago        |
+-----------------------------------------------------------------------------------+-------------------+
| mariadb:10.1.26                                                                   | 6 days ago        |
+-----------------------------------------------------------------------------------+-------------------+
| gotty:latest                                                                      | 11 days ago       |
+-----------------------------------------------------------------------------------+-------------------+
| rabbitmq:3.5.1-management                                                         | 18 days ago       |
+-----------------------------------------------------------------------------------+-------------------+
```

For more options run:
```
dim-display -h
``` 

```
usage: dim-display [-h] [-q] [-w WHITELIST] [-m MIN_AGE] [-r] [-s {age,image}]

Display Images Last Start Time.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           If set, returns only the image names
  -w WHITELIST, --whitelist WHITELIST
                        Images whitelist file
  -m MIN_AGE, --min-age MIN_AGE
                        Minimum image age in seconds
  -r, --reverse         If set images will be sorted by reversed order
  -s {age,image}, --sort-by {age,image}
                        If set images will be sorted by that attribute

```
