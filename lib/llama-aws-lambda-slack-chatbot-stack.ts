import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as path from "path";
import * as dotenv from "dotenv";

dotenv.config();

export class LlamaAwsLambdaSlackChatbotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const chatbot = new lambda.DockerImageFunction(this, "ChatBotFunction", {
      timeout: cdk.Duration.seconds(900),
      code: lambda.DockerImageCode.fromImageAsset(
        path.join(__dirname, "..", "chatbot")
      ),
      environment: {
        SLACK_SIGNING_SECRET: process.env.SLACK_SIGNING_SECRET!,
        SLACK_BOT_TOKEN: process.env.SLACK_BOT_TOKEN!,
      },
      memorySize: 8192,
    });

    chatbot.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      // cors: {
      //   allowedMethods: [lambda.HttpMethod.POST],
      //   allowedOrigins: ["TODO"],
      // },
    });

    // https://github.com/slackapi/bolt-python/blob/main/slack_bolt/adapter/aws_lambda/lazy_listener_runner.py#L25
    const policy = new iam.PolicyStatement({
      resources: ["*"],
      actions: ["lambda:InvokeFunction"],
    });

    chatbot.addToRolePolicy(policy);
  }
}
