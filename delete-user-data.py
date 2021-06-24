#!/usr/bin/env python

# Copyright (C) 2019-2020 University of Dundee & Open Microscopy Environment.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# Delete users' data to free space on the server.
# author: m.t.b.carroll@dundee.ac.uk

import omero

from omero.gateway import BlitzGateway
from omero.rtypes import rlong
from omero.sys import ParametersI
from omero.cli import cli_login
from omero.cmd import \
    Delete2, Delete2Response, \
    DiskUsage2, DiskUsage2Response, \
    LegalGraphTargets, LegalGraphTargetsResponse

import sys

from argparse import ArgumentParser
from copy import copy
from getpass import getuser
from time import time

parser = ArgumentParser()
parser.add_argument("--days", "-d", type=int, default=0)
parser.add_argument("--inodes", "-i", type=int, default=0)
parser.add_argument("--gigabytes", "-g", type=int, default=0)
parser.add_argument("--force", "-f", default=False, action="store_true")
parser.add_argument("--test", "-t", default=False, action="store_true")
ns = parser.parse_args()

# Do not delete data of users who logged out within recent days.
minimum_days = ns.days

# How many inodes need to be removed, can be 0.
excess_file_count = ns.inodes

# How many bytes need to be deleted, can be 0; written as n * 1GB.
excess_file_size = ns.gigabytes * 1000**3

# Leave this as True except when running the script for real.
dry_run = not ns.force

# https://bugs.python.org/issue11588 would allow argparse to do this.
if not ns.test and excess_file_count == 0 and excess_file_size == 0:
    parser.error("specify how much to delete")

# Report configuration.

print('Ignoring users who have logged out within the past {} days.'
      .format(minimum_days))

if excess_file_count > 0:
    print('Aiming to delete at least {:,} files.'
          .format(excess_file_count))

if excess_file_size > 0:
    print('Aiming to delete at least {:,} bytes of data.'
          .format(excess_file_size))

if dry_run:
    print('Despite output, will not actually delete any data.')
else:
    print('Running for real: will actually delete data.')


# If adjusting UserStats, find_worst, choose_users then check with "--test".

class UserStats:
    # Represents a user and their resource usage.
    # "is_worse_than" defines a strict partial order.

    def __init__(self, id, name, count, size, logout):
        self.id = id
        self.name = name
        self.count = count
        self.size = size
        self.logout = logout

    def is_worse_than(self, other):
        if other.count > self.count or other.size > self.size or \
           other.logout < self.logout:
            return False
        return self.count > other.count or self.size > other.size or \
            self.logout < other.logout


def find_worst(user_stats):
    # Partition the users into the worst and any remainder.
    worst = []
    other = []
    for new in user_stats:
        if any([old.is_worse_than(new) for old in worst]):
            other.append(new)
        else:
            other.extend([old for old in worst if new.is_worse_than(old)])
            worst = [old for old in worst if not new.is_worse_than(old)]
            worst.append(new)
    return (worst, other)


def choose_users(file_count, file_size, user_stats):
    # Iterate through users one by one until enough data would be deleted.
    to_delete = []
    reducing_file_count = True
    reducing_file_size = True
    while user_stats:
        if reducing_file_count and file_count <= 0:
            reducing_file_count = False
            for user_stat in user_stats:
                user_stat.count = 0
        if reducing_file_size and file_size <= 0:
            reducing_file_size = False
            for user_stat in user_stats:
                user_stat.size = 0
        if not (reducing_file_count or reducing_file_size):
            break
        (worst, other) = find_worst(user_stats)
        target_user = worst[0]
        user_stats = worst[1:] + other
        to_delete.append(target_user)
        file_count -= target_user.count
        file_size -= target_user.size
    return to_delete


def submit(conn, request, expected):
    # Submit a request and wait for it to complete.
    # Returns with the response only if it was of the given type.
    cb = conn.c.submit(request, loops=500)
    try:
        rsp = cb.getResponse()
    finally:
        cb.close(True)

    if not isinstance(rsp, expected):
        conn._closeSession()
        sys.exit('unexpected response: {}'.format(rsp))
    return rsp


