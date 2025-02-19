# ai-abstract-classifier

## Scope

This is an application that takes [AnythingLLM][anythingllm] and a selection of [abstracts][abstracts]
and asks a local LLM ([granite][granite] ideally) if the abstract has been written by an AI and/or
is a possible sales pitch.
It gives a file called `overview.csv` with a confidence score of up to `100` if it's been AI or
too "sales-y."

You can also inject a `csv` into this instead of reading an API, either [pretalx][pretalx] or [sessionize][sessionize] for the time being.

## CSV notes

Take a look at [test_data/testing.csv](./test_data/testing.csv) as an example. You run it via `python main.py -c CSV_FILE`, check `python main.py -h` for help.

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

**Note**: As of this release you will need to configure the model you want this to us via the
"default" AnythingLLM configuration. It seems for _now_ you can't programaticly change the workspace
for different models, so this is the work around.

Check out [testing_notes.md](./test_data/testing_notes.md) for some of the numbers ran with other
models on the same data.

Run these following commands:

```bash
git clone git@github.com:jjasghar/pretalx-ai-validator.git
cd pretalx-ai-validator
python3.11 -m venv --upgrade-deps venv
source venv/bin/activate
pip install -r requirements.txt
cp config.toml.example config.toml
vim config.toml
python main.py -h
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
[sessionize]: https://sessionize.com
[pretalx]: https://pretalx.com/p/about/
