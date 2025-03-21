from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="APP",
    settings_files=["settings.yaml", ".secrets.yaml"],
    environments=False,
    load_dotenv=True,
)