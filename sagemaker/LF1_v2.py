import json
import boto3
import re
import os
import io
import csv
#import httplib2
#import urllib
import http.client

#import sagemaker

#from sagemaker.mxnet.model import MXNetPredictor
#from sms_spam_classifier_utilities import one_hot_encode
#from sms_spam_classifier_utilities import vectorize_sequences

def lambda_handler(event, context):
    """Read file from s3 on trigger."""
    s3 = boto3.client("s3")
    if event:
        file_obj = event["Records"][0]
        #print(file_obj)
        filename = str(file_obj['s3']['object']['key'])
        bucketname = str(file_obj['s3']['bucket']['name'])
        ip = file_obj["requestParameters"]["sourceIPAddress"]
        print("Filename: ", filename)
        fileObj = s3.get_object(Bucket=bucketname, Key=filename)
        file_content = fileObj["Body"].read().decode('utf-8')
        
        ### extract From email info
        
        print("@@@@@@@@@@@@@@@@@@@@@")
        #print(file_content)
        patternFrom = "From:(.*?)>"
        patternF = "<(.*?)>"
        substringFrom = re.search(patternFrom, file_content).group(1) + ">"
        EMAIL_FROM = re.search(patternF, substringFrom).group(1)
        print(EMAIL_FROM)
        EMAIL_RECEIVE_DATE = re.findall(r'Date: (.*?)\r\nMessage-ID:', file_content, flags=re.DOTALL)
        print(EMAIL_RECEIVE_DATE)
        EMAIL_SUBJECT = re.findall(r'Subject: (.*?)\r\nTo:', file_content, flags=re.DOTALL)
        print(EMAIL_SUBJECT)
        EMAIL_BODY = re.findall(r'quoted-printable\r\n\r\n(.*?)\r\n\r\n<http', file_content, flags=re.DOTALL)
        print(EMAIL_BODY)
        
        ### segamaker part
        # grab environment variables
          
         
        runtime= boto3.client('runtime.sagemaker')
        ENDPOINT_NAME = 'sms-spam-classifier-mxnet-2020-05-13-10-36-22-042' #os.environ['ENDPOINT_NAME']
        payload = 'FreeMsg: Txt: CALL to No: 8688816 stop?txtStop' #EMAIL_BODY
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                           ContentType='text/csv',
                                           Body=payload)
        
        #result = json.loads(response['Body'].read().decode())
        
        print("@@@@@@@@@@@@@@@@@@@@@")
        print(response)
        #print("@@@ a")
        #print(response['Body'])
        t = response['Body']
        #print("@@@ b")
        #print(t.read())
        #print("@@@ c")
        """
        print(t.read().decode("utf-8"))
        result = json.loads(t.read().decode("utf-8"))
        print("@@@ d")
        print(result)
        #print ("response_payload: {}".format(result))
        
        """
        
        """
        #runtime= boto3.client('runtime.sagemaker')
        endpoint = 'sms-spam-classifier-mxnet-2020-05-13-10-36-22-042' #os.environ['ENDPOINT_NAME']
        cbody = 'FreeMsg: Txt: CALL to No: 8688816 stop?txtStop' #EMAIL_BODY
        
        conn = http.client.HTTPSConnection(endpoint)
        payload = "{\"body\": \"" + str(cbody) + "\"}"
        headers = {
          'Content-Type': 'application/json'
        }
        conn.request("POST", "/Prod", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        
        json_acceptable_string = data.replace("'", "\"")
        d = json.loads(json_acceptable_string)

        print("LABEL:", d['predicted_label'])
        send_email(date, d['predicted_label'], from_email, cbody, subject)
        
        """
        """
        endpoint = 'sms-spam-classifier-mxnet-2020-05-13-10-36-22-042'
        runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='us-east-1')
        content_type = 'text/csv'
        payload = 'FreeMsg: Txt: CALL to No: 86888 & claim your reward of 3 hours talk time to use from your phone now! ubscribe6GBP/ mnth inc 3hrs 16 stop?txtStop' #EMAIL_BODY
        # Send image via InvokeEndpoint API
        response = runtime.invoke_endpoint(EndpointName=endpoint, ContentType=content_type, Body=payload)
        # Unpack response
        print("@@@@@@@@@@ a @@@@@@@@@@@")
        print(response['Body'].read())
        print("@@@@@@@@@@@ b @@@@@@@@@@")
        result = json.loads(response['Body'].read().decode())
        print("@@@@@@@@@@@ c @@@@@@@@@@")
        print(result)
        """
        """
        sagemaker = boto3.client('sagemaker-runtime')

        custom_attributes = "c000b4f9-df62-4c85-a0bf-7c525f9104a4"  # An example of a trace ID.
        endpoint_name = "sms-spam-classifier-mxnet-2020-05-13-10-36-22-042"                                       # Your endpoint name.
        content_type = "text/csv"                                        # The MIME type of the input data in the request body.
        accept = "..."                                              # The desired MIME type of the inference in the response.
        payload = EMAIL_BODY                                             # Payload for inference.
        
        response = sagemaker.invoke_endpoint(
            EndpointName=endpoint_name, 
            CustomAttributes=custom_attributes, 
            ContentType=content_type,
            Accept=accept,
            Body=payload
            )
        
        print(response['CustomAttributes'])
        # Uncomment the following line to connect to an existing endpoint.
        # mxnet_pred = MXNetPredictor('<endpoint_name>')
        
        test_messages = ["FreeMsg: Txt: CALL to No: 86888 & claim your reward of 3 hours talk time to use from your phone now! ubscribe6GBP/ mnth inc 3hrs 16 stop?txtStop"]
        #test_messages = [EMAIL_BODY]
        one_hot_test_messages = one_hot_encode(test_messages, vocabulary_length)
        encoded_test_messages = vectorize_sequences(one_hot_test_messages, vocabulary_length)
        
        result = mxnet_pred.predict(encoded_test_messages)
        print(result)
        """
        
        CLASSIFICATION = "Ham"
        CLASSIFICATION_CONFIDENCE_SCORE = "99"
        

        ### reply
        subject = 'Ham or Spam judgement for CSGY9223 -G- CChw4' #+ bucket_name
        body = "We received your email sent at " \
        + str(EMAIL_RECEIVE_DATE) + " with the subject " \
        + str(EMAIL_SUBJECT) + ". Here is a 240 character sample of the email body: " \
        + str(EMAIL_BODY) + " The email was categorized as " \
        + str(CLASSIFICATION) + " with a [" \
        + str(CLASSIFICATION_CONFIDENCE_SCORE) + "%] confidence."#.format(action, object, ip)
        
        message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
    
        ses = boto3.client("ses")
        response = ses.send_email(Source = "info@mike30327.engineer", 
        Destination = {"ToAddresses": [EMAIL_FROM]}, 
        Message = message)
        
        print("@@@@@@@@@@@@@@@@@@@@@")
                
    return 'Thanks'