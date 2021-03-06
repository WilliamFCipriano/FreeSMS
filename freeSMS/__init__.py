#!/usr/bin/env python2

# This script attempts to send a SMS via Email message for free.
# It does this by attempting to deliver to a list of email gateways for a large number of carriers
# Sending directly to the correct gateway would be preferred, but this script assumes you don't know it
# When the recipient responds, you can email back and forth normally via the correct gateway
import emailer


def text(number,message,gateway_list = 'data/us-gateways.list',loud=False, rate=4):
    email = open('email.config')
    email = email.read().split(':')

    gateway_list = open(gateway_list)
    gateway_list = gateway_list.read().split('\n')

    hit_gateways = list()
    addresses = list()
    for gateway in gateway_list:
        gateway = gateway.split(':')
        if gateway[0] not in hit_gateways:
            addresses.append(number + '@' + gateway[0])
        else:
            if loud:
                print gateway[1] + ' uses gateway already hit ' + gateway[0] + ' skipping.'
        if len(addresses) >= rate:
            if loud:
                for address in addresses:
                    print 'SMS attempt to ' + address
            try:
                emailer.email(email[0],email[1],email[2],email[3],addresses,message)
            except Exception as ex:
                if loud:
                    print 'Email failed!'
                    print 'failed with error' + str(ex)
            hit_gateways.append(gateway[0])
            addresses = list()


# This module can be used by itself if you wish
if __name__ == "__main__":
    import sys
    try:
        number = sys.argv[1]
    except:
        print 'Proper Syntax: [command] [10-digit-phone-number] [message]'
        print 'Example: __init__.py 5551239876 This is how you send a text message!'
        sys.exit(0)
    x = 0
    message = ''
    for args in sys.argv:
        if x >= 2:
            message = message + " " + str(args)
        x += 1
    text(number,message,loud=True)