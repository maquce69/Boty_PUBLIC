# Telegram bot in OpenShift

This is a template to host in [OpenShift](https://openshift.redhat.com) a Python 3 **Telegram bot** using [Flask](http://flask.pocoo.org/). Build over (https://github.com/maquce69/Boty_PUBLIC)


### Running on OpenShift

Create a Python application with this command

```shell
rhc app-create <project> python-3.6 --from-code https://github.com/maquce69/Boty_PUBLIC
```

### Environment variables

Now we must set some environment variables in openshift: 

**`TELEGRAM_BOT_USERNAME`**: Used to detect mentions to your bot.

**`TELEGRAM_SECRET_URL`**: This bot works with [webhooks](https://core.telegram.org/bots/api#setwebhook), so we need to be notified of new messages. We don't want to be spammed or attacked, so this value should be secret. **Note:** Flask uses `/<secret_url>`, don't use the full url

**`TELEGRAM_TOKEN`**: Is our authorization to use the [Bot API](https://core.telegram.org/bots/api)

```shell
rhc env set TELEGRAM_BOT_USERNAME=<username> TELEGRAM_SECRET_URL=<secret_url> TELEGRAM_TOKEN=<token> -a <project>
```

Once we do this, we must restart the app (you could do this [via web](https://openshift.redhat.com/app/console/applications) too):

```shell
rhc app restart <project>
```


### Connect OpenShift with Telegram

Now our bot is registered (in Telegram) and is ready to answer our commands (in OpenShift), but our messages to the bot are not sent to OpenShift, we must set the (webhook) url that Telegram will use to communicate with our OpenShift application.

We must use the [setWebhook](https://core.telegram.org/bots/api#setwebhook) method. Is simpole, is a GET request, so you can do this in your browser or using cURL:

```shell
curl https://api.telegram.org/bot<token>/setWebhook?url=https://<project>-<namespace>.rhcloud.com/<secret_url>
```

Telegram will answer with this:

```JSON
{
	"ok": true,
	"result": true,
	"description": "Webhook was set"
}
```
### Enjoy

Go to talk your bot (you should find it at **`telegram.me/<username>`**) and try the **`/echo`** command. 

