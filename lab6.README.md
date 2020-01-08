# Lab 6 - What Next

Congratulations you have completed the labs. We have learned how to build a serverless booking API with AWS CDK by design from scratch. We craft it by creating an abstract diagram and implement it mostly in our favorite IDE such as VSCode. With this approach, we just need to understand the essentials of each AWS services we use and then we shall be able to put them together with AWS CDK even without opening the AWS console for individual services.  We focus on the higher design patterns rather than how to provision the infrastructure or how to create correct IAM policies or security groups.  Actually, we are building our services with **Architecture of the Code**, which we believe is the next phase of Infrastructure of Code for modern applications especially for serverless and container-based applications.


further reading: [Containers and infrastructure as code, like peanut butter and jelly](https://aws.amazon.com/blogs/containers/containers-and-infrastructure-as-code-like-peanut-butter-and-jelly/) by ***Clare Liguori*** posted on 18 OCT 2019.



# Going to Production

This repostory demonstrates how to build a simple serverless booking API in AWS. To move it forward, we still have to put some thoughts into consideration



**Security Hardening** -  We didn't explore how to secure our API service. In the real production environment, we have to leverage some advanced features to harden our API service such as

- API Gateway Access Control - see [Controlling and Managing Access to a REST API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html)  
- [Using AWS WAF to protect your API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-aws-waf.html)
- [DynamoDB encryption at rest with CMK](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html) 
- [Lambda per-function concurrency control](https://docs.aws.amazon.com/lambda/latest/dg/per-function-concurrency.html) 

**Performance** - For the booking status query, the REST API may not be the best option. Consider using API Gateway Websocket API for the status query API or consider using GraphQL with AWS App Sync for replacement.

Consider [DynamoDB Global Table](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html) to replicate the table items across regions so each regional API can access the items locally.

**Error Handling** - Using [AWS Lambda destinations](https://aws.amazon.com/blogs/compute/introducing-aws-lambda-destinations/) to better handle the Lambda function errors or exceptions.

**AWS Event Fork Pipelines** - To fork your booking request to multiple pipelines with different operational logic. See https://aws.amazon.com/about-aws/whats-new/2019/03/introducing-aws-event-fork-pipelines-nested-applications-for-event-driven-serverless-architectures/



# Thanks

Appreciate your participation in this builder session. We are still working on this content to make it better so any github issue or PR is highly welcome and appreciated.

Enjoy your Serverless Building on AWS !