def get_delete_classes(conn):
    # Find the model object types to query and target in deleting users' data.

    delete_classes = []

    rsp = submit(conn, LegalGraphTargets(request=Delete2()),
                 LegalGraphTargetsResponse)

    params = ParametersI()
    params.addId(rlong(0))
    params.page(0, 1)

    for delete_class in rsp.targets:
        if delete_class.endswith('Link'):
            continue
        # TODO: Skipping these only to prevent console output.
        if delete_class in ['ome.model.meta.GroupExperimenterMap',
                            'ome.model.meta.Namespace',
                            'ome.model.meta.ShareMember']:
            continue
        try:
            conn.getQueryService().projection(
                "SELECT 1 FROM {} WHERE details.owner.id = :id"
                .format(delete_class), params)
            delete_classes.append(delete_class)
        except omero.QueryException:
            # TODO: Suppress console warning output.
            pass
    return delete_classes


def delete_data(conn, user_id):
    # Delete all the data of the given user. Respects the state of dry_run.
    all_groups = {'omero.group': '-1'}
    params = ParametersI()
    params.addId(rlong(user_id))
    delete = Delete2(dryRun=dry_run, targetObjects={})
    for delete_class in get_delete_classes(conn):
        object_ids = []
        for result in conn.getQueryService().projection(
                "SELECT id FROM {} WHERE details.owner.id = :id"
                .format(delete_class), params, all_groups):
            object_id = result[0].val
            object_ids.append(object_id)
        if object_ids:
            delete.targetObjects[delete_class] = object_ids
    if delete.targetObjects:
        submit(conn, delete, Delete2Response)


def find_users(conn):
    # Determine which users' data to consider deleting.

    users = {}

    for result in conn.getQueryService().projection(
            "SELECT id, omeName FROM Experimenter", None):
        user_id = result[0].val
        user_name = result[1].val
        if user_name not in ('PUBLIC', 'guest', 'root', 'monitoring'):
            users[user_id] = user_name

    for result in conn.getQueryService().projection(
            "SELECT DISTINCT owner.id FROM Session WHERE closed IS NULL",
            None):
        user_id = result[0].val
        if user_id in users.keys():
            print('Ignoring "{}" (#{}) who is logged in.'
                  .format(users[user_id], user_id))
            del users[user_id]

    now = time()

    logouts = {}

    for result in conn.getQueryService().projection(
            "SELECT owner.id, MAX(closed) FROM Session GROUP BY owner.id",
            None):
        user_id = result[0].val
        if user_id not in users:
            continue

        if result[1] is None:
            # never logged in
            user_logout = 0
        else:
            # note time in seconds since epoch
            user_logout = result[1].val / 1000

        days = (now - user_logout) / (60 * 60 * 24)
        if (days < minimum_days):
            print('Ignoring "{}" (#{}) who logged in recently.'
                  .format(users[user_id], user_id))
            del users[user_id]

        logouts[user_id] = user_logout
    return users, logouts


def resource_usage(conn):
    # Note users' resource usage.
    # DiskUsage2.targetClasses remains too inefficient so iterate.

    user_stats = []
    users, logouts = find_users(conn)
    for user_id, user_name in users.items():
        print('Finding disk usage of "{}" (#{}).'.format(user_name, user_id))
        user = {'Experimenter': [user_id]}
        rsp = submit(conn, DiskUsage2(targetObjects=user), DiskUsage2Response)

        file_count = 0
        file_size = 0

        for who, usage in rsp.totalFileCount.items():
            if who.first == user_id:
                file_count += usage
        for who, usage in rsp.totalBytesUsed.items():
            if who.first == user_id:
                file_size += usage

        if file_count > 0 or file_size > 0:
            user_stats.append(UserStats(
                user_id, user_name, file_count, file_size, logouts[user_id]))
    return user_stats


