<<<<<<< HEAD
import unittest
import web
=======
import simplejson
>>>>>>> master

from infogami.infobase import client, server

import utils

def setup_module(mod):
    utils.setup_conn(mod)
    utils.setup_server(mod)
    
    mod.site = client.Site(mod.conn, "test")
    mod.s = mod.site.store
    mod.seq = mod.site.seq
    
def teardown_module(mod):
    utils.teardown_server(mod)
    utils.teardown_conn(mod)
    
class TestRecentChanges:
    def save_doc(self, key, **kw):
        doc = {"key": key, "type": {"key": "/type/object"}}
        return site.save(doc, **kw)
        
    def recentchanges(self, **query):
        return [c.dict() for c in site.recentchanges(query)]
        
    def test_all(self, wildcard):
        self.save_doc("/foo", comment="test recentchanges")
                
        changes = self.recentchanges(limit=1)
        assert changes == [{
            "id": wildcard,
            "kind": "update",
            "author": None,
            "ip": wildcard,
            "timestamp": wildcard,
            "changes": [{"key": "/foo", "revision": 1}],
            "comment": "test recentchanges",
            "data": {}
        }]
                        
        assert site.get_change(changes[0]["id"]).dict() == {
            "id": wildcard,
            "kind": "update",
            "author": None,
            "ip": wildcard,
            "timestamp": wildcard,
            "comment": "test recentchanges",
            "changes": [{"key": "/foo", "revision": 1}],
            "data": {}
        }
    
    def test_key(self, wildcard):
        self.save_doc("/foo")
        self.save_doc("/bar")
    
        changes = self.recentchanges(key="/foo")
        assert len(changes) == 1
        
    def test_query_by_data(self):
        self.save_doc("/one", data={"x": "one"}, comment="one")
        self.save_doc("/two", data={"x": "two"}, comment="two")

        changes = self.recentchanges(data={"x": "one"})
        assert [c['data'] for c in changes] == [{"x": "one"}]

        changes = self.recentchanges(data={"x": "two"})
        assert [c['data'] for c in changes] == [{"x": "two"}]
    
class TestStore:
    def setup_method(self, method):
        s.clear()
        
    def test_getitem(self):
        try:
            s["x"]
        except KeyError:
            pass
        else:
            assert False, "should raise KeyError"
        
        s["x"] = {"name": "x"}
        assert s["x"] == {"name": "x"}
        
        s["x"] = {"name": "xx"}
        assert s["x"] == {"name": "xx"}
        
    def test_contains(self):
        assert "x" not in s
        
        s["x"] = {"name": "x"}
        assert "x" in s

        del s["x"]
        assert "x" not in s
        
    def test_keys(self):
        assert s.keys() == []
        
        s["x"] = {"name": "x"}
        assert s.keys() == ["x"]

        s["y"] = {"name": "y"}
        assert s.keys() == ["y", "x"]
        
        del s["x"]
        assert s.keys() == ["y"]
        
    def test_keys_unlimited(self):
        for i in range(200):
            s[str(i)] = {"value": i}
            
        def srange(*args):
            return [str(i) for i in range(*args)]
            
        assert s.keys() == srange(100, 200)[::-1]
        assert list(s.keys(limit=-1)) == srange(200)[::-1]
        
    def test_key_value_items(self):
        s["x"] = {"type": "foo", "name": "x"}
        s["y"] = {"type": "bar", "name": "y"}
        s["z"] = {"type": "bar", "name": "z"}
        
        assert s.keys() == ["z", "y", "x"]
        assert s.keys(type='bar') == ["z", "y"]
        assert s.keys(type='bar', name="name", value="y") == ["y"]

        assert s.values() == [
            {"type": "bar", "name": "z"},
            {"type": "bar", "name": "y"},
            {"type": "foo", "name": "x"}
        ]
        assert s.values(type='bar') == [
            {"type": "bar", "name": "z"},
            {"type": "bar", "name": "y"}
        ]
        assert s.values(type='bar', name="name", value="y") == [
            {"type": "bar", "name": "y"}
        ]

        assert s.items() == [
            ("z", {"type": "bar", "name": "z"}),
            ("y", {"type": "bar", "name": "y"}),
            ("x", {"type": "foo", "name": "x"})
        ]
        assert s.items(type='bar') == [
            ("z", {"type": "bar", "name": "z"}),
            ("y", {"type": "bar", "name": "y"}),
        ]
        assert s.items(type='bar', name="name", value="y") == [
            ("y", {"type": "bar", "name": "y"}),
        ]
        
    def test_bad_data(self):
        s["x"] = 1
        assert s["x"] == 1
        assert "x" in s
        
class TestSeq:
    def test_seq(self):
        seq.get_value("foo") == 0
        seq.get_value("bar") == 0
        
        for i in range(10):
            seq.next_value("foo") == i+1
            
<<<<<<< HEAD
            
class MockSite:
    def get(self, key, lazy=False):
        return client.Thing(self, key=key)
            
class TestThingData:
    def _verify_thingdata(self, thingdata, data):
        def _verify(v1, v2):
            if isinstance(v2, dict):
                if "key" in v2:
                    assert isinstance(v1, client.Thing) and v1.key == v2['key']
                else:
                    assert isinstance(v1, client.ThingData)
                    self._verify_thingdata(v1, v2)
            elif isinstance(v2, list):
                assert len(v1) == len(v2)
                for x, y in zip(v1, v2):
                    _verify(x, y)
            else:
                assert v1 == v2
        
        assert thingdata.keys() == data.keys()
        assert len(thingdata) == len(data)

        for k in data:
            _verify(thingdata[k], data[k])
        
    def test_data(self):
        data = {
            "key": "/foo",
            "type": {"key": "/type/page"},
            "title": "foo",
            "links": ["http://foo.com", "http://bar.com"],
            "nested": [{
                "x": "a",
                "y": "b"
            }]
        }
        thingdata = client.ThingData(MockSite(), data)
        self._verify_thingdata(thingdata, data)
        
    def test_setattr(self):
        data = {
            "key": "/foo",
            "type": {"key": "/type/page"},
            "title": "foo"
        }
        thingdata = client.ThingData(MockSite(), data)
        
        thingdata['title'] = "bar"

        assert thingdata['title'] == 'bar'
        assert thingdata.title == 'bar'
        assert thingdata.get('title') == 'bar'
        assert thingdata.dict()['title'] == 'bar'

class TestSanity:
    """Simple tests to make sure that queries are working fine via all these layers."""
    def test_reindex(self):
        keys = ['/type/page']
        site._request("/reindex", method="POST", data={"keys": simplejson.dumps(keys)})
