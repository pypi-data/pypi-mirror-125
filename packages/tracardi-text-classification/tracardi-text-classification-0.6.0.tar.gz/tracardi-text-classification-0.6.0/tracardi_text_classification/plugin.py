import aiohttp
from tracardi.service.storage.driver import storage
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.domain.result import Result
from tracardi_text_classification.model.configuration import Configuration
from tracardi_text_classification.model.ml_source_onfiguration import MLSourceConfiguration
from tracardi_dot_notation.dot_template import DotTemplate


def validate(config: dict) -> Configuration:
    return Configuration(**config)


class TextClassificationAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'TextClassificationAction':
        config = validate(kwargs)
        source = await storage.driver.resource.load(config.source.id)
        source = MLSourceConfiguration(**source.config)
        return TextClassificationAction(config, source)

    def __init__(self, config: Configuration, source: MLSourceConfiguration):
        self.source = source
        self.config = config
        self.models = {
            'social': 'SocialMedia',
            'press': 'IPTC'
        }

    async def run(self, payload):

        if self.config.model not in self.models:
            raise ValueError(f"Model `{self.config.model}` is incorrect. Available models are `{self.models}`")

        dot = self._get_dot_accessor(payload)
        template = DotTemplate()
        async with aiohttp.ClientSession() as session:
            params = {
                "key": self.source.token,
                "txt": template.render(self.config.text, dot),
                "model": "{}_{}".format(self.models[self.config.model], self.config.language)
            }

            if self.config.has_title():
                params['title'] = dot[self.config.title]

            try:
                async with session.post('https://api.meaningcloud.com/class-2.0', params=params) as response:
                    if response.status != 200:
                        raise ConnectionError("Could not connect to service https://api.meaningcloud.com. "
                                              f"It returned `{response.status}` status.")

                    data = await response.json()
                    if 'status' in data and 'msg' in data['status']:
                        if data['status']['msg'] != "OK":
                            raise ValueError(data['status']['msg'])

                    result = {
                        "categories": data['category_list'],
                    }

                    return Result(port="payload", value=result), Result(port="error", value=None)

            except Exception as e:
                self.console.error(repr(e))
                return Result(port="payload", value=None), Result(port="error", value=str(e))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_text_classification.plugin',
            className='TextClassificationAction',
            inputs=["payload"],
            outputs=['payload', 'error'],
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            manual="text_classification_action",
            init={
                "source": {
                    "id": None
                },
                "language": "en",
                "model": "social",
                "title": None,
                "text": None
            },
            form=Form(groups=[
                FormGroup(
                    name="Text classification resource",
                    fields=[
                        FormField(
                            id="source",
                            name="MeaningCloud resource",
                            description="Select MeaningCloud resource. Authentication credentials will be used to "
                                        "connect to MeaningCloud server.",
                            component=FormComponent(
                                type="resource",
                                props={"label": "resource"})
                        )
                    ]
                ),
                FormGroup(
                    name="Text classification settings",
                    fields=[
                        FormField(
                            id="language",
                            name="Language",
                            description="Select language.",
                            component=FormComponent(type="select", props={
                                "label": "Language",
                                "items": {
                                    "en": "English",
                                    "sp": "Spanish",
                                    "fr": "French",
                                    "it": "Italian",
                                    "pt": "Portuguese",
                                    "ct": "Catalan"
                                }
                            })
                        ),
                        FormField(
                            id="model",
                            name="Model",
                            description="Select classification model. Reference the documentation for more details.",
                            component=FormComponent(type="select", props={
                                "label": "Model",
                                "items": {
                                    "press": "IPTC",
                                    "social": "Social Text"
                                }
                            })
                        ),
                        FormField(
                            id="text",
                            name="Text",
                            description="Type text to classify.",
                            component=FormComponent(type="textarea", props={"rows": 8})
                        ),
                        FormField(
                            id="title",
                            name="Title",
                            required=False,
                            description="This field is optional. Type title to make better classification.",
                            component=FormComponent(type="text", props={"label": "Title"})
                        )
                    ])
            ]),
        ),
        metadata=MetaData(
            name='Text classification',
            desc='It connects to the service that classifies a given sentence.',
            type='flowNode',
            width=200,
            height=100,
            icon='paragraph',
            group=["Machine learning"]
        )
    )
