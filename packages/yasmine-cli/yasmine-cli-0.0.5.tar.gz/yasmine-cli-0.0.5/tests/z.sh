#!/bin/bash

cat test_data/Test.xml | yasmine-cli --field=code --value=MIKE --level_station=*.ANMO --dont_validate | \
    yasmine-cli --field=latitude --value=33.77 --level_station=*.CCM | \
    yasmine-cli --field=operators --value=yml:yml/operators.yml --level_station=*.MIKE | \
    yasmine-cli --field=operators[1] --value=yml:yml/operator.yml --level_station=*.MIKE -o y.xml

