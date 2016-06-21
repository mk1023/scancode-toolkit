#
# Copyright (c) 2015 nexB Inc. and others. All rights reserved.
# http://nexb.com and https://github.com/nexB/scancode-toolkit/
# The ScanCode software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of nexB Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from nexB Inc. and others.
#  Visit https://github.com/nexB/scancode-toolkit/ for support and download.

from __future__ import absolute_import, print_function

import os

from commoncode.testcase import FileBasedTesting

from licensedcode.whoosh_spans.spans import Span

from licensedcode import index
from licensedcode import models
from licensedcode import query


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')



class TestHashMatch(FileBasedTesting):
    test_data_dir = TEST_DATA_DIR

    def test_match_hash_can_match_exactly(self):
        rule_dir = self.get_test_loc('hash/rules')
        rules = list(models._rules_proper(rule_dir))
        idx = index.LicenseIndex(rules)
        query_doc = self.get_test_loc('hash/rules/lgpl-2.0-plus_23.RULE')

        matches = idx.match(query_doc)
        assert 1 == len(matches)
        match = matches[0]
        assert 100 == match.score()
        assert 'hash' == match._type
        assert rules[0] == match.rule
        assert Span(0, 122) == match.qspan
        assert Span(0, 122) == match.ispan

    def test_match_hash_returns_correct_offset(self):
        rule_dir = self.get_test_loc('hash/rules')
        rules = list(models._rules_proper(rule_dir))
        idx = index.LicenseIndex(rules)
        query_doc = self.get_test_loc('hash/query.txt')
        q = query.Query(location=query_doc, idx=idx)
        assert len(q.query_runs) > 1
        print
        matches = idx.match(query_doc)
        assert 1 == len(matches)
        match = matches[0]
        assert 'hash' == match._type
        assert 100 == match.score()
        assert rules[0] == match.rule
        assert Span(1, 123) == match.qspan
        assert Span(0, 122) == match.ispan