"""
2. Automated Backup Solution:
Write a script to automate the backup of a specified directory to a remote server or a cloud storage solution. 
The script should provide a report on the success or failure of the backup operation.
"""
import os
import tarfile
import boto3
import time
import argparse
from botocore.exceptions import NoCredentialsError, ClientError


def log_message(message, log_file):
    """
    Log a message to the log file and print it to the console.

    Args:
        message (str): The message to log.
        log_file (str): Path to the log file.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")


def create_backup(source_dir, backup_path):
    """
    Create a tar.gz archive of the specified directory.

    Args:
        source_dir (str): The directory to back up.
        backup_path (str): The path where the backup archive will be saved.
    """
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    log_message(f"Backup created at {backup_path}", backup_path)


def upload_to_s3(
    file_path, bucket_name, object_name, aws_access_key, aws_secret_key, log_file
):
    """
    Upload the backup file to an S3 bucket.

    Args:
        file_path (str): The path of the file to upload.
        bucket_name (str): The name of the S3 bucket.
        object_name (str): The name of the object in the S3 bucket.
        aws_access_key (str): AWS access key.
        aws_secret_key (str): AWS secret key.
        log_file (str): Path to the log file.
    """
    s3_client = boto3.client(
        "s3", aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        log_message(
            f"Backup successfully uploaded to S3 bucket '{bucket_name}' as '{object_name}'",
            log_file,
        )
        return True
    except FileNotFoundError:
        log_message(f"Error: The file {file_path} was not found.", log_file)
        return False
    except NoCredentialsError:
        log_message("Error: AWS credentials not available.", log_file)
        return False
    except ClientError as e:
        log_message(f"Error: {e}", log_file)
        return False


def main(source_dir, s3_bucket, aws_access_key, aws_secret_key, log_file):
    """
    Create a backup of the specified directory and upload it to an S3 bucket.

    Args:
        source_dir (str): The directory to back up.
        s3_bucket (str): The name of the S3 bucket.
        aws_access_key (str): AWS access key.
        aws_secret_key (str): AWS secret key.
        log_file (str): Path to the log file.
    """
    backup_name = f"backup-{time.strftime('%Y-%m-%d_%H-%M-%S')}.tar.gz"
    backup_path = f"/tmp/{backup_name}"

    log_message("Starting backup operation...", log_file)

    create_backup(source_dir, backup_path)

    success = upload_to_s3(
        backup_path, s3_bucket, backup_name, aws_access_key, aws_secret_key, log_file
    )

    if success:
        os.remove(backup_path)
        log_message(f"Local backup file {backup_path} removed.", log_file)
    else:
        log_message(
            f"Failed to upload backup to S3. Local backup file {backup_path} retained.",
            log_file,
        )

    log_message("Backup operation completed.", log_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory Backup to S3 Script")
    parser.add_argument("source_dir", help="The directory to back up")
    parser.add_argument("s3_bucket", help="The name of the S3 bucket")
    parser.add_argument("aws_access_key", help="AWS access key")
    parser.add_argument("aws_secret_key", help="AWS secret key")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    main(
        args.source_dir,
        args.s3_bucket,
        args.aws_access_key,
        args.aws_secret_key,
        args.log_file,
    )
