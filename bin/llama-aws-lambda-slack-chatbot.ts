#!/usr/bin/env node

import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { LlamaAwsLambdaSlackChatbotStack } from "../lib/llama-aws-lambda-slack-chatbot-stack";
import * as dotenv from "dotenv";
import * as z from "zod";

// To deploy this app, following 4 environment variables are required.
const Env = z.object({
  STACK_NAME: z.string().min(1),
  SLACK_SIGNING_SECRET: z.string().min(1),
  SLACK_BOT_TOKEN: z.string().min(1),
  STOP_SEQUENCE: z.string(),
});

type Env = z.infer<typeof Env>;

// Load .env file and verify environment variables
dotenv.config();
const env = Env.parse(process.env);

// Create cdk app and stack...
const app = new cdk.App();

new LlamaAwsLambdaSlackChatbotStack(app, env.STACK_NAME, {
  SLACK_SIGNING_SECRET: env.SLACK_SIGNING_SECRET,
  SLACK_BOT_TOKEN: env.SLACK_BOT_TOKEN,
  STOP_SEQUENCE: env.STOP_SEQUENCE,
});
