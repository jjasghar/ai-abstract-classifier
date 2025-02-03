# pretalx-ai-validator

## Scope

This is an application that takes [AnythingLLM][anythingllm] and a selection of [abstracts][abstracts]
and asks a local LLM ([granite][granite] ideally) if the abstract has been written by an AI and/or
is a possible sales pitch.
It gives a file called `overview.csv` with a confidence score of up to `100` if it's been AI or
too "sales-y."

You can also inject a `csv` into this instead of reading the API. Take a look at [test_data/testing.csv](./test_data/testing.csv) as an example. Take a look at the `config.toml.example` for where to configure the `csv`.

**NOTE**: This is `,` seporated for the time being, so you'll need to remove all the `,` from the actual abstracts so it can be parsed correctly.

The sections that are needed the `csv` are as follows:
- code
- title
- abstract
- description

## Configuration

Everything is configured in the [config.toml](./config.toml.example) file, copy it to
the working directory and do something like the following:

First install AnythingLLM, [here](https://anythingllm.com/desktop), and configure it
with something along these lines of [this](https://ibm.github.io/opensource-ai-workshop/lab-3/).

Next run these following commands:

```bash
git clone git@github.com:jjasghar/pretalx-ai-validator.git
cd pretalx-ai-validator
python3.11 -m venv --upgrade-deps venv
source venv/bin/activate
pip install -r requirements.txt
cp config.toml.example config.toml
vim config.toml
python main.py
```

## Utils

There is a [jsons_to_markdown.py](./utils/jsons_to_markdown.py) to convert the [chat_primes](./chat_primes/jsons/) to readable format(s).

## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2025- IBM, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```



[anythingllm]: https://github.com/Mintplex-Labs/anything-llm
[abstracts]: https://talks.devopsdays.org/devopsdays-austin-2024/cfp
[granite]: http://ollama.com/library/granite3.1-dense
