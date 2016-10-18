This script enables the server to report its ip addresses after change by sending emails.

### Config:

Configurations are divided into two parts. 

First you should check the script `runner.py`, and set the following variables:

- `SERVERNAME`: the name for your server. 
- `EMAIL`: the email account you use to send emails
- `PASSWROD`: password of the email account (Notice that if you use 163.com email account, you should use the password for mobile devices instead of the login password)
- `SMTP_SERVER`: get this setting from your email service provider
- `SMTP_PORT`:

Second, add the emails which you want to be notified when the IP of the server changes to file `emails.yaml`, which is a yaml setting file.

### Usage:

Use **cron** to run this script periodically. First clone this project to your local directory. Make the `runner.py` executable by

```bash
chmod -x /path/to/runner.py
```

Then edit the configuration of cron

```bash
crontab -e
```

Add the following line:

```bash
*/5 * * * * /usr/bin/python /path/to/runner.py
```
