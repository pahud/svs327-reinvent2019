

# Lab 2 -  Create Amazon API Gateway, Amazon SNS and Amason SQS with AWS CDK



### Build our API Endpoint

Let's check the architecture abstract overview. We need to create a managed API frontend as the endpoint to receive all the booking request and send the request back to the queue asynchronously without blocking the booking requests and immediately return a token. The client should query the booking status with this token on another API(could be REST or GraphQL) so we seperate the booking and query requests.



OK. **Amazon API Gateway** is a great fit as managed REST API service in AWS. Let's create it with AWS CDK. 

 ```js
const api = new apigateway.RestApi(this, 'my-api');
 ```

Our initial API endpoint is completed. and now we need seperate the booking and query resources on it.

**HTTP POST {API_ENDPOINT}/book**  to receive the booking request
**HPTT GET {API_ENDPOINT}/query/{message_id}** to check the booking status

Create the `/book` and `/query` resource

```js
// create /book resource
const book = api.root.addResource('book');
// create /query resource
const query = api.root.addResource('query');
```



### Build API Methods, API Integrations, SNS Topic and SQS queue

Now that we have `/book` and `/query` API resources, we need define the HTTP methods on those resources and the API integration respecrtively. Amazon API Gateway supports many different integrations such as Lambda integration, AWS service integration, mock integration,etc.  We are going to build with AWS service integration for `/book` and Amazon SNS, which means when `/boot` receives the `HTTP POST` request, API Gateway will simply delegate to another IAM role to perform **sns:Publish** API call for us and we don't have to write any Lambda fuction for it. To achieve this, we need create:

1. new **IAM role** with minimal priviledges required
2. **aws service integration**
3. **SNS topic** to receive the API call from API gateway assumed role
4. **SQS queue**

Create the **IAM role** for the service integration

```js
    const integApig2Snsrole = new iam.Role(this, 'IntegApig2SnsRole', {
      assumedBy: new iam.ServicePrincipal('apigateway.amazonaws.com'),
    });
```

The SNS topic

```js
    const topic = this.node.tryGetContext('SNS_TOPIC_ARN') ? 
      sns.Topic.fromTopicArn(this, 'Topic', this.node.tryGetContext('SNS_TOPIC_ARN')) : new sns.Topic(this, 'Topic')
```

The SQS queue

```js
const queue = new sqs.Queue(this, 'Queue')
```

And make the SQS queue to subscribe the SNS topic so all messages published to this topic will pipe to SQS queue.

```js
topic.addSubscription(new subscription.SqsSubscription(queue))
```


Now let's build the **API gateway service integration**. Behind the scene, API Gateway will assume to `integApig2Snsrole` and perform sns publish API calls for us. Read the Amazon SNS API Reference for **Publish** [here](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html). The Sample Request is like

```
https://sns.us-west-2.amazonaws.com/?Action=Publish&TargetArn={TargetArn}&Message={Message}&Version=2010-03-31
```

We can't just **passthrough** the client request to SNS API, instead, we need **transform** it with request templates before sending to SNS API and on receiveing the response from SNS API, we transform again with response templates.

For more info about the aws service integration, click [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-aws-proxy.html).

For more info about the API Gateway mapping templates, check [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/mappings.html).


OK here we go

```js
    const integApig2Sns = new apigateway.AwsIntegration({
      service: 'sns',
      // action: 'Publish',
      path: '/publish',
      proxy: false,
      integrationHttpMethod: 'POST',
      options: {
        credentialsRole: integApig2Snsrole,
        requestParameters: {
          'integration.request.header.Content-Type': '\'application/x-www-form-urlencoded\''
        },
        requestTemplates: {
          'application/json': `Action=Publish&TopicArn=$util.urlEncode('${topic.topicArn}')&Message=$util.urlEncode($input.body)`,
        },
        passthroughBehavior: apigateway.PassthroughBehavior.NEVER,
        integrationResponses: [
          {
            statusCode: '200',
            responseTemplates: { 'application/json': '$input.json("$")' },
            // responseTemplates: { 'application/json': JSON.stringify({ success: true }) },
          },
          {
            selectionPattern: 'Invalid',
            statusCode: '503',
            responseTemplates: { 'application/json': JSON.stringify({ success: false, message: 'Invalid Request' }) },
          },
        ],
      }
    });


    // create integration response programmatically:
    var statuses: { [index: string]: string; } = {
      "200": "",
      "400": "[\s\S]*\[400\][\s\S]*",
      "401": "[\s\S]*\[401\][\s\S]*",
      "403": "[\s\S]*\[403\][\s\S]*",
      "404": "[\s\S]*\[404\][\s\S]*",
      "422": "[\s\S]*\[422\][\s\S]*",
      "500": "[\s\S]*(Process\s?exited\s?before\s?completing\s?request|\[500\])[\s\S]*",
      "502": "[\s\S]*\[502\][\s\S]*",
      "504": "([\s\S]*\[504\][\s\S]*)|(^[Task timed out].*)"
    }

    // create method response
    var methodResponses: apigateway.MethodResponse[] = [];
    for (let status in statuses) {
      // var selectionPattern = statuses[status];
      methodResponses.push({
        statusCode: status,
        // responseParameters: {
        //   "method.response.header.Access-Control-Allow-Origin": true
        // },
        responseModels: {}
      })
    }

    book.addMethod('POST', integApig2Sns, {
      methodResponses
    });



    new cdk.CfnOutput(this, 'BookingAPIEndpoint', { value: `${book.url}` })
    new cdk.CfnOutput(this, 'BookCommand', {
      value: `curl -XPOST -H 'content-type: application/json' ${book.url}`
    })
```

Last but not least, the assumed role used by Amazon API Gateway can't publish to our SNS topic unless we grant the required privileges. Previously we might need to lookup  the document and find all minimal required IAM policies for this role, however, in AWS CDK, simpliy do it like this.

```js
topic.grantPublish(integApig2Snsrole)
```

Which means the SNS topic we created just granted all required IAM policies to this role. Behind the scene, CDK will generated required cloudformation templates to attach required IAM policies to this IAM role we just created.



OK Let's **cdk deploy** it and see if we can create everything defined above.

```js
# open another terminal in your favorite IDE such as VSCode
$ npm run watch  # this will spawn a tsc process to keep monitoring all the typescript files and compile it when you make any change
$ cdk deploy
```

Your API Gateway, SNS and SQS should be ready, let's send a POST request with cURL on the `/book` and open the SQS console to see if the message has arrived.


Click [here](https://github.com/pahud/svs327-reinvent2019/blob/04ee35b11105de4ae8bfafc47a3de06a42488b75/cdk/lib/cdk-stack.ts#L1-L133) to see the source code we've covered.


Great! Let's move to [Lab 3](lab3.README.md).
