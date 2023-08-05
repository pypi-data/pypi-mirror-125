# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_coves',
 'dbt_coves.config',
 'dbt_coves.core',
 'dbt_coves.tasks',
 'dbt_coves.tasks.generate',
 'dbt_coves.ui',
 'dbt_coves.utils']

package_data = \
{'': ['*'], 'dbt_coves': ['templates/*']}

install_requires = \
['Jinja2>=2.11.2,<2.12.0',
 'PyYAML>=5.4.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'dbt>=0.18.0',
 'luddite>=1.0.1,<2.0.0',
 'packaging>=20.8,<21.0',
 'pre-commit>=2.15.0,<3.0.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'pydantic>=1.8,<2.0',
 'pyfiglet>=0.8.post1,<0.9',
 'questionary>=1.9.0,<2.0.0',
 'rich>=10.4.0,<11.0.0',
 'sqlfluff-templater-dbt>=0.7.1,<0.8.0',
 'sqlfluff>=0.7.0,<0.8.0',
 'yamlloader>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['dbt-coves = dbt_coves.core.main:main']}

setup_kwargs = {
    'name': 'dbt-coves',
    'version': '0.21.0a8',
    'description': 'CLI tool for dbt users adopting analytics engineering best practices.',
    'long_description': '\ndbt-coves\n*********\n\n|Maintenance| |PyPI version fury.io| |Code Style| |Checked with mypy| |Imports: isort| |Imports: python| |Build| |pre-commit.ci status| |codecov| |Maintainability| |Downloads|\n\n.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg\n   :target: https://github.com/datacoves/dbt-coves/graphs/commit-activity\n\n.. |PyPI version fury.io| image:: https://badge.fury.io/py/dbt-coves.svg\n   :target: https://pypi.python.org/pypi/dbt-coves/\n\n.. |Code Style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/ambv/black\n\n.. |Checked with mypy| image:: http://www.mypy-lang.org/static/mypy_badge.svg\n   :target: http://mypy-lang.org\n\n.. |Imports: isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336\n   :target: https://pycqa.github.io/isort/\n\n.. |Imports: python| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue\n   :target: https://img.shields.io/badge/python-3.8%20%7C%203.9-blue\n\n.. |Build| image:: https://github.com/datacoves/dbt-coves/actions/workflows/main_ci.yml/badge.svg\n   :target: https://github.com/datacoves/dbt-coves/actions/workflows/main_ci.yml/badge.svg\n\n.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/bitpicky/dbt-coves/main.svg\n   :target: https://results.pre-commit.ci/latest/github/datacoves/dbt-coves/main\n\n.. |codecov| image:: https://codecov.io/gh/datacoves/dbt-coves/branch/main/graph/badge.svg?token=JB0E0LZDW1\n   :target: https://codecov.io/gh/datacoves/dbt-coves\n\n.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/1e6a887de605ef8e0eca/maintainability\n   :target: https://codeclimate.com/github/datacoves/dbt-coves/maintainability\n\n.. |Downloads| image:: https://pepy.tech/badge/dbt-coves\n   :target: https://pepy.tech/project/dbt-coves\n\nWhat is dbt-coves?\n==================\n\ndbt-coves is a complimentary CLI tool for `dbt <https://www.getdbt.com>`_ that allows users to quickly apply `Analytics Engineering <https://www.getdbt.com/what-is-analytics-engineering/>`_ best practices.\n\ndbt-coves helps with the generation of scaffold for dbt by analyzing your data warehouse schema in Redshift, Snowflake, or Big Query and creating the necessary configuration files (sql and yml).\n\n⚠️ **dbt-coves is in alpha version. Don’t use on your prod models unless you have tested it before.**\n\nHere\'s the tool in action\n-------------------------\n\n.. image:: https://cdn.loom.com/sessions/thumbnails/74062cf71cbe4898805ca508ea2d9455-1624905546029-with-play.gif\n   :target: https://www.loom.com/share/74062cf71cbe4898805ca508ea2d9455\n\nSupported dbt versions\n======================\n\n.. list-table::\n   :header-rows: 1\n\n   * - Version\n     - Status\n   * - 0.17.0\n     - ❌ Not supported\n   * - 0.18.x\n     - ✅ Tested\n   * - 0.19.x\n     - ✅ Tested\n   * - 0.20.x\n     - ✅ Tested\n   * - 0.21.x\n     - 🕥 In progress\n\nSupported adapters\n==================\n\n.. list-table::\n   :header-rows: 1\n\n   * - Feature\n     - Snowflake\n     - Redshift\n     - BigQuery\n     - Postgres\n   * - profile.yml generation\n     - ✅ Tested\n     - 🕥 In progress\n     - ❌ Not tested\n     - ❌ Not tested\n   * - sources generation\n     - ✅ Tested\n     - 🕥 In progress\n     - ❌ Not tested\n     - ❌ Not tested\n\nInstallation\n************\n\n.. code:: console\n\n   pip install dbt-coves\n\nWe recommend using `python virtualenvs\n<https://docs.python.org/3/tutorial/venv.html>`_ and create one\nseparate environment per project.\n\n⚠️ **if you have dbt < 0.18.0 installed, dbt-coves will automatically\nupgrade dbt to the latest version**\n\n\nMain Features\n*************\n\n\nProject initialization\n======================\n\n.. code:: console\n\n   dbt-coves init\n\nInitializes a new ready-to-use dbt project that includes recommended\nintegrations such as `sqlfluff\n<https://github.com/sqlfluff/sqlfluff>`_, `pre-commit\n<https://pre-commit.com/>`_, dbt packages, among others.\n\nUses a `cookiecutter <https://github.com/datacoves/cookiecutter-dbt>`_\ntemplate to make it easier to maintain.\n\n\nModels generation\n=================\n\n.. code:: console\n\n   dbt-coves generate <resource>\n\nWhere *<resource>* could be *sources*.\n\nCode generation tool to easily generate models and model properties\nbased on configuration and existing data.\n\nSupports `Jinja <https://jinja.palletsprojects.com/>`_ templates to\nadjust how the resources are generated.\n\n\nQuality Assurance\n=================\n\n.. code:: console\n\n   dbt-coves check\n\nRuns a set of checks in your local environment to ensure high code\nquality.\n\nChecks can be extended by implementing `pre-commit hooks\n<https://pre-commit.com/#creating-new-hooks>`_.\n\n\nEnvironment setup\n=================\n\n.. code:: console\n\n   dbt-coves setup\n\nRuns a set of checks in your local environment and helps you configure\nit properly: ssh key, git, dbt profiles.yml, vscode extensions.\n\n\nSettings\n********\n\nDbt-coves could optionally read settings from ``.dbt_coves.yml`` or\n``.dbt_coves/config.yml``. A standard settings files could looke like\nthis:\n\n.. code:: yaml\n\n   generate:\n     sources:\n       schemas:\n         - RAW\n       destination: "models/sources/{{ schema }}/{{ relation }}.sql"\n       model_props_strategy: one_file_per_model\n       templates_folder: ".dbt_coves/templates"\n\nIn this example options for the ``generate`` command are provided:\n\n``schemas``: List of schema names where to look for source tables\n\n``destination``: Path to generated model, where ``schema`` represents\nthe lowercased schema and ``relation`` the lowercased table name.\n\n``model_props_strategy``: Defines how dbt-coves generates model\nproperties files, currently just ``one_file_per_model`` is available,\ncreates one yaml file per model.\n\n``templates_folder``: Folder where source generation jinja templates\nare located.\n\n\nOverride source generation templates\n====================================\n\nCustomizing generated models and model properties requires placing\nspecific files under the ``templates_folder`` folder like these:\n\n\nsource_model.sql\n----------------\n\n.. code:: sql\n\n   with raw_source as (\n\n       select * from {% raw %}{{{% endraw %} source(\'{{ relation.schema.lower() }}\', \'{{ relation.name.lower() }}\') {% raw %}}}{% endraw %}\n\n   ),\n\n   final as (\n\n       select\n   {%- if adapter_name == \'SnowflakeAdapter\' %}\n   {%- for key, cols in nested.items() %}\n     {%- for col in cols %}\n           {{ key }}:{{ \'"\' + col + \'"\' }}::varchar as {{ col.lower().replace(" ","_").replace(":","_").replace("(","_").replace(")","_") }}{% if not loop.last or columns %},{% endif %}\n     {%- endfor %}\n   {%- endfor %}\n   {%- elif adapter_name == \'BigQueryAdapter\' %}\n   {%- for key, cols in nested.items() %}\n     {%- for col in cols %}\n           cast({{ key }}.{{ col.lower() }} as string) as {{ col.lower().replace(" ","_").replace(":","_").replace("(","_").replace(")","_") }}{% if not loop.last or columns %},{% endif %}\n     {%- endfor %}\n   {%- endfor %}\n   {%- elif adapter_name == \'RedshiftAdapter\' %}\n   {%- for key, cols in nested.items() %}\n     {%- for col in cols %}\n           {{ key }}.{{ col.lower() }}::varchar as {{ col.lower().replace(" ","_").replace(":","_").replace("(","_").replace(")","_") }}{% if not loop.last or columns %},{% endif %}\n     {%- endfor %}\n   {%- endfor %}\n   {%- endif %}\n   {%- for col in columns %}\n           {{ \'"\' + col.name.lower() + \'"\' }} as {{ col.name.lower() }}{% if not loop.last %},{% endif %}\n   {%- endfor %}\n\n       from raw_source\n\n   )\n\n   select * from final\n\n\nsource_model_props.yml\n----------------------\n\n.. code:: yaml\n\n   version: 2\n\n   sources:\n     - name: {{ relation.schema.lower() }}\n   {%- if source_database %}\n       database: {{ source_database }}\n   {%- endif %}\n       schema: {{ relation.schema.lower() }}\n       tables:\n         - name: {{ relation.name.lower() }}\n           identifier: {{ relation.name }}\n\n   models:\n     - name: {{ model.lower() }}\n       columns:\n   {%- for cols in nested.values() %}\n     {%- for col in cols %}\n         - name: {{ col.lower().replace(" ","_").replace(":","_").replace("(","_").replace(")","_") }}\n     {%- endfor %}\n   {%- endfor %}\n   {%- for col in columns %}\n         - name: {{ col.name.lower() }}\n   {%- endfor %}\n\n\nCLI Detailed Reference\n**********************\n\nCLI tool for dbt users applying analytics engineering best practices.\n\n::\n\n   usage: dbt_coves [-h] [-v] {init,generate,check,fix,setup} ...\n\n\nNamed Arguments\n===============\n\n-v, --version\n\nshow program’s version number and exit\n\n\ndbt-coves commands\n==================\n\ntask\n\nPossible choices: init, generate, check, fix, setup\n\n\nSub-commands:\n=============\n\n\ninit\n----\n\nInitializes a new dbt project using predefined conventions.\n\n::\n\n   dbt_coves init [-h] [--log-level LOG_LEVEL] [-vv] [--config-path CONFIG_PATH] [--project-dir PROJECT_DIR] [--profiles-dir PROFILES_DIR] [--profile PROFILE] [-t TARGET] [--vars VARS] [--template TEMPLATE] [--current-dir]\n\n\nNamed Arguments\n~~~~~~~~~~~~~~~\n\n--log-level\n\noverrides default log level\n\nDefault: “”\n\n-vv, --verbose\n\nWhen provided the length of the tracebacks will not be truncated.\n\nDefault: False\n\n--config-path\n\nFull path to .dbt_coves.yml file if not using default. Default is\ncurrent working directory.\n\n--project-dir\n\nWhich directory to look in for the dbt_project.yml file. Default is\nthe current working directory and its parents.\n\n--profiles-dir\n\nWhich directory to look in for the profiles.yml file.\n\nDefault: “~/.dbt”\n\n--profile\n\nWhich profile to load. Overrides setting in dbt_project.yml.\n\n-t, --target\n\nWhich target to load for the given profile\n\n--vars\n\nSupply variables to your dbt_project.yml file. This argument should be\na YAML string, eg. ‘{my_variable: my_value}’\n\nDefault: “{}”\n\n--template\n\nCookiecutter template github url, i.e.\n‘https://github.com/datacoves/cookiecutter-dbt-coves.git’\n\n--current-dir\n\nGenerate the dbt project in the current directory.\n\nDefault: False\n\n\ngenerate\n--------\n\nGenerates sources and models with defaults.\n\n::\n\n   dbt_coves generate [-h] [--log-level LOG_LEVEL] [-vv] [--config-path CONFIG_PATH] [--project-dir PROJECT_DIR] [--profiles-dir PROFILES_DIR] [--profile PROFILE] [-t TARGET] [--vars VARS] {sources} ...\n\n\nNamed Arguments\n~~~~~~~~~~~~~~~\n\n--log-level\n\noverrides default log level\n\nDefault: “”\n\n-vv, --verbose\n\nWhen provided the length of the tracebacks will not be truncated.\n\nDefault: False\n\n--config-path\n\nFull path to .dbt_coves.yml file if not using default. Default is\ncurrent working directory.\n\n--project-dir\n\nWhich directory to look in for the dbt_project.yml file. Default is\nthe current working directory and its parents.\n\n--profiles-dir\n\nWhich directory to look in for the profiles.yml file.\n\nDefault: “~/.dbt”\n\n--profile\n\nWhich profile to load. Overrides setting in dbt_project.yml.\n\n-t, --target\n\nWhich target to load for the given profile\n\n--vars\n\nSupply variables to your dbt_project.yml file. This argument should be\na YAML string, eg. ‘{my_variable: my_value}’\n\nDefault: “{}”\n\n\ndbt-coves generate commands\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\ntask\n\nPossible choices: sources\n\n\nSub-commands:\n~~~~~~~~~~~~~\n\n\nsources\n"""""""\n\nGenerate source dbt models by inspecting the database schemas and\nrelations.\n\n::\n\n   dbt_coves generate sources [-h] [--log-level LOG_LEVEL] [-vv] [--config-path CONFIG_PATH] [--project-dir PROJECT_DIR] [--profiles-dir PROFILES_DIR] [--profile PROFILE] [-t TARGET] [--vars VARS] [--database DATABASE]\n                              [--schemas SCHEMAS] [--relations RELATIONS] [--destination DESTINATION] [--model_props_strategy MODEL_PROPS_STRATEGY] [--templates_folder TEMPLATES_FOLDER]\n\n\nNamed Arguments\n+++++++++++++++\n\n--log-level\n\noverrides default log level\n\nDefault: “”\n\n-vv, --verbose\n\nWhen provided the length of the tracebacks will not be truncated.\n\nDefault: False\n\n--config-path\n\nFull path to .dbt_coves.yml file if not using default. Default is\ncurrent working directory.\n\n--project-dir\n\nWhich directory to look in for the dbt_project.yml file. Default is\nthe current working directory and its parents.\n\n--profiles-dir\n\nWhich directory to look in for the profiles.yml file.\n\nDefault: “~/.dbt”\n\n--profile\n\nWhich profile to load. Overrides setting in dbt_project.yml.\n\n-t, --target\n\nWhich target to load for the given profile\n\n--vars\n\nSupply variables to your dbt_project.yml file. This argument should be\na YAML string, eg. ‘{my_variable: my_value}’\n\nDefault: “{}”\n\n--database\n\nDatabase where source relations live, if different than target\n\n--schemas\n\nComma separated list of schemas where raw data resides, i.e.\n‘RAW_SALESFORCE,RAW_HUBSPOT’\n\n--relations\n\nComma separated list of relations where raw data resides, i.e.\n‘RAW_HUBSPOT_PRODUCTS,RAW_SALESFORCE_USERS’\n\n--destination\n\nWhere models sql files will be generated, i.e.\n‘models/{schema_name}/{relation_name}.sql’\n\n--model_props_strategy\n\nStrategy for model properties files generation, i.e.\n‘one_file_per_model’\n\n--templates_folder\n\nFolder with jinja templates that override default sources generation\ntemplates, i.e. ‘templates’\n\n\ncheck\n-----\n\nRuns pre-commit hooks and linters.\n\n::\n\n   dbt_coves check [-h] [--log-level LOG_LEVEL] [-vv] [--config-path CONFIG_PATH] [--project-dir PROJECT_DIR] [--profiles-dir PROFILES_DIR] [--profile PROFILE] [-t TARGET] [--vars VARS] [--no-fix]\n\n\nNamed Arguments\n~~~~~~~~~~~~~~~\n\n--log-level\n\noverrides default log level\n\nDefault: “”\n\n-vv, --verbose\n\nWhen provided the length of the tracebacks will not be truncated.\n\nDefault: False\n\n--config-path\n\nFull path to .dbt_coves.yml file if not using default. Default is\ncurrent working directory.\n\n--project-dir\n\nWhich directory to look in for the dbt_project.yml file. Default is\nthe current working directory and its parents.\n\n--profiles-dir\n\nWhich directory to look in for the profiles.yml file.\n\nDefault: “~/.dbt”\n\n--profile\n\nWhich profile to load. Overrides setting in dbt_project.yml.\n\n-t, --target\n\nWhich target to load for the given profile\n\n--vars\n\nSupply variables to your dbt_project.yml file. This argument should be\na YAML string, eg. ‘{my_variable: my_value}’\n\nDefault: “{}”\n\n--no-fix\n\nDo not suggest auto-fixing linting errors. Useful when running this\ncommand on CI jobs.\n\nDefault: False\n\n\nfix\n---\n\nRuns linter fixes.\n\n::\n\n   dbt_coves fix [-h] [--log-level LOG_LEVEL] [-vv] [--config-path CONFIG_PATH] [--project-dir PROJECT_DIR] [--profiles-dir PROFILES_DIR] [--profile PROFILE] [-t TARGET] [--vars VARS]\n\n\nNamed Arguments\n~~~~~~~~~~~~~~~\n\n--log-level\n\noverrides default log level\n\nDefault: “”\n\n-vv, --verbose\n\nWhen provided the length of the tracebacks will not be truncated.\n\nDefault: False\n\n--config-path\n\nFull path to .dbt_coves.yml file if not using default. Default is\ncurrent working directory.\n\n--project-dir\n\nWhich directory to look in for the dbt_project.yml file. Default is\nthe current working directory and its parents.\n\n--profiles-dir\n\nWhich directory to look in for the profiles.yml file.\n\nDefault: “~/.dbt”\n\n--profile\n\nWhich profile to load. Overrides setting in dbt_project.yml.\n\n-t, --target\n\nWhich target to load for the given profile\n\n--vars\n\nSupply variables to your dbt_project.yml file. This argument should be\na YAML string, eg. ‘{my_variable: my_value}’\n\nDefault: “{}”\n\n\nsetup\n-----\n\nSets up SSH keys, git repo, and db connections.\n\n::\n\n   dbt_coves setup [-h] [--log-level LOG_LEVEL] [-vv] [--config-path CONFIG_PATH] [--project-dir PROJECT_DIR] [--profiles-dir PROFILES_DIR] [--profile PROFILE] [-t TARGET] [--vars VARS]\n\n\nNamed Arguments\n~~~~~~~~~~~~~~~\n\n--log-level\n\noverrides default log level\n\nDefault: “”\n\n-vv, --verbose\n\nWhen provided the length of the tracebacks will not be truncated.\n\nDefault: False\n\n--config-path\n\nFull path to .dbt_coves.yml file if not using default. Default is\ncurrent working directory.\n\n--project-dir\n\nWhich directory to look in for the dbt_project.yml file. Default is\nthe current working directory and its parents.\n\n--profiles-dir\n\nWhich directory to look in for the profiles.yml file.\n\nDefault: “~/.dbt”\n\n--profile\n\nWhich profile to load. Overrides setting in dbt_project.yml.\n\n-t, --target\n\nWhich target to load for the given profile\n\n--vars\n\nSupply variables to your dbt_project.yml file. This argument should be\na YAML string, eg. ‘{my_variable: my_value}’\n\nDefault: “{}”\n\nSelect one of the available sub-commands with –help to find out more\nabout them.\n\n\nThanks\n******\n\nThe project main structure was inspired by `dbt-sugar\n<https://github.com/bitpicky/dbt-sugar>`_. Special thanks to `Bastien\nBoutonnet <https://github.com/bastienboutonnet>`_ for the great work\ndone.\n\n\nAuthors\n*******\n\n*  Sebastian Sassi `@sebasuy <https://twitter.com/sebasuy>`_ –\n   `Convexa <https://convexa.ai>`_\n\n*  Noel Gomez `@noel_g <https://twitter.com/noel_g>`_ – `Ninecoves\n   <https://ninecoves.com>`_\n\n\nAbout\n*****\n\nLearn more about `Datacoves <https://datacoves.com>`_.\n',
    'author': 'Datacoves',
    'author_email': 'hello@datacoves.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://datacoves.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
