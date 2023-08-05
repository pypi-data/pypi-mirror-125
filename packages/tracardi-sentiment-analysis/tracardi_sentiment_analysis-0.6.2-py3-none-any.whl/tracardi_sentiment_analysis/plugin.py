import aiohttp
from tracardi.service.storage.driver import storage
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.domain.result import Result
from tracardi_sentiment_analysis.model.configuration import Configuration
from tracardi_sentiment_analysis.model.sa_source_onfiguration import SASourceConfiguration
from tracardi_dot_notation.dot_template import DotTemplate


def validate(config: dict) -> Configuration:
    return Configuration(**config)


class SentimentAnalysisAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'SentimentAnalysisAction':
        config = validate(kwargs)
        source = await storage.driver.resource.load(config.source.id)
        source = SASourceConfiguration(**source.config)

        return SentimentAnalysisAction(source, config)

    def __init__(self, source: SASourceConfiguration, config: Configuration):
        self.source = source
        self.config = config

    async def run(self, payload):
        dot = self._get_dot_accessor(payload)
        template = DotTemplate()
        async with aiohttp.ClientSession() as session:
            params = {
                "key": self.source.token,
                "lang": self.config.language,
                "txt": template.render(self.config.text, dot)
            }
            try:
                async with session.post('https://api.meaningcloud.com/sentiment-2.1', params=params) as response:
                    if response.status != 200:
                        raise ConnectionError("Could not connect to service https://api.meaningcloud.com. "
                                              f"It returned `{response.status}` status.")

                    data = await response.json()
                    if 'status' in data and 'msg' in data['status']:
                        if data['status']['msg'] != "OK":
                            raise ValueError(data['status']['msg'])

                    result = {
                        "sentiment": data['score_tag'],
                        "agreement": data['agreement'],
                        "subjectivity": data['subjectivity'],
                        "confidence": float(data['confidence'])
                    }

                    return Result(port="payload", value=result), Result(port="error", value=None)
            except Exception as e:
                self.console.error(repr(e))
                return Result(port="payload", value=None), Result(port="error", value=str(e))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_sentiment_analysis.plugin',
            className='SentimentAnalysisAction',
            inputs=["payload"],
            outputs=['payload', 'error'],
            version='0.6.2',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                },
                "language": "en",
                "text": None
            },
            form=Form(groups=[
                FormGroup(
                    name="Text sentiment resource",
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
                    name="Text sentiment settings",
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
                            id="text",
                            name="Text",
                            description="Type text to classify.",
                            component=FormComponent(type="textarea", props={"rows": 8})
                        )
                    ])
            ]),
        ),
        metadata=MetaData(
            name='Sentiment analysis',
            desc='It connects to the service that predicts sentiment from a given sentence.',
            type='flowNode',
            width=200,
            height=100,
            icon='paragraph',
            group=["Machine learning"]
        )
    )
