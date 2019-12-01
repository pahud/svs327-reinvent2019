# Lab 5 - Testing and clean up

We have built everything we require with less than 200 lines of AWS CDK.



After deployment completed, you will see the output like this:

```
Outputs:
CdkStack.TableName = CdkStack-TableCD117FA1-1EYUN5Z89QXBZ
CdkStack.TopicArn = arn:aws:sns:us-west-2:903779448426:CdkStack-TopicBFC7AF6E-6YDKX2V5PZ3J
CdkStack.BookCommand = curl -s -XPOST -H 'content-type: application/json' https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/book
CdkStack.BookingAPIEndpoint = https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/book
CdkStack.myapiEndpoint3628AFE3 = https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/
CdkStack.QueueName = CdkStack-Queue4A7E3555-IFW7JAOKDTJK
CdkStack.QueryAPIEndpoint = https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/query/{message_id}

Stack ARN:
arn:aws:cloudformation:us-west-2:903779448426:stack/CdkStack/c1903f00-13f6-11ea-b64e-0a6b72e80b7e
```



Let's submit a booking request to the **BookingAPIEndpoint** - simply copy and paste the **BookCommand** provided and pipe to `jq` to format the JSON output if you prefer.

```sh
curl -s -XPOST -H 'content-type: application/json' https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/book | jq
{
  "PublishResponse": {
    "PublishResult": {
      "MessageId": "1eb55497-3d8b-51b5-8c55-02ca77671c42",
      "SequenceNumber": null
    },
    "ResponseMetadata": {
      "RequestId": "f40758cc-5ab5-53d5-9f9d-0e9110596e22"
    }
  }
}
```



OK we got our MessageId, wihch is the ticket indicates our booking request is being processed. Let's check the booking result from another API.

curl the **QueryAPIEndpoint** like this and replace the `{message_id}` with the one you recieved above.

```sh
curl -s https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/query/{message_id}
```

e.g.

```sh
curl -s https://6gh9klhwph.execute-api.us-west-2.amazonaws.com/prod/query/1eb55497-3d8b-51b5-8c55-02ca77671c42 | jq 
{
  "result": "booking completed",
  "confirm_code": "7b194ae1-b3c9-4125-ab09-53e30f1a4c39",
  "message_id": "1eb55497-3d8b-51b5-8c55-02ca77671c42"
}
```

OK my ticket booking is `completed` and I got the **confirm_code** as well.



# Clean up

Just like most AWS CDK applications, simpliy run `cdk destroy` to destroy all resources created by AWS CDK.

```js
# destroy all resources created by AWS CDK
$ cdk destroy
```

OK. Let's move to [Lab 6](lab6.README.md).
