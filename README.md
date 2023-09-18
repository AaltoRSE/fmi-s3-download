# fmi-s3-downloader

Script to download a list of urls from FMI S3 using a Python script.

The script utilizes boto3 and multhreading.

## Install

### Clone source code

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


## Expected problems

The script does not work with non-public data as it uses anonymous download requests. See [here]() how to add the AWS credentials.

The script does not specify [region]() which will most likely result in problems with other urls.

