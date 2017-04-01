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
```

## Usage
* Usage

    `python lehu.py --help`

* Pull Files
	* Usage
	
	    `python lehu.py pull --help`

	* Do everything in default (from `data.json`).
	
	    `python lehu.py pull`

	* Load data from specified file.
	
	    `python lehu.py pull --data <filename>`

	* Don't ignore existing files.
	
	    `python lehu.py pull -f`

* Push Files
	* Usage
	
	    `python lehu.py push --help`

	* Just upload a file.
	
	    `python lehu.py push --code <upload_code> --path <file_path> --name <file_name>`


## Hint
* Press `Ctrl + C` to cancel current download job.


## TODO
- [x] Download files
- [ ] Search shared files with author or keywords
- [x] Upload file
- [x] Friendly commands
- [x] Template for `data.json`
- [ ] Display progress of upload action


## Demo
![demo](https://github.com/Lodour/Lehu-Disk-Shortcut/raw/master/demo.jpeg)
