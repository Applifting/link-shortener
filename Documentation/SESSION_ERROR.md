**Problem**: The SessionDict object turned into a dictionary is being serialized,
however its value for the 'user_info' key is a sanic_oauth.core.UserInfo object,
which itself is not serializable. (Solution below)

**Cause**: Google Sign-in probably changed the type of payload, and as such,
the method is now deprecated.

**Code**:
```
@app.middleware('response')
async def save_session(request, response):
    await request.app.session_interface.save(request, response)
```

-> TypeError: <sanic_oauth.core.UserInfo object at 0x7fe840cdd1c0> is not JSON serializable

Location: "/usr/local/lib/python3.8/site-packages/sanic_session/base.py", line 147

Link to location: https://github.com/xen/sanic_session/blob/master/sanic_session/base.py

Command inducing error: "val = ujson.dumps(dict(request[self.session_name]))"

**Diagnostic**:
```
app.session_interface.session_name # -> 'session'
request['session'] # -> <SessionDict {
                          'after_auth_redirect': '/profile',
                          'token': <token>,
                          'user_info': <sanic_oauth.core.UserInfo object>
                          }>
dict(request['session']) # ->
{
  'after_auth_redirect': '/profile',
  'token': <token>,
  'user_info': <sanic_oauth.core.UserInfo object>
}

request['session'].__dict__ # ->
{
  'on_update': <function SessionDict.__init__.<locals>.on_update at 0x7f59032a5280>,
  'sid': '3fda9c9b9e494858aa9885cdda98a019',
  'modified': True
}
request['session'].__dict__['on_update'] ->
<function SessionDict.__init__.<locals>.on_update at 0x7f44b4660280>

request['session'].__dict__['on_update'].__dict__ ->
{}

dir(request['session']) ->
['__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__'
, '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__',
# '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'modified', # 'on_update', 'pop', 'popitem', 'setdefault', 'sid', 'update', 'values']
```
```
Items:  dict_items([('after_auth_redirect', '/profile'), ('token', <token>), ('user_info', <sanic_oauth.core.UserInfo object at 0x7f277815c160>)])
Keys:  dict_keys(['after_auth_redirect', 'token', 'user_info'])
Values:  dict_values(['/profile', <token>, <sanic_oauth.core.UserInfo object at 0x7f277815c160>])
```


**Solution**: Turn the UserInfo object within the SessionDict object into a dictionary
of its own default attributes.


**--- HACK version - do not use --- (Correct version inside codebase - server.py)**
```
if 'user_info' in request['session']:
      try:
          user_obj = request['session'].get('user_info')
          user_dict = user_obj.__dict__
          request['session'].__setitem__('user_info', user_dict)
      except AttributeError:
          pass
```
