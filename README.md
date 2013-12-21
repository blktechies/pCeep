## pullCommitpush
### It's like speed dating, for technology start-up croud.

----
## What you need to know

### app structure
```
.
|- app
     |-- models
     |-- static
     |-- templates
     |-- views
  |-- ui
     |-- coffee
     |-- sass
  |-- tests
```
---

### setup:
```
  $ npm install && bower install
  $ pip install -r requirements.txt
  $ python manage.py devserver
  $ ./db_create.py
  $ ./db_seed.py
  $ python manage.py dev
```
Now the dev server is running, try to log in with a social account.
Once logged in, back in terminal create some dummy messages to yourself:
```
$ ./seed_messages
```


Here's the deal:
NPM sets up grunt and related packages. That includes COMPASS, which requires RUBY (*shakes fist).
Bower sets up frontend stuff, like jquery, moment, socket-io, etc. You can add more as you need.
Grunt compiles coffeescript and scss files to /app/static. 

```
$ grunt build 
```
will concat, minify and uglify files for production. For front-end work, run:
```
$ grunt watch

```


Alvaro Muir, @alvaromuir