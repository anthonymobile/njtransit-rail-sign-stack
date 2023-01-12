# NJTransit Rail Arrivals Board

This is a combination web scraper and service that provides a simple HTML arrivals board for any NJTransit rail station served by the [NJTransit Departure Vision](https://www.njtransit.com/dv-to/) website.

## Examples
- Hoboken Terminal, 10 lines
- Hoboken Terminal, 5 lines
- Hawthorne Station, 10 lines

## Endpoint
- Development endpoint [https://rl2gcitpe7.execute-api.us-east-1.amazonaws.com/](https://rl2gcitpe7.execute-api.us-east-1.amazonaws.com/)
- Production endpoint (FUTURE) https://mydeparturevision.crowdr.org


## Query Arguments

- Required
    - `station_name` - Use full name as required on [NJTransit Departure Vision](https://www.njtransit.com/dv-to/) website.
        - e.g. `https://rl2gcitpe7.execute-api.us-east-1.amazonaws.com/?station_name=Hoboken%20Terminal`

- Optional
    - `num_arrivals` - Number of upcoming arrivals to display. (default is specified in `lambda1/config.py`)
        - e.g. `https://rl2gcitpe7.execute-api.us-east-1.amazonaws.com/?station_name=Hoboken%20Terminal&num_arrivals=5`
    - `font_size` - vw/vh units for CSS styling. 1 is small, 3 (default) is medium, 5 is large.


# CDK Documentation

## deploy

`cdk deploy --profile {profile_name}`

## resources

tutorial on which this is based [here](https://patrick-ryan.medium.com/aws-cdkv2-python-lambda-with-dependencies-the-quick-read-ffe87e555a18)

# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
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

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
