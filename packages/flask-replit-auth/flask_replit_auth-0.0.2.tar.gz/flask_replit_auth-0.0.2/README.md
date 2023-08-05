# The Unofficial Replit Auth Flask Extension
Replit authentication is an amazing thing. It is a bit confusing, though, to get information. This package provides an easy way to do so.
```python
@app.route("/")
def index():
  user(request)
  if request.user:
    return request.user['username']
  else:
    return 'Not logged in!'
```
Usage:  
1. ```from flask import request```  
2. ```from flask_replit_auth import user```  
3. In any request route, call ```user(request)```.  
4. To get information, call ```request.user```. It will either return ```None```, or a ```dict``` with all the information.
# Replit Auth - Frontend
```js
var button = document.getElementById('login_with_replit');

if (location.protocol !== 'https:') {
  alert('Replit auth requires https!');
}

button.onclick = function() {
  window.addEventListener('message', authComplete);

  var h = 500;
  var w = 350;
  var left = (screen.width / 2) - ( w / 2);
  var top = (screen.height / 2) - (h / 2);

  var authWindow = window.open('https://repl.it/auth_with_repl_site?domain=' + location.host, '_blank', 'modal=yes, toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left)

  function authComplete(e) {
    if (e.data !== 'auth_complete') {
      return;
    }

    window.removeEventListener('message', authComplete);

    authWindow.close();
    // Reload the page to get the credentials.
    location.reload();
  }
}
```
Usage:  
1. Apply the code above to your HTML file.  
2. Set the ```id``` of you login button to ```login_with_replit```.  