# fmi-s3-downloader

## Install

### Clone 

Clone this repository
```
git clone ZXXX
```

### Create conda environment

Install [conda] if not already installed.

Create and activate environment
```
conda env create -f env.yml -p env/
conda activate env/
```

## Example Run

Example run with
```
python3 src/main.py test-data/urls.116.txt
```

The script will download the 116 urls in `test_data/urls.116.txt` into the default output folder `data/` using the default number of threads 4.

Executing the command again will not download any new files as long as they already exist in the default output folder.

You can change the output folder using the option `--data_dir path-to-your-folder`.

The number of concurrent threads can be changed with `--workers number-of-workers`. Start from, e.g., the default 4 and double the amount until you see no improvement.


## Developing

Lint script using
```
black src && isort src
```
