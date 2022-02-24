# This file defines the function that can be used to create a SageMaker Training job.

import boto3
import sagemaker as sage
from .constants import (
    ML_M5_4XLARGE,
    DEFAULT_REGION,
)


def get_sagemaker_client(region: str = DEFAULT_REGION):
    return boto3.client('sagemaker', region_name=region)


def create_training_job(
        docker_image_arn: str, sagemaker_role: str, sagemaker_bucket: str, input_s3_data_path: str,
        output_s3_data_path: str = '', instance_type: str = ML_M5_4XLARGE, subnets: list = None,
        security_group_ids: list = None, volume_size: int = 30, max_run: int = 86400, max_wait: int = 86401,
        use_spot_instances: bool = True, region: str = DEFAULT_REGION, use_vpc: bool = False, **kwargs
):
    """
        Creates a training job based on the given parameters
        
        docker_image_arn: ARN of the docker image stored in the Amazon ECR.
        sagemaker_role: ARN of the IAM role that will be used to create the training job.
        sagemaker_bucket: S3 bucket where the input artifacts are present and output artifacts are stored
        input_s3_data_path: Location of the input data in the SageMaker S3 Bucket
        output_s3_data_path: Location of the output data in the SageMaker S3 bucket's output folder
        instance_type: Type of the EC2 instance that will be used for training
        volume_size: Size of the EBS volume in GBs. Default is 30 GB.
        max_run:  Timeout in seconds for training (default: 24 * 60 * 60). 
            After this amount of time Amazon SageMaker terminates the job regardless of its current status.
        max_wait: Timeout in seconds waiting for spot training instances (default: 86401). 
            After this amount of time Amazon SageMaker will stop waiting for Spot instances to become available. 
            This must always be greater than max_run.
        use_spot_instances: a boolean value that denotes whether to use EC2 spot instances for this training job
        region: The AWS region in which to create the training job.
        subnets: List of subnet ids
        security_group_ids: List of security group ids
        use_vpc: a boolean value that indicates whether or not to create training job within a VPC. Uses subnets and
            security groups passed in the params or custom default values when set to True. If not specified defaults
            to False and training job will be created without VPC config.

        Usage - 

        create_training_job(
            docker_image_arn='123456789012.dkr.ecr.us-east-1.amazonaws.com/sagemaker-decision-trees:latest',
            sagemaker_role='arn:aws:iam::123456789012:role/SageMakerRole',
            sagemaker_bucket='sagemaker-artifacts',
            input_s3_data_path='input-data',
            instance_type='ml.m5.4xlarge',
            max_run=86400,
            max_wait=86401,
            use_spot_instances=True,
            subnets=['subnet-09eee0125678355c3'],
            security_group_ids=['sg-098457cc5a4b04971'],
            use_vpc=True
        )

        The output by the model will always be found inside the "output" folder in the SageMaker bucket.
    """
    boto3_session = boto3.Session(region_name=region)
    sess = sage.Session(boto_session=boto3_session)
    output_path = f's3://{sagemaker_bucket}/output' + (f'/{output_s3_data_path}' if output_s3_data_path else '')
    if use_vpc:
        tree = sage.estimator.Estimator(
            docker_image_arn, sagemaker_role, 1, instance_type, output_path=output_path,
            use_spot_instances=use_spot_instances, subnets=subnets,
            security_group_ids=security_group_ids,
            max_wait=max_wait, sagemaker_session=sess, max_run=max_run,
            volume_size=volume_size, **kwargs
        )
    else:
        if subnets and security_group_ids:
            raise Exception(f'Job creation Failed. Please make sure to set use_vpc to True for '
                            f'successful creation of training job if you are passing VPC configs'
                            f'(subnets and security groups)')
        tree = sage.estimator.Estimator(
            docker_image_arn, sagemaker_role, 1, instance_type, output_path=output_path,
            use_spot_instances=use_spot_instances, max_wait=max_wait, sagemaker_session=sess,
            max_run=max_run, volume_size=volume_size, **kwargs
        )

    tree.fit(f's3://{sagemaker_bucket}/{input_s3_data_path}')
