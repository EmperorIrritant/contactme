import json
import boto3

import sys
import pprint

sqs = boto3.client("sqs")
sns = boto3.client("sns")
queue_url = ""
sns_subscription_topic_arn = ""
sns_msg_size_limit = 256*1024

def lambda_handler(event, context):
    messages = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )
    if sys.getsizeof(str(messages)) > sns_msg_size_limit * 0.8:
        for message in messages:
            if sys.getsizeof(str(message)) < sns_msg_size_limit * 0.6:
                msg = pprint.pformat(message)
                response = sns.publish(
                    TopicArn=sns_subscription_topic_arn,
                    Message=msg
                )
            else:
                # TODO Trigger a Lambda using CloudWatch Alarm based on message size instead of processing huge messages here
                pass
    else:
        response = sns.publish(
            TopicArn=sns_subscription_topic_arn,
            Message=str(messages)
        )