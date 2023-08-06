[![pypi](https://img.shields.io/pypi/v/asgi-correlation-id)](https://pypi.org/project/asgi-correlation-id/)
[![test](https://github.com/snok/asgi-correlation-id/actions/workflows/test.yml/badge.svg)](https://github.com/snok/asgi-correlation-id/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/snok/asgi-correlation-id/branch/main/graph/badge.svg?token=1aXlWPm2gb)](https://codecov.io/gh/snok/asgi-correlation-id)

# ASGI Correlation ID middleware

Middleware for generating or propagating correlation IDs, making it possible to connect each of your
logs to a single HTTP request.

Correlation IDs are propagated when HTTP requests contain the `Correlation-ID` HTTP header key,
and generated when no header is present. The key value of the HTTP header can be customized,
and if you're, e.g., on a platform like [Heroku](https://devcenter.heroku.com/articles/http-request-id),
you should use `X-Request-ID` instead.

In addition to the core functionality, the package supports forwarding correlation IDs
to [Sentry](https://sentry.io/organizations/otovo/issues/) events
and [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)
tasks. See the extensions section below for details.

# Table of contents

- [Installation](#installation)
- [Setting up the middleware](#setting-up-the-middleware)
    - [Adding the middleware](#adding-the-middleware)
    - [Middleware settings](#middleware-settings)
    - [Configuring logging](#configuring-logging)
- [Extensions](#extensions)
  - [Sentry](#sentry)
  - [Celery](#celery)
- [Extending Celery further](#setting-up-celery-support)
    - [The feature](#the-feature)
    - [Adding Celery event hooks](#adding-celery-event-hooks)
    - [Celery event hook settings](#celery-event-hook-settings)
    - [Configuring Celery logging](#configuring-celery-logging)


# Installation

```python
pip install asgi-correlation-id
```

# Setting up the middleware

To set up the package, you need to add the middleware *and* configure logging.

## Adding the middleware

The middleware can be added like this

```python
app = FastAPI(middleware=[Middleware(CorrelationIdMiddleware)])
```

or this

```python
app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)
```

or any other way your framework allows.

For [Starlette](https://github.com/encode/starlette) apps, just substitute `FastAPI` with `Starlette` in the example above.

## Middleware settings

The middleware has a few settings. These are the defaults:

```python
class CorrelationIdMiddleware(
    header_name='Correlation-ID',
    validate_guid=True,
    uuid_length=32,
)
```

Each individual setting is described below:

### header_name

The HTTP header key to read IDs from.

In additon to `Correlation-ID`, another popular choice for header name is `X-Request-ID`. Among other things, this
is the standard header value for request IDs on [Heroku](https://devcenter.heroku.com/articles/http-request-id).

Defaults to `Correlation-ID`.

### validate_guid

By default, the middleware validates correlation IDs
as valid UUIDs. If turned off, any string will be accepted.

An invalid header is discarded, and a fresh UUID is generated in its place.

Defaults to `True`.

### uuid_length

Lets you optionally trim the length of correlation IDs.
Probably not needed in most cases, but for, e.g., local development
having 32-length UUIDs in every log output to
your console *can* be excessive.

Defaults to `32`.

## Configuring logging

To get a benefit from the middleware, you'll want to configure your logging setup to log the correlation ID in some form
or another. This way logs can be correlated to a single request - which is largely the point of the middleware.

To set up logging of the correlation ID, you simply have to implement the filter supplied by the package.

If your logging config looks something like this:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'web': {
            'class': 'logging.Formatter',
            'datefmt': '%H:%M:%S',
            'format': '%(levelname)s ... %(name)s %(message)s',
        },
    },
    'handlers': {
        'web': {
            'class': 'logging.StreamHandler',
            'formatter': 'web',
        },
    },
    'loggers': {
        'my_project': {
            'handlers': ['web'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

You simply have to add a log filter, like this

```diff
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
+   'filters': {
+       'correlation_id': {'()': CorrelationId},
+   },
    'formatters': {
        'web': {
            'class': 'logging.Formatter',
            'datefmt': '%H:%M:%S',
+           'format': '%(levelname)s ... [%(correlation_id)s] %(name)s %(message)s',
        },
    },
    'handlers': {
        'web': {
            'class': 'logging.StreamHandler',
+           'filters': ['correlation_id'],
            'formatter': 'web',
        },
    },
    'loggers': {
        'my_project': {
            'handlers': ['web'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

And your log output will go from this

```
INFO ... project.views This is a DRF view log, and should have a GUID.
WARNING ... project.services.file Some warning in a function
INFO ... project.views This is a DRF view log, and should have a GUID.
INFO ... project.views This is a DRF view log, and should have a GUID.
WARNING ... project.services.file Some warning in a function
WARNING ... project.services.file Some warning in a function
```

to containing a correlation ID, connecting each log to a single request

```docker
INFO ... [773fa6885e03493498077a273d1b7f2d] project.views This is a DRF view log, and should have a GUID.
WARNING ... [773fa6885e03493498077a273d1b7f2d] project.services.file Some warning in a function
INFO ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.views This is a DRF view log, and should have a GUID.
INFO ... [99d44111e9174c5a9494275aa7f28858] project.views This is a DRF view log, and should have a GUID.
WARNING ... [0d1c3919e46e4cd2b2f4ac9a187a8ea1] project.services.file Some warning in a function
WARNING ... [99d44111e9174c5a9494275aa7f28858] project.services.file Some warning in a function
```

If you're using things like a json-formatter, just add `correlation-id: %(correlation_id)s` to your list of properties.

# Extensions

We've added a couple of (we think) nice extensions to extend the scope of correlation IDs.

## Sentry

If your project has [sentry-sdk](https://pypi.org/project/sentry-sdk/)
installed, correlation IDs will automatically be added to Sentry events as
a `transaction_id`.

See this [blogpost](https://blog.sentry.io/2019/04/04/trace-errors-through-stack-using-unique-identifiers-in-sentry#1-generate-a-unique-identifier-and-set-as-a-sentry-tag-on-issuing-service)
for a little bit of detail.

## Celery

Calling `task.delay()` in the context of a HTTP request would normally mean that you lose
the correlation ID completely, because your work is picked up by a separate worker in a separate context.

To make sure correlation IDs persist across this jump, we load Celery signal hooks that transfer and receive
correlation IDs from and to task headers.

This behavior is enabled as long as [celery](https://pypi.org/project/celery/) is installed.

# Extending Celery further

Loading correlation IDs from a HTTP request to a background task is enabled by default.

In addition to this though, the package provides one more set of hooks you can use to improve
tracing in Celery.

## The feature

In the case of a HTTP request spawning a background task, we have full information about the sequence of events.
But what happens if that background task spawns more background tasks, or retries and rejections are added to the mix?
As soon as more than one task is spawned, the correlation ID is reduced to an "origin ID" -> the ID of the HTTP request
that spawned the first worker.

In the same way correlation IDs are nice, because it connects logs to a single HTTP request, we would like something to
give us the sequence of events when things get complicated. For this purpose we can extend the concept of a correlation
id by adding a few more IDs. We therefore provide two more log filters:

- A `current_id`, which is a generated UUID, unique to each new worker process
- A `parent_id` which is the `current_id` of the process that issued the current task.

So to summarize, if you add all Celery hooks, you would end up with:

- A `correlation_id`: The ID of an originating HTTP request or a generated ID in the case of scheduled tasks
- A `current_id`: The ID of the current worker process
- A `parent_id`: The ID of the parent worker process if one existed.

This means all logs can be correlated to a single correlation ID, and the sequence of events
can be completely reconstructed, since each new task will have a reference to which process issued it.

## Adding Celery event hooks

Setting up the event hooks is simple, just import `configure_celery_current_and_parent_id` and run it during startup.

```python
from fastapi import FastAPI

from asgi_correlation_id import configure_celery_current_and_parent_id

app = FastAPI()

app.add_event_handler('startup', configure_celery_current_and_parent_id)
```

You can look over the event
hooks [here](https://github.com/snok/asgi-correlation-id/blob/main/asgi_correlation_id/extensions/celery.py).

## Celery event hook settings

The setup function has a single setting.

### uuid_length

Lets you optionally trim the length of IDs.
Probably not needed in most cases, but for, e.g., local development
having 32-length UUIDs in every log output to
your console *can* be excessive.

Defaults to `32`.

## Configuring logging

If this is your logging config after setting up the middleware

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {'()': CorrelationId},
    },
    'formatters': {
        'web': {
            'class': 'logging.Formatter',
            'datefmt': '%H:%M:%S',
            'format': '%(levelname)s ... [%(correlation_id)s] %(name)s %(message)s',
        },
    },
    'handlers': {
        'web': {
            'class': 'logging.StreamHandler',
            'filters': ['correlation_id'],
            'formatter': 'web',
        },
    },
    'loggers': {
        'my_project': {
            'handlers': ['web'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

You simply need to add these lines of code to start logging the `current_id` and `parent_id`

```diff
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {'()': CorrelationId},
+       'celery_tracing': {'()': CeleryTracingIds},
    },
    'formatters': {
        'web': {
            'class': 'logging.Formatter',
            'datefmt': '%H:%M:%S',
            'format': '%(levelname)s ... [%(correlation_id)s] %(name)s %(message)s',
        },
+       'celery': {
+           'class': 'logging.Formatter',
+           'datefmt': '%H:%M:%S',
+           'format': '%(levelname)s ... [%(correlation_id)s] [%(celery_parent_id)s-%(celery_current_id)s] %(name)s %(message)s',
+       },
    },
    'handlers': {
        'web': {
            'class': 'logging.StreamHandler',
            'filters': ['correlation_id'],
            'formatter': 'web',
        },
+       'celery': {
+           'class': 'logging.StreamHandler',
+           'filters': ['correlation_id', 'celery_tracing'],
+           'formatter': 'celery',
+       },
    },
    'loggers': {
        'my_project': {
+           'handlers': ['celery' if any('celery' in i for i in sys.argv) else 'web'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

This example implements separate logging handlers and formatters for Celery and non-celery processes, but that's
not strictly necessary. Using a JSON-formatter is probably also desired once you
get past a small number of log filters, since logs quickly become pretty cluttered.

During development though, using the UUID length can be useful for limiting noise. Something like this
is what we would use ourselves:

```python
{
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'correlation_id': {'()': CorrelationId},
        'celery_tracing': {'()': CeleryTracingIds},
    },
    'formatters': {
        'dev': {
            'class': 'logging.Formatter',
            'datefmt': '%H:%M:%S',
            'format': '%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s',
        },
        'dev-celery': {
            'class': 'logging.Formatter',
            'datefmt': '%H:%M:%S',
            'format': (
                '%(levelname)s:\t\b%(asctime)s %(name)s:%(lineno)d [%(correlation_id)s]'
                ' [%(celery_parent_id)s-%(celery_current_id)s] %(message)s'
            ),
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': """
                asctime: %(asctime)s
                created: %(created)f
                filename: %(filename)s
                funcName: %(funcName)s
                levelname: %(levelname)s
                level: %(levelname)s
                levelno: %(levelno)s
                lineno: %(lineno)d
                message: %(message)s
                module: %(module)s
                msec: %(msecs)d
                name: %(name)s
                pathname: %(pathname)s
                process: %(process)d
                processName: %(processName)s
                relativeCreated: %(relativeCreated)d
                thread: %(thread)d
                threadName: %(threadName)s
                exc_info: %(exc_info)s
                correlation-id: %(correlation_id)s
                celery-current-id: %(celery_current_id)s
                celery-parent-id: %(celery_parent_id)s
            """,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'dev': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['correlation_id'],
            'formatter': 'console',
        },
        'dev-celery': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['correlation_id', 'celery_tracing'],
            'formatter': 'console-celery',
        },
        'json': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['correlation_id'],
            'formatter': 'json',
        },
    },
    'loggers': {
        'my_project': {
            'handlers': [
                'json' if settings.ENVIRONMENT != 'dev'
                else 'dev-celery' if any('celery' in i for i in sys.argv)
                else 'dev'
            ],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```
