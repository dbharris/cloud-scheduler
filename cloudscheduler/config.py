#!/usr/bin/env python
# vim: set expandtab ts=4 sw=4:

# Copyright (C) 2009 University of Victoria
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

## Auth.: Patrick Armstrong

import os
import sys
from urlparse import urlparse
import ConfigParser

import utilities

# Cloud Scheduler Options Module.

# Set default values
condor_webservice_url = "http://localhost:8080"
condor_collector_url = "http://localhost:9618"
condor_retrieval_method = "soap"
condor_q_command = "condor_q -l"
condor_status_command = "condor_status -l"
condor_host = "localhost"
condor_host_on_vm = ""
condor_context_file = ""
vm_lifetime = 10080
cert_file = ""
key_file = ""
cert_file_on_vm = ""
key_file_on_vm = ""
ca_root_certs = []
ca_signing_policies = []
cloudscheduler_ssh_key = ""
cloud_resource_config = None
image_attach_device = "sda"
scratch_attach_device = "sdb"
info_server_port = 8111
workspace_path = "workspace"
persistence_file = "/var/run/cloudscheduler.persistence"
ban_tracking = False
ban_file = "/var/run/cloudscheduler.banned"
ban_min_track = 5
ban_failrate_threshold = 1.0
polling_error_threshold = 10
condor_register_time_limit = 900
graceful_shutdown = False
graceful_shutdown_method = "hold"
getclouds = False
scheduling_metric = "slot"
high_priority_job_support = False
high_priority_job_weight = 1
cleanup_interval = 5
vm_poller_interval = 5
job_poller_interval = 5
machine_poller_interval = 5
scheduler_interval = 5

log_level = "INFO"
log_location = None
log_stdout = False
log_max_size = None
log_format = "%(asctime)s - %(levelname)s - %(threadName)s - %(message)s"


