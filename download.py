import argparse
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
from botocore import UNSIGNED
from botocore.client import Config


def parse_arguments():
    """Usage: scrape input_file --workers 4"""

    parser = argparse.ArgumentParser(prog="scrape", description="Scrape a list of urls")

    parser.add_argument("input_file", type=str)
    parser.add_argument("--download_dir", type=str, default="downloads")
    parser.add_argument("--log_file", type=str, default="logs/log.txt")
    parser.add_argument("--workers", type=int, default=4)

    return parser.parse_args()


def setup_logging(log_file, log_level="INFO"):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def load_urls(input_file):
    """Read urls from an input text file (one url per row)."""
    with open(input_file, "r") as fin:
        urls = [line.strip() for line in fin if line.strip()]

    logging.info(f".. Loaded {len(urls)} urls")

    return urls


def parse_url(url):
    """Parse an S3 URL into its bucket name and object key."""

    stripped_url = url.replace("s3://", "")
    # Split the URL at the first slash
    bucket_name, object_key = stripped_url.split("/", 1)

    return bucket_name, object_key


def download_single_url(url, download_dir):
    client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    bucket_name, object_key = parse_url(url)
    output_file = Path(download_dir) / Path(object_key.split("/")[-1])
    if output_file.is_file():
        logging.info(f".. Skipping, output file already exists: {output_file}")
        return
    # with open(output_file, "wb") as fout:
    #    client.download_fileobj(bucket_name, object_key, fout)
    client.download_file(bucket_name, object_key, output_file)
    logging.info(f".. Downloaded: {output_file}")


def download_multiple_urls(urls, download_dir, max_workers):
    Path(download_dir).mkdir(exist_ok=True, parents=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for url in urls:
            logging.info(f"URL: {url}")
            executor.submit(download_single_url, url, download_dir)


def main():
    args = parse_arguments()
    setup_logging(args.log_file)
    logging.info("Load urls")
    urls = load_urls(args.input_file)
    logging.info("Start downloading objects")
    t = time.time()
    download_multiple_urls(urls, args.download_dir, args.workers)
    logging.info(f"Finished. Consumed {time.time()-t:.3f} seconds.")


if __name__ == "__main__":
    main()
