#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { LlamaAwsLambdaSlackChatbotStack } from "../lib/llama-aws-lambda-slack-chatbot-stack";
import * as dotenv from "dotenv";

dotenv.config();

const app = new cdk.App();

// TODO: Use zod to validate process.env.*
new LlamaAwsLambdaSlackChatbotStack(app, process.env.STACK_NAME!, {
  SLACK_SIGNING_SECRET: process.env.SLACK_SIGNING_SECRET!,
  SLACK_BOT_TOKEN: process.env.SLACK_BOT_TOKEN!,
});
