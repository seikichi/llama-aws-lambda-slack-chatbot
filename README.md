# LLaMA AWS Lambda Slack Chatbot

![screenshot](/images/llama.png?raw=true)

## Deploy

1. Create new Slack app
2. Create .env file from .env.sample
3. Create llama.cpp model and save as chatbot/model.bin
4. Run `cdk deploy`
5. Update App Manifest using Function URL

```yaml
display_information:
  name: LLaMA
features:
  bot_user:
    display_name: LLaMA
    always_online: true
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - chat:write
settings:
  event_subscriptions:
    request_url: https://FIXME.lambda-url.FIXME.on.aws/slack/events
    bot_events:
      - app_mention
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```
