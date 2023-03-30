# LLaMA AWS Lambda Slack Chatbot

Create a Slack chatbot that can talk to [llama.cpp](https://github.com/ggerganov/llama.cpp) using AWS Lambda.

## Demo

T.B.D.

## Requirements

- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install)

## Deploy (GPT4All)

[GPT4All](https://github.com/nomic-ai/gpt4all) is used here, but you can deploy LLaMA or [Alpaca](https://github.com/ggerganov/llama.cpp#instruction-mode-with-alpaca) by the similar process.

First, prepare gpt4all-lora-quantized.bin according to the llama.cpp documentation ([link](https://github.com/ggerganov/llama.cpp#using-gpt4all)).

Then, create an Slack app:

![create-an-app.png](/images/create-an-app.png?raw=true)

![create-an-app.png](/images/name-app.png?raw=true)

Next, update the App Manifest as follows:

```diff
 display_information:
   name: GPT4All
+features:
+  bot_user:
+    display_name: GPT4All
+    always_online: true
+oauth_config:
+  scopes:
+    bot:
+      - app_mentions:read
+      - chat:write
 settings:
   org_deploy_enabled: false
   socket_mode_enabled: false
   token_rotation_enabled: false
```

![create-an-app.png](/images/app-manifest-first.png?raw=true)

Now you can install the app to your workspace.

![install-to-workspace.png](/images/install-to-workspace.png?raw=true)

OK, get the following information:

- Settings > Basic Information > App Credentials > Signing Secret
- Settings > Install App > Bot User OAuth Token

Create .env file using the above information

```sh
> cp .env.sample .env
> # edit .env
> cat .env
STACK_NAME=LLamaBotStack
SLACK_SIGNING_SECRET=YOUR-SLACK-SIGNING-SECRET
SLACK_BOT_TOKEN=YOUR-BOT=User-OAuth-Token
STOP_SEQUENCE=""
```

Also, please copy model and prompt files to the `chatbot` directory:

```sh
> cp path/to/gpt4all-lora-quantized.bin chatbot/model.bin
> cp prompts/alpaca.txt chatbot/prompt.txt
```

OK, let's deploy the application:

```sh
> cdk deploy
...
Outputs:
LLamaBotStack.SlackEventSubscriptionUrl = https://xxxxxxxxxxx.lambda-url.ap-northeast-1.on.aws/slack/events
```

Using the above URL, update the App Manifest again.

```diff
 display_information:
   name: GPT4All
 features:
   bot_user:
     display_name: GPT4All
     always_online: true
 oauth_config:
   scopes:
     bot:
       - app_mentions:read
       - chat:write
 settings:
+  event_subscriptions:
+    request_url: https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.lambda-url.ap-northeast-1.on.aws/slack/events
+    bot_events:
+      - app_mention
   org_deploy_enabled: false
   socket_mode_enabled: false
   token_rotation_enabled: false
```

![app-manifest-second.png](/images/app-manifest-second.png?raw=true)

That's it! Now you can enjoy the llama.cpp on your Slack workspace.