def run_tests():
    # Run tests on "choose_users".

    alice = UserStats(0, 'Alice', 0, 0, 0)
    chloe = UserStats(0, 'Chloe', 0, 1, 0)
    daisy = UserStats(0, 'Daisy', 0, 2, 0)
    elsie = UserStats(0, 'Elsie', 1, 0, 0)
    emily = UserStats(0, 'Emily', 1, 1, 0)
    ethan = UserStats(0, 'Ethan', 1, 2, 0)
    freya = UserStats(0, 'Freya', 2, 0, 0)
    grace = UserStats(0, 'Grace', 2, 1, 0)
    henry = UserStats(0, 'Henry', 2, 2, 0)
    isaac = UserStats(0, 'Isaac', 0, 0, 1)
    jacob = UserStats(0, 'Jacob', 0, 1, 1)
    james = UserStats(0, 'James', 0, 2, 1)
    logan = UserStats(0, 'Logan', 1, 0, 1)
    lucas = UserStats(0, 'Lucas', 1, 1, 1)
    mason = UserStats(0, 'Mason', 1, 2, 1)
    oscar = UserStats(0, 'Oscar', 2, 0, 1)
    poppy = UserStats(0, 'Poppy', 2, 1, 1)
    sofia = UserStats(0, 'Sofia', 2, 2, 1)

    test_users = [alice, chloe, daisy, elsie, emily, ethan,
                  freya, grace, henry, isaac, jacob, james,
                  logan, lucas, mason, oscar, poppy, sofia]

    test_cases = [
        (0, 0, set()),
        (1, 1, {'Henry'}),
        (2, 2, {'Henry'}),
        (6, 0, {'Freya', 'Grace', 'Henry'}),
        (6, 2, {'Freya', 'Grace', 'Henry'}),
        (0, 6, {'Daisy', 'Ethan', 'Henry'}),
        (2, 6, {'Daisy', 'Ethan', 'Henry'}),
        (6, 6, {'Ethan', 'Grace', 'Henry', 'Sofia'}),
        (7, 7, {'Ethan', 'Grace', 'Henry', 'Sofia'}),
        (6, 8, {'Daisy', 'Ethan', 'Grace', 'Henry', 'Sofia'}),
        (6, 9, {'Daisy', 'Ethan', 'Grace', 'Henry', 'Sofia'}),
        (8, 6, {'Ethan', 'Freya', 'Grace', 'Henry', 'Sofia'}),
        (9, 6, {'Ethan', 'Freya', 'Grace', 'Henry', 'Sofia'}),
        (2, 15, {'Chloe', 'Daisy', 'Emily', 'Ethan', 'Grace', 'Henry',
                 'James', 'Mason', 'Sofia'}),
        (6, 15, {'Chloe', 'Daisy', 'Emily', 'Ethan', 'Grace', 'Henry',
                 'James', 'Mason', 'Sofia'}),
        (15, 2, {'Elsie', 'Emily', 'Ethan', 'Freya', 'Grace', 'Henry',
                 'Oscar', 'Poppy', 'Sofia'}),
        (15, 6, {'Elsie', 'Emily', 'Ethan', 'Freya', 'Grace', 'Henry',
                 'Oscar', 'Poppy', 'Sofia'}),
        (13, 13, {'Daisy', 'Emily', 'Ethan', 'Freya', 'Grace', 'Henry',
                  'Mason', 'Poppy', 'Sofia'})]

    case_number = 0

    def test(case_number):
        for file_count, file_size, expected_names in test_cases:
            case_number += 1
            copied_users = list(map(copy, test_users))
            chosen = choose_users(file_count, file_size, copied_users)
            actual_names = set([user.name for user in chosen])
            assert actual_names == expected_names
        return case_number

    case_number = test(case_number)
    test_users.reverse()
    case_number = test(case_number)


def perform_delete(conn):
    # Perform data deletion.
    users = choose_users(excess_file_count, excess_file_size,
                         resource_usage(conn))
    print('Found {} user(s) for deletion.'.format(len(users)))
    for user in users:
        print('Deleting {} GB of data belonging to "{}" (#{}).'.format(
              user.size / 1000**3, user.name, user.id,))
        delete_data(conn, user.id)


def main():

    if ns.test:
        print('Running tests, will then exit.')
        run_tests()
        return  # EARLY EXIT

    with omero.cli.cli_login() as cli:
        conn = omero.gateway.BlitzGateway(client_obj=cli.get_client())
        try:
            perform_delete(conn)
        except KeyboardInterrupt:
            pass  # ignore
        finally:
            conn.close()


if __name__ == "__main__":
    main()
