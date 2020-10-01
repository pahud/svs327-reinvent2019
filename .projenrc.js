const {
  AwsCdkTypeScriptApp,
  Semver
} = require('projen');

const project = new AwsCdkTypeScriptApp({
  cdkVersion: "1.65.0",
  name: "svs327-reinvent2019",
  authorName: "Pahud Hsieh",
  authorEmail: "pahudnet@gmail.com",
  repository: "https://github.com/pahud/svs327-reinvent2019.git",
  cdkDependencies: [
    "@aws-cdk/aws-apigateway",
    "@aws-cdk/aws-dynamodb",
    "@aws-cdk/aws-iam",
    "@aws-cdk/aws-lambda",
    "@aws-cdk/aws-lambda-event-sources",
    "@aws-cdk/aws-sns",
    "@aws-cdk/aws-sns-subscriptions",
    "@aws-cdk/aws-sqs",
  ]
});


const common_exclude = ['cdk.out', 'cdk.context.json', 'docker-compose.yml', 'images', 'yarn-error.log'];
project.npmignore.exclude(...common_exclude);
project.gitignore.exclude(...common_exclude);

project.synth();
