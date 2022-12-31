# NJT RAIL ARRIVALS BOARD

Runs as a lambda in the cloud, accessed from a Pi running Chillipie kiosk.

## secrets file
`/secrets.json`

```
{
    "username": "", # NJT rail api username
    "password": "", # NJT rail api password
    "account": "",  #aws account #
    "region": "us-east-1"
}
```

## local testing

1. use the VSCode launch config
2. test `http://127.0.0.1:5000/?station_code=HB`


## deploy to AWS

Using CDK. See template docs below.


### dryrun

See what the CloudFormation template will build. Then deploy

1. `awsp` to select the right AWS profile
2. `cdk synth`
3. `cdk deploy`

try:
https://914hmlqb3h.execute-api.us-east-1.amazonaws.com/?station_code=MB
https://914hmlqb3h.execute-api.us-east-1.amazonaws.com/prod?station_code=MB
https://njtsign-rail.crowdr.org/?station_code=MB
https://njtsign-rail.crowdr.org/prod?station_code=MB


Review changes and update after code changes:
```
cdk diff
cdk deploy
```

## hardware setup

Recommended hardware:
- Raspberry Pi 3 or later with integrated Wifi
- Integrated display and power supply. I like the [SunFounder Raspberry Pi 4 Screen 10.1"](https://www.amazon.com/gp/product/B07FZZ95WN) about $110 on Amazon.

## software setup

1. flash an SD with the [futureice/chilliepie distro](https://github.com/futurice/chilipie-kiosk) pi distro
2. configure networking on the pi by entering Wifi credentials into `wpa_supplicant.conf` text file and saving it to the boot partition on the SD. [walkthrough](https://www.raspberrypi-spy.co.uk/2017/04/manually-setting-up-pi-wifi-using-wpa_supplicant-conf/)
3. configure remote access too for headless installs (create and empty file called `ssh` in the boot partition)
4. boot 
5. set the URL for the kiosk by editing `chillipie-kiosk-url.txt` (see below)
6. TK add some useful cron tasks for maintenance
    - turn on and off overnight
    - reboot nightly
7. configure the system`sudo raspi-config`
    - expand the filesystem to fill the disk
    - set correct time zone
8. reboot (so the fs expands)

## url for fetching content

TBD. intended operation will be to track all arrivals on all routes in all directions at a single station.

```
https://TK.execute-api.us-east-1.amazonaws.com/dev?station=HB
```


# The Simple Webservice

This is an example CDK stack to deploy The Simple Webservice stack described by Jeremy Daly here - https://www.jeremydaly.com/serverless-microservice-patterns-for-aws/#simplewebservice

Most of this code was borrowed from https://www.cdkworkshop.com

This is the most basic of implementations and would have to be hardened before production use. e.g. cognito added to the API Gateway

![Architecture](img/architecture.png)

After deployment you should have a proxy api gateway where any url hits a lambda which inserts a record of the url into a dynamodb with a count of how many times that url has been visited. 

**UPDATE THE ABOVE: THE DATABASE IS REMOVED AND DIFFERENT LAMBDA INVOKED (NJTRAIL SIGN BELOW)**


## CDK Python Useful Commands

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!