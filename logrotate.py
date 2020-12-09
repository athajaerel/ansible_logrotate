## :( @devlaptop68:~ $ more .local/bin/lr_if.bash 
##!/bin/bash
#
## possible improvement: deploy conf if not exist, substitute $HOME
#
#[ ! -d $HOME/.lr ] && mkdir $HOME/.lr
#[ ! -d $HOME/old_logs ] && mkdir $HOME/old_logs
#
#/usr/sbin/logrotate -f $HOME/.lr/lr_if.conf -s $HOME/.lr/logrotate.state
#
## :) @devlaptop68:~ $ more .lr/lr_if.conf 
#/path/ansible.log
#{
#	rotate 1000
#	olddir /home/adam.richardson/old_logs
#	compress
#	nodateext
#	missingok
#}

from __future__ import (absolute_import, division, print_function)
from ansible.plugins.callback import CallbackBase

__metaclass__ = type

import json
#import urllib2
import sys
import os

DOCUMENTATION = '''
    callback: logrotate
    callback_type: aggregate
    options:
      logdir:
        default: $HOME/old_logs
        required: False
        env:
          - name: LOGROTATE_LOGDIR
        ini:
          - section: defaults
            key: logdir
        type: path
        version_added: 0.0.1
      confdir:
        default: $HOME/.lr
        required: False
        env:
          - name: LOGROTATE_CONFDIR
        ini:
          - section: defaults
            key: confdir
        type: path
        version_added: 0.0.1
'''

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_NEEDS_WHITELIST = True
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'logrotate'
    NAME = CALLBACK_NAME # needed?

    def __init__(self):
        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
        self.logdir = os.environ.get('LOGROTATE_LOGDIR')
        self.confdir = os.environ.get('LOGROTATE_CONFDIR')
        if self.logdir is None:
            self.logdir = '%s/old_logs' % os.environ.get('HOME')
        if self.confdir is None:
            self.confdir = '%s/.lr' % os.environ.get('HOME')

    def v2_runner_on_failed(self, taskResult, ignore_errors=False):
        x=1

    def v2_runner_on_skipped(self, result):
        x=1

    def v2_runner_on_ok(self, result):
        x=1

    def v2_runner_on_unreachable(self, result):
        x=1

#    def _time(self):
#        return datetime.datetime.now().strftime("%H:%M:%S")


#    def v2_playbook_on_no_hosts_matched(self):
#        self._display.display("skipping: no hosts matched", color=C.COLOR_SKIP)

#    def v2_playbook_on_no_hosts_remaining(self):
#        self._display.banner("NO MORE HOSTS LEFT")

#    def v2_playbook_on_task_start(self, task, is_conditional):

    def _print_task_banner(self, task):
        # args can be specified as no_log in several places: in the task or in
        # the argument spec.  We can check whether the task is no_log but the
        # argument spec can't be because that is only run on the target
        # machine and we haven't run it thereyet at this time.
        #
        # So we give people a config option to affect display of the args so
        # that they can secure this if they feel that their stdout is insecure
        # (shoulder surfing, logging stdout straight to a file, etc).
        args = ''
        if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
            args = u', '.join(u'%s=%s' % a for a in task.args.items())
            args = u' %s' % args

        self._display.banner(u"TASK [%s%s]" % (task.get_name().strip(), args))
        if self._display.verbosity >= 2:
            path = task.get_path()
            if path:
                self._display.display(u"task path: %s" % path, color=C.COLOR_DEBUG)

        self._last_task_banner = task._uuid

    def v2_playbook_on_cleanup_task_start(self, task):
        self._display.banner("CLEANUP TASK [%s]" % task.get_name().strip())

    def v2_playbook_on_handler_task_start(self, task):
        self._display.banner("RUNNING HANDLER [%s]" % task.get_name().strip())

    def v2_playbook_on_play_start(self, play):

    def v2_on_file_diff(self, result):

    def v2_runner_item_on_ok(self, result):

    def v2_runner_item_on_failed(self, result):

    def v2_runner_item_on_skipped(self, result):

    def v2_playbook_on_include(self, included_file):

    def v2_playbook_on_stats(self, stats):

    def v2_playbook_on_start(self, playbook):

    def v2_runner_retry(self, result):

# hopefully there's a v2_playbook_on_poststats api? assuming stats is what it seems...

