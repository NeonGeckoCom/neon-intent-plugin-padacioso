from ovos_plugin_manager.intents import IntentExtractor, IntentPriority, IntentDeterminationStrategy

from padacioso import IntentContainer


class PadaciosoExtractor(IntentExtractor):

    def __init__(self, config=None,
                 strategy=IntentDeterminationStrategy.SEGMENT_REMAINDER,
                 priority=IntentPriority.HIGH,
                 segmenter=None):
        super().__init__(config, strategy=strategy,
                         priority=priority, segmenter=segmenter)
        self.container = IntentContainer()

    def detach_intent(self, intent_name):
        super().detach_intent(intent_name)
        self.container.remove_intent(intent_name)

    def register_entity(self, entity_name, samples=None, lang=None):
        super().register_entity(entity_name, samples, lang)
        samples = samples or [entity_name]
        self.container.add_entity(entity_name, samples)

    def register_intent(self, intent_name, samples=None, lang=None):
        super().register_intent(intent_name, samples, lang)
        self.container.add_intent(intent_name, samples)

    def calc_intent(self, utterance, min_conf=0.5, lang=None):
        utterance = utterance.strip().lower()
        intent = self.container.calc_intent(utterance)
        if intent["name"]:
            remainder = self.get_utterance_remainder(
                utterance, samples=self.get_intent_samples(intent["name"], lang))
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
        return None
