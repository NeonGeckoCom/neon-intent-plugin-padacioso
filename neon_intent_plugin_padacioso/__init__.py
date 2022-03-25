from ovos_plugin_manager.templates.intents import IntentExtractor

from padacioso import IntentContainer


class PadaciosoExtractor(IntentExtractor):
    keyword_based = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = IntentContainer()

    def detach_intent(self, intent_name):
        super().detach_intent(intent_name)
        self.container.remove_intent(intent_name)

    def register_entity(self, entity_name, samples=None):
        super().register_entity(entity_name, samples)
        samples = samples or [entity_name]
        self.container.add_entity(entity_name, samples)

    def register_intent(self, intent_name, samples=None):
        super().register_intent(intent_name, samples)
        self.container.add_intent(intent_name, samples)

    def calc_intent(self, utterance, min_conf=0.5):
        utterance = utterance.strip().lower()
        intent = self.container.calc_intent(utterance)
        if intent["name"]:
            remainder = self.get_utterance_remainder(
                utterance, samples=self.intent_samples[intent["name"]])
            intent["intent_engine"] = "padacioso"
            intent["intent_type"] = intent.pop("name")
            intent["utterance"] = utterance
            intent["utterance_remainder"] = remainder
            entity_text = "".join(v for v in intent["entities"].values())
            if len(intent["entities"]):
                ratio = len(entity_text) / len(utterance) / len(intent["entities"])
            else:
                ratio = len(entity_text) / len(utterance)
            ratio += 0.01
            ratio = ratio / len(self.segmenter.segment(utterance))
            intent["conf"] = 1 - ratio
            return intent
        return {'conf': 0,
                'intent_type': 'unknown',
                'entities': {},
                'utterance': utterance,
                'utterance_remainder': utterance,
                'intent_engine': 'padacioso'}