# setup will look for a configuration file specified on the command line,
# or in ~/.cloudscheduler.conf or /etc/cloudscheduler.conf
def setup(path=None):

    global condor_webservice_url
    global condor_collector_url
    global condor_retrieval_method
    global condor_q_command
    global condor_status_command
    global condor_context_file
    global condor_host
    global condor_host_on_vm
    global vm_lifetime
    global cert_file
    global key_file
    global cert_file_on_vm
    global key_file_on_vm
    global ca_root_certs
    global ca_signing_policies
    global cloudscheduler_ssh_key
    global cloud_resource_config
    global image_attach_device
    global scratch_attach_device
    global info_server_port
    global workspace_path
    global persistence_file
    global ban_tracking
    global ban_file
    global ban_min_track
    global ban_failrate_threshold
    global polling_error_threshold
    global condor_register_time_limit
    global graceful_shutdown
    global graceful_shutdown_method
    global getclouds
    global scheduling_metric
    global high_priority_job_support
    global high_priority_job_weight
    global cleanup_interval
    global vm_poller_interval
    global job_poller_interval
    global machine_poller_interval
    global scheduler_interval

    global log_level
    global log_location
    global log_stdout
    global log_max_size
    global log_format

    homedir = os.path.expanduser('~')

    # Find config file
    if not path:
        if os.path.exists(homedir + "/.cloudscheduler/cloud_scheduler.conf"):
            path = homedir + "/.cloudscheduler/cloud_scheduler.conf"
        elif os.path.exists("/etc/cloudscheduler/cloud_scheduler.conf"):
            path = "/etc/cloudscheduler/cloud_scheduler.conf"
        else:
            print >> sys.stderr, "Configuration file problem: There doesn't " \
                  "seem to be a configuration file. " \
                  "You can specify one with the --config-file parameter, " \
                  "or put one in ~/.cloudscheduler/cloud_scheduler.conf or "\
                  "/etc/cloudscheduler/cloud_scheduler.conf"
            sys.exit(1)

    # Read config file
    config_file = ConfigParser.ConfigParser()
    try:
        config_file.read(path)
    except IOError:
        print >> sys.stderr, "Configuration file problem: There was a " \
              "problem reading %s. Check that it is readable," \
              "and that it exists. " % path
        raise
    except ConfigParser.ParsingError:
        print >> sys.stderr, "Configuration file problem: Couldn't " \
              "parse your file. Check for spaces before or after variables."
        raise
    except:
        print "Configuration file problem: There is something wrong with " \
              "your config file."
        raise

    if config_file.has_option("global", "condor_retrieval_method"):
        condor_retrieval_method = config_file.get("global",
                                                "condor_retrieval_method")

    if config_file.has_option("global", "condor_q_command"):
        condor_q_command = config_file.get("global",
                                                "condor_q_command")

    if config_file.has_option("global", "condor_status_command"):
        condor_status_command = config_file.get("global",
                                                "condor_status_command")

    if config_file.has_option("global", "condor_webservice_url"):
        condor_webservice_url = config_file.get("global",
                                                "condor_webservice_url")

    if config_file.has_option("global", "condor_collector_url"):
        condor_collector_url = config_file.get("global",
                                                "condor_collector_url")

    if config_file.has_option("global", "condor_host_on_vm"):
        condor_host_on_vm = config_file.get("global",
                                                "condor_host_on_vm")

    if config_file.has_option("global", "condor_context_file"):
        condor_context_file = config_file.get("global",
                                                "condor_context_file")

    if config_file.has_option("global", "vm_lifetime"):
        try:
            vm_lifetime = config_file.getint("global", "vm_lifetime")
        except ValueError:
            print "Configuration file problem: vm_lifetime must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "cert_file"):
        cert_file = config_file.get("global", "cert_file")

    if config_file.has_option("global", "key_file"):
        key_file = config_file.get("global", "key_file")

    if config_file.has_option("global", "cert_file_on_vm"):
        cert_file_on_vm = config_file.get("global", "cert_file_on_vm")

    if config_file.has_option("global", "key_file_on_vm"):
        key_file_on_vm = config_file.get("global", "key_file_on_vm")

    if config_file.has_option("global", "ca_root_certs"):
        ca_root_certs = config_file.get("global", "ca_root_certs").split(',')

    if config_file.has_option("global", "ca_signing_policies"):
        ca_signing_policies = config_file.get("global", "ca_signing_policies").split(',')

    if config_file.has_option("global", "cloudscheduler_ssh_key"):
        cloudscheduler_ssh_key = config_file.get("global", "cloudscheduler_ssh_key")

    if config_file.has_option("global", "cloud_resource_config"):
        cloud_resource_config = config_file.get("global",
                                                "cloud_resource_config")

    if config_file.has_option("global", "image_attach_device"):
        image_attach_device = config_file.get("global",
                                                "image_attach_device")

    if config_file.has_option("global", "scratch_attach_device"):
        scratch_attach_device = config_file.get("global",
                                                "scratch_attach_device")

    if config_file.has_option("global", "info_server_port"):
        try:
            info_server_port = config_file.getint("global", "info_server_port")
        except ValueError:
            print "Configuration file problem: info_server_port must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "workspace_path"):
        workspace_path = config_file.get("global", "workspace_path")

    if config_file.has_option("global", "persistence_file"):
        persistence_file = config_file.get("global", "persistence_file")

    if config_file.has_option("global", "ban_file"):
        ban_file = config_file.get("global", "ban_file")

    if config_file.has_option("global", "polling_error_threshold"):
        try:
            polling_error_threshold = config_file.getint("global", "polling_error_threshold")
        except ValueError:
            print "Configuration file problem: polling_error_threshold must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "ban_failrate_threshold"):
        try:
            ban_failrate_threshold = config_file.getfloat("global", "ban_failrate_threshold")
            if ban_failrate_threshold == 0:
                print "Please use a float value (0, 1.0]"
                sys.exit(1)
        except ValueError:
            print "Configuration file problem: ban_failrate_threshold must be an " \
                  "float value."
            sys.exit(1)

    if config_file.has_option("global", "ban_min_track"):
        try:
            ban_min_track = config_file.getint("global", "ban_min_track")
        except ValueError:
            print "Configuration file problem: ban_min_track must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "condor_register_time_limit"):
        try:
            condor_register_time_limit = 60*config_file.getint("global", "condor_register_time_limit")
        except ValueError:
            print "Configuration file problem: condor_register_time_limit must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "ban_tracking"):
        ban_tracking = config_file.getboolean("global", "ban_tracking")

    if config_file.has_option("global", "graceful_shutdown"):
        graceful_shutdown = config_file.getboolean("global", "graceful_shutdown")

    if config_file.has_option("global", "graceful_shutdown_method"):
        graceful_shutdown_method = config_file.get("global", "graceful_shutdown_method")

    if config_file.has_option("global", "getclouds"):
        getclouds = config_file.getboolean("global", "getclouds")
        
    if config_file.has_option("global", "scheduling_metric"):
        scheduling_metric = config_file.get("global", "scheduling_metric")

    if config_file.has_option("global", "high_priority_job_support"):
        high_priority_job_support = config_file.getboolean("global", "high_priority_job_support")

    if config_file.has_option("global", "high_priority_job_weight"):
        try:
            high_priority_job_weight = config_file.getint("global", "high_priority_job_weight")
        except ValueError:
            print "Configuration file problem: high_priority_job_weight must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "scheduler_interval"):
        try:
            scheduler_interval = config_file.getint("global", "scheduler_interval")
        except ValueError:
            print "Configuration file problem: scheduler_interval must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "vm_poller_interval"):
        try:
            vm_poller_interval = config_file.getint("global", "vm_poller_interval")
        except ValueError:
            print "Configuration file problem: vm_poller_interval must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "job_poller_interval"):
        try:
            job_poller_interval = config_file.getint("global", "job_poller_interval")
        except ValueError:
            print "Configuration file problem: job_poller_interval must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "machine_poller_interval"):
        try:
            machine_poller_interval = config_file.getint("global", "machine_poller_interval")
        except ValueError:
            print "Configuration file problem: machine_poller_interval must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("global", "cleanup_interval"):
        try:
            cleanup_interval = config_file.getint("global", "cleanup_interval")
        except ValueError:
            print "Configuration file problem: cleanup_interval must be an " \
                  "integer value."
            sys.exit(1)

    if config_file.has_option("logging", "log_level"):
        log_level = config_file.get("logging", "log_level")

    if config_file.has_option("logging", "log_location"):
        log_location = os.path.expanduser(config_file.get("logging", "log_location"))

    if config_file.has_option("logging", "log_stdout"):
        log_stdout = config_file.getboolean("logging", "log_stdout")

    if config_file.has_option("logging", "log_max_size"):
        try:
            log_max_size = config_file.getint("logging", "log_max_size")
        except ValueError:
            print "Configuration file problem: log_max_size must be an " \
                  "integer value in bytes."
            sys.exit(1)

    if config_file.has_option("logging", "log_format"):
        log_format = config_file.get("logging", "log_format")

    # Derived options
    if condor_host_on_vm:
        condor_host = condor_host_on_vm
    else:
        condor_host = utilities.get_hostname_from_url(condor_webservice_url)
