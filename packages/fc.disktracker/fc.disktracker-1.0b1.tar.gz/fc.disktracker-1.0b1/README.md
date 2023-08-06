
fc.disktracker
============== 

fc.disktracker is a utility that collects hard disksm their models and
serial numbers and forwards them to the sinpe-it system 



Development environment
-----------------------

To install this package for development in a checkout, invoke:
	

	./bootstrap.sh

To run the tests, invoke: 
	
	bin/pytest 


Documentation
-------------

To run the disktracker, invoke:

	bin/disktracker


### SnipeIT preperations

Select or create an new user that disktracker can use to interact with SnipeIT. Please ensure that the user has the following rights:

* Create models
* Create manufacturers
* Create assets
* Delete assets
* Checkout assets
* Checkin assets

Create a token for this user. Please consult the official [documentation](https://snipe-it.readme.io/reference#generating-api-tokens) for more information about the token.


### config-file

The config file is expected to be at `/etc/disktracker.conf`. An alternatice path may be given
when the programm is started via the `-c` or `--config` flag. This is an example configuration:

    [snipe.it]
    token = 123456789
    url = https://snipeitinstance.com

The options `token` and `url` are mandatory. The option `url` is used to specify the instance of SnipeIT
the programm should use. The value of the `token` option has to be created with that instance. 
