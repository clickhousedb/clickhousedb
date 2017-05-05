import os.path as p

import pytest

from ..cluster import ClickHouseCluster

cluster = ClickHouseCluster(__file__) \
    .add_instance('instance', ['configs/graphite_rollup.xml'])

instance = cluster.instances['instance']


def setup_module():
    print "Setting up cluster..."
    cluster.up()
    cluster.instances['instance'].client.query('CREATE DATABASE test')

def teardown_module():
    print "Shutting down cluster..."
    cluster.down()


def compare_with_reference(sql_file, reference_file):
    current_dir = p.dirname(__file__)
    with open(p.join(current_dir, sql_file)) as sql, open(p.join(current_dir, reference_file)) as reference:
        assert instance.client.query(sql.read()) == reference.read()


def test1():
    compare_with_reference('test1.sql', 'test1.reference')

def test2():
    compare_with_reference('test2.sql', 'test2.reference')

def test3():
    compare_with_reference('test3.sql', 'test3.reference')

def test4():
    compare_with_reference('test4.sql', 'test4.reference')
