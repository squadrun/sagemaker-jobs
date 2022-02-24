====================
SageMaker Jobs
====================

Contains Abstracted SageMaker methods that are used to create SageMaker Training Jobs.


Methods
#########

get_sagemaker_client
**********************
Returns a boto3 sagemaker client.

- **region**:
    The AWS region for which the client should be created. Type is String.

    Default: ``us-east-1``


create_training_jobs
**********************

- **docker_image_arn (Required)**:
    ARN of the docker image stored in the Amazon ECR.

    Eg - ``123456789012.dkr.ecr.us-east-1.amazonaws.com/sagemaker-decision-trees:latest``

- **sagemaker_role (Required)**:
    ARN of the IAM role that SageMaker will assume when running the training job.

    Eg - ``arn:aws:iam::123456789012:role/SageMakerRole``

- **sagemaker_bucket (Required)**:
    S3 bucket where the training job artifacts will be stored.

    Eg - ``sagemaker_artifacts``


- **input_s3_data_path (Required)**:
    Location of the input data in the SageMaker S3 Bucket.

    Eg - If data is stored at ``sagemaker_artifacts/my_input_data_folder`` then use ``my_input_data_folder``

- output_s3_data_path:
    Location of the output data in the SageMaker S3 bucket's output folder.

    Be default this value is empty and hence
    SageMaker will create a folder based on the ECR repo name and timestamp
    like - ``sagemaker-decision-trees-2020-09-28-11-22-02-826``.

    In this case you will find model files inside
    this folder - ``sagemaker_bucket/output/sagemaker-decision-trees-2020-09-28-11-22-02-826``.

    If you give it some value like ``decision-trees`` then SageMaker will put model files inside this folder -
    ``sagemaker_bucket/output/decision-trees/sagemaker-decision-trees-2020-09-28-11-22-02-826``

    Default: Empty String.

- instance_type:
    Type of the EC2 instance that will be used for training.

    Default: ``ml.m5.4xlarge``

- volume_size:
    Size of the EBS volume in GBs. Type is integer.

    Default: ``30``.

- max_run:
    Timeout in seconds for training.
    After this amount of time Amazon SageMaker terminates the job regardless of its current status. Type is integer

    Default: ``86400``

- max_wait:
    Timeout in seconds waiting for spot training instances.

    After this amount of time Amazon SageMaker will stop waiting for Spot instances to become available.
    This must always be greater than max_run. Type is integer

    Default: ``86401``

- use_spot_instances:
    A boolean value that denotes whether to use EC2 spot instances for this training job. Type is boolean.

    Default: ``True``.

- region:
    The AWS region in which to create the training job. Type is String.

    Default: ``us-east-1``

- base_job_name:
    The Prefix of the training job name. Type is String.

    Default: Empty String.

- use_vpc:
    A boolean value that indicates whether to create training job within a VPC or not. Uses subnets and
    security groups passed in the params. If not specified defaults to False and training job will be created without VPC config.

    Default: ``False``

- subnets:
    List of subnet ids

    Default: ``['subnet-09eee0198342315c3']``

- security_group_ids:
     List of security group ids

     Default: ``['sg-032937cc5a4b09451']``

- **kwargs:
    Any extra keyword arguments that you want to pass to the SageMaker's Estimator.


Usage
------

.. code-block:: python

    from sagemaker_jobs import create_training_jobs, get_sagemaker_client, ML_M5_4XLARGE


    create_training_job(
        docker_image_arn='123456789012.dkr.ecr.us-east-1.amazonaws.com/sagemaker-decision-trees:latest',
        sagemaker_role='arn:aws:iam::123456789012:role/SageMakerRole',
        sagemaker_bucket='sagemaker_artifacts',
        input_s3_data_path='input_data',
        instance_type=ML_M5_4XLARGE,
        max_run=86400,
        max_wait=86401,
        use_spot_instances=True,
        base_job_name="Decision Tree Job",
        use_vpc=True,
        subnets=['subnet-09eee0198452315c3'],
        security_group_ids=['sg-098457cc5a4b04971'],
    )

    # Stop a training job
    sagemaker_client = get_sagemaker_client()
    sagemaker_client.stop_training_job(TrainingJobName='Decision Tree Job')



Notes
------

1. By default a training job uses Spot instances to save costs but this may result in the training job getting interrupted in case there are no Spot instances available.


How to Modify this Package
----------------------------

1. This package works with Python 3
2. After making the necessary changes run the following commands to build the project and install the package

.. code-block:: bash

    python setup.py sdist
    sudo -E python -m pip install dist/sagemaker-jobs-0.1.tar.gz


3. You can uninstall the package by running the following command - ``sudo -E pip uninstall sagemaker-jobs``
4. To switch virtual environments on the JupyterHub server use these commands

.. code-block:: bash

    conda env list
    source activate <environment-from-above-list>
