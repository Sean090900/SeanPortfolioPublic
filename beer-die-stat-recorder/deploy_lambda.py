import os
import zipfile
from datetime import datetime

# configure file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
APP_DIR_NAME = 'src'
APP_DIR = os.path.join(BASE_DIR, APP_DIR_NAME)
ARCHIVE_DIR = os.path.join(BASE_DIR, 'archive')
FUNCTION_NAME = 'twilio-lambda-API' 

def main():

    # create a temporary directory
    print('Creating temporary storage... ', end='')
    temp_dir = create_dir('TEMP')
    print('DONE!')

    # copy all source code to the temporary directory
    print('Copying source files to temporary storage... ', end='')
    temp_app_dir = copy_app(APP_DIR, temp_dir)
    print('DONE!')

    # set permissions on the copied files per aws documentation
    print('Setting file permissions for AWS deployment... ', end='')
    set_aws_permissions(temp_app_dir)
    print('DONE!')

    # zip the copied files into an aws lambda deployment package
    print('Creating deployment package... ', end='')
    zip_path = zip_lambda_app(temp_dir)
    print('DONE!')

    # deploy lambda function
    print('Deploying Lambda function to AWS... ', end='')
    deploy_lambda(zip_path)
    print('DONE!')

    # empty and remove the temporary directory that was created
    print('Cleaning up temporary files... ', end='')
    purge_directory(temp_dir)
    os.rmdir(temp_dir)
    print('DONE!')


def create_dir(dir_name):
    """
    Creates a new directory with the specified name.
    Args:
        dir_name (str): the name of the directory to be created.
    Returns:
        dir_path (str): the absolute path to the newly created directory.
    """

    # construct absolue path to the new directory
    dir_path = os.path.join(BASE_DIR, dir_name)

    # create the new directory
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # ensure new directory is empty
    purge_directory(dir_path)

    # success
    return(dir_path)


def copy_app(from_dir, to_dir):
    """
    Recursively copies the a specified directory to another specified directory.
    Args:
        from_dir (str): the absolute path of the directory to be copied.
        to_dir (str): the absolute path of the destination directory.
    Returns:
        new_app_dir (str): the path the directory copy that was created.
    """

    # construct app directory path for the new copy
    new_app_dir = os.path.join(to_dir, APP_DIR_NAME)

    # recursively copy target directory to destination directory
    os.system('cp -r {} {}'.format(from_dir, new_app_dir))

    # success
    return(new_app_dir)


def set_aws_permissions(dir_path):
    """
    Given a directory, recursively sets all file permissions for AWS Lambda functions.
    Read more: https://docs.aws.amazon.com/lambda/latest/dg/deployment-package-v2.html
    Args:
        dir_path (str): the absolute path to the directory to be modified recursively.
    Returns:
        None
    """

    # change file permissions recursively for files and directories
    os.system('chmod 644 $(find {} -type f)'.format(dir_path))
    os.system('chmod 755 $(find {} -type d)'.format(dir_path))


def zip_lambda_app(temp_dir):
    """
    Creates a deployment package (.zip archive) of the entire /lambda_app/ directory contents.
    Args:
        temp_dir (str): the absolute path to the temporary directory where the app has been copied.
    Returns:
        zip_path (str): the absolute path of the newly created deployment package (.zip archive).
    """

    # construct timestamped file name for the new deployment package (.zip archive)
    zip_name = '{}_{}.zip'.format(FUNCTION_NAME, get_timestamp())

    # construct absolute file paths
    app_dir = os.path.join(temp_dir, 'src')
    zip_path = os.path.join(temp_dir, zip_name)

    # create deployment package (.zip archive)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(app_dir):
            for file in files:

                # construct file paths
                abs_file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(abs_file_path, app_dir)

                # add this file to the zip archive
                zip_file.write(abs_file_path, rel_file_path)

    # success
    return(zip_path)


def deploy_lambda(zip_path):
    """
    Deploy lambda function deployment package to AWS.
    Args:
        zip_path (str): absolute path to the deployment package (.zip archive) to be deployed.
    Returns:
        None
    """

    # ensure archive directory exists
    if not os.path.exists(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)

    # create an archive directory for this deployment
    deployment_dir = os.path.join(ARCHIVE_DIR, get_timestamp())
    if not os.path.exists(deployment_dir):
        os.mkdir(deployment_dir)
    purge_directory(deployment_dir)

    # copy deployment package to archive directory
    os.system('cp {} {}'.format(zip_path, deployment_dir))

    # construct aws cli lambda function deploy command
    deploy_cmd_data = {
        'function_name': FUNCTION_NAME,
        'zip_path': zip_path,
        'metadata_path': os.path.join(deployment_dir, 'deployment_metadata.txt')
    }
    deploy_cmd = 'aws lambda update-function-code'
    deploy_cmd += ' --function-name %(function_name)s'
    deploy_cmd += ' --zip-file fileb://%(zip_path)s'
    deploy_cmd += ' --output json > %(metadata_path)s'
    deploy_cmd = deploy_cmd % deploy_cmd_data

    # deploy lambda function to aws
    os.system(deploy_cmd)


def purge_directory(dir_path):
    """
    Completely empties the specified directory.
    Args:
        dir_path (str): the absolute path of the directory to be emptied.
    Returns:
        None
    """

    # empty the specified directory of all files and sub-directories
    os.system('rm -rf {}/*'.format(dir_path))


def get_timestamp():
    """
    Returns the current time as a string formatted for use in file naming.
    Args:
        None
    Returns:
        current_timestamp (str): Current time in YYYY-MM-DD_HHMMSS format.
    """

    # get the current time and format as a string
    current_timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')

    # success
    return(current_timestamp)


if __name__ == '__main__':
    main()
