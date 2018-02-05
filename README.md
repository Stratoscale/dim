# DIM - Docker Image Monitor

Listen on docker events and register image usage time.

## Installation
```
sudo pip install git+http://github.com/stratoscale/dim.git
```

## Usage

### Monitoring
The installation will add the dim service to systemd, make sure you reload it.

```
systemctl daemon-reload
systemctl start dim.service
``` 
### Display

To display the images last start time run
```
dim-display
``` 
example output

```
+-----------------------------+-------------------+
| Image                       | Last Start Time   |
+=============================+===================+
| dr-manager:last_build       | 5 minutes ago     |
+-----------------------------+-------------------+
| dr_melet-local:latest       | 6 minutes ago     |
+-----------------------------+-------------------+
| dr_nginx-remote:latest      | 6 minutes ago     |
+-----------------------------+-------------------+
| consul:latest               | 6 minutes ago     |
+-----------------------------+-------------------+
| dr_melet-remote:latest      | 6 minutes ago     |
+-----------------------------+-------------------+
| stratoscale/wiremock:latest | 6 minutes ago     |
+-----------------------------+-------------------+
| mariadb:10.1.26             | 6 minutes ago     |
+-----------------------------+-------------------+
| dr-build:latest             | 7 minutes ago     |
+-----------------------------+-------------------+
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
  -q, --quite           If set, returns only the image names
  -w WHITELIST, --whitelist WHITELIST
                        Images whitelist file
  -m MIN_AGE, --min-age MIN_AGE
                        Minimum image age in seconds
  -r, --reverse         If set images will be sorted by reversed order
  -s {age,image}, --sort-by {age,image}
                        If set images will be sorted by that attribute

```
