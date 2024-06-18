# Copyright (c) 2024 SK broadband, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Volume format related Utilities.
"""

from oslo_concurrency import processutils as putils
from oslo_config import cfg
from oslo_log import log as logging

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

SUPPORTED_DRIVER = (
    'cinder.volume.drivers.netapp.common.NetAppDriver',
    'cinder.volume.drivers.rbd.RBDDriver')

SUPPORTED_FORMAT = (
    'etx4',
    'xfs',
    'ntfs')

volume_format_opts = [
    cfg.BoolOpt('empty_volume_format',
               default=False,
               help='Empty volume format type.'),
]

CONF.register_opts(volume_format_opts)


def validate_driver(driver):
    return driver in SUPPORTED_DRIVER

def validate_format(format_type):
    return format_type in SUPPORTED_FORMAT

def create_partition_table(device, style):
    putils.execute('parted', '--script', device, 'mklabel', style,
                     check_exit_code=True)

def create_partition(device, style, fs, start, end):
    putils.execute('parted', '--script', device, '--',
                     'mkpart', style, fs, start, end,
                     check_exit_code=True)

def mkfs(fs, path, label=None):
    """Format a file or block device

    :param fs: Filesystem type (e.g. 'ext4', 'xfs', 'ntfs')
    :param path: Path to file or block device to format
    :param label: Volume label
    """
    args = ['mkfs', '-t', fs, '-f']
    if label:
        label_opt = '-L'
        args.extend([label_opt, label])
    args.append(path)
    putils.execute(*args, check_exit_code=True,
            run_as_root=True)
