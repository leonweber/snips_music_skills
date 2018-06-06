#!/usr/bin/env python2

import subprocess
import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io



RADIOS = {
        "radio one": "http://radioeins.de/stream"
        }

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    current_session_id = intentMessage.session_id
    radio_name = intentMessage.slots.radio_name[0].raw_value
    if radio_name in RADIOS:
        subprocess.call(["mplayer", RADIOS[radio_name]])
    else:
        hermes.publish_end_session(current_session_id, "Sorry, I could not find a radio with the name " + radio_name)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("nodewig:radioOn", subscribe_intent_callback) \
         .start()

