# Lehu Disk Shortcut
A shortcut for [Lehu-NetDisk](http://disk.lehu.shu.edu.cn/).
上海大学乐乎网盘助手。

## Install
```bash
$ git clone git@github.com:Lodour/Lehu-Disk-Shortcut.git
$ cd Lehu-Disk-Shortcut/
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
$ mv data.json.sample data.json
$ vim data.json
$ python lehu.py --help
```

## Usage
* Load data from specificied file.
`python lehu.py --data <filename>`

* Don't ignore existing files.
`python lehu.py -f`

## Hint
* Press `Ctrl + C` to cancel current download job.

## TODO
- [x] Download files
- [ ] Search shared files with author or keywords
- [ ] Upload file
- [x] Friendly commands
- [x] Template for `data.json`
