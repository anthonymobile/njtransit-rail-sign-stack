# NJTransit Rail Arrivals Board

This is a combination web scraper and service that provides a simple HTML arrivals board for any NJTransit rail station served by the [NJTransit Departure Vision](https://www.njtransit.com/dv-to/) website.

## Examples
- [Hoboken Terminal, 5 arrivals, big text](https://mydeparturevision.crowdr.org/?station_name=Hoboken%20Terminal&font_size=4&num_arrivals=5)
- [Hoboken Terminal, 10 lines, medium text](https://mydeparturevision.crowdr.org/?station_name=Hoboken%20Terminal&font_size=3&num_arrivals=10)
- [Hoboken Terminal, 20 lines, small text](https://mydeparturevision.crowdr.org/?station_name=Hoboken%20Terminal&font_size=2&num_arrivals=20)

## Endpoint
- Production endpoint (FUTURE) https://mydeparturevision.crowdr.org


## Query Arguments

- Required
    - `station_name` - Use full name as required on [NJTransit Departure Vision](https://www.njtransit.com/dv-to/) website.
        - e.g. `https://mydeparturevision.crowdr.org//?station_name=Hoboken%20Terminal`
        - or https://mydeparturevision.crowdr.org/?station_name=Hoboken%20Terminal

- Optional
    - `num_arrivals` - Number of upcoming arrivals to display. (default is specified in `lambda1/config.py`)
        - e.g. `https://mydeparturevision.crowdr.org//?station_name=Hoboken%20Terminal&num_arrivals=5`
    - `font_size` - vw/vh units for CSS styling. 1 is small, 3 (default) is medium, 5 is large.


# CDK Documentation

## deploy

`cdk deploy --profile {profile_name}`

## resources

tutorial on which this is based [here](https://patrick-ryan.medium.com/aws-cdkv2-python-lambda-with-dependencies-the-quick-read-ffe87e555a18)


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
