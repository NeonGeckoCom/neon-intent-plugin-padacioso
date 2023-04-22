from ovos_plugin_manager.intents import IntentExtractor, IntentPriority, IntentDeterminationStrategy, IntentMatch

from padacioso import IntentContainer


class PadaciosoExtractor(IntentExtractor):

    def __init__(self, config=None,
                 strategy=IntentDeterminationStrategy.SEGMENT_REMAINDER,
                 priority=IntentPriority.HIGH,
                 segmenter=None):
        super().__init__(config, strategy=strategy,
                         priority=priority, segmenter=segmenter)
        self.engines = {}  # lang: IntentContainer

    def _get_engine(self, lang=None):
        lang = lang or self.lang
        if lang not in self.engines:
            self.engines[lang] = IntentContainer()
        return self.engines[lang]

    def detach_intent(self, intent_name):
        for intent in self.registered_intents:
            if intent.name == intent_name and intent.lang in self.engines:
                self.engines[intent.lang].remove_intent(intent_name)
        super().detach_intent(intent_name)

    def register_entity(self, entity_name, samples=None, lang=None):
        lang = lang or self.lang
        container = self._get_engine(lang)
        super().register_entity(entity_name, samples, lang)
        samples = samples or [entity_name]
        container.add_entity(entity_name, samples)

    def register_intent(self, intent_name, samples=None, lang=None):
        lang = lang or self.lang
        container = self._get_engine(lang)
        super().register_intent(intent_name, samples, lang)
        container.add_intent(intent_name, samples)

    def calc_intent(self, utterance, min_conf=0.5, lang=None, session=None):
        lang = lang or self.lang
        container = self._get_engine(lang)
        utterance = utterance.strip().lower()
        intent = container.calc_intent(utterance)
        if intent["name"]:
            for intent in self.registered_intents:
                if intent.name == intent["name"]:
                    remainder = intent.get_utterance_remainder(utterance)
                    break
            else:
                remainder = ""
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
            skill_id = self.get_intent_skill_id(intent["intent_type"])
            return IntentMatch(intent_service=intent["intent_engine"],
                               intent_type=intent["intent_type"],
                               intent_data=intent,
                               confidence=intent["conf"],
                               skill_id=skill_id)
        return None
