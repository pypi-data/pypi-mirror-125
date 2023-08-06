# edu-py-logger

## Connection and configuration

Logger connects in the settings with 2 strings:
```
dictConfig(get_config(settings.service_name, settings.logging_file_path))
settings.logger = LoggerService(settings.service_name, settings.run_env)
```

The path for output is set up in env.
```
LOGGING_FILE_PATH=/home/dev/logging.log
```

## Log format
```
(
    "%(service_name)s | "
    "%(ipv4)s | "
    "%(env)s | "
    "%(trace_id)s | "
    "%(correlation_id)s | "
    "%(user_id)s | "
    "%(levelprefix)s | "
    "%(asctime)s | "
    "%(message)s"
)
```
