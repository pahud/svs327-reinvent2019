# Lab 3 -   Create the DynamoDB Table

Now we have **Amazon API Gateway**, **Amazon SNS** topic and **Amazon SQS** queue. All booking requests through `/book` REST api will asynchorously hit the SQS queue waiting for the pickup from a worker and persist its state in a highly durable managed datastore. And that's where Amazon DynamoDB come in.


We need to create a simple DynamoDB table with `message_id` as the partition key and enable the DynamoDB stream for this table to make sure when any incoming item insert into this table, another Lambda function will just pickup for the order fullfillment. 


Create the table

```js
    // DynamoDB Table
    const table = new ddb.Table(this, 'Table', {
      partitionKey: {
        name: 'message_id',
        type: ddb.AttributeType.STRING
      },
      stream: ddb.StreamViewType.NEW_IMAGE,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    })
    new cdk.CfnOutput(this, 'TableName', { value: table.tableName })
```



Let's CDK deploy it again

```js
cdk deploy
```

AWS CDK will compile into cloudformation template and create cloudformation changeset and provision this DynamoDB table for you.

Open the DynamoDB console, your table should be ready.

Read all the source code we've covered in this Lab [here](https://github.com/pahud/svs327-reinvent2019/blob/04ee35b11105de4ae8bfafc47a3de06a42488b75/cdk/lib/cdk-stack.ts#L135-L144).

Let's move to [Lab 4](lab4.README.md)

