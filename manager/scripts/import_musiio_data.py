from dataclasses import dataclass
from enum import Enum
from typing import List

from manager.scripts.musiio_client import MusiioExtractionService


class TagType(Enum):
    content_type = "CONTENT TYPE"
    content_type_v2 = "CONTENT TYPE V2"
    use_case = "USE CASE"
    genre = "GENRE"
    genre_v3 = "GENRE V3"
    genre_v2 = "GENRE V2"
    mood = "MOOD"
    mood_secondary = "MOOD SECONDARY"
    mood_valence = "MOOD VALENCE"
    bpm = "BPM"
    bpm_alt = "BPM ALT"
    bpm_variation = "BPM VARIATION"
    key = "KEY"
    key_sharp = "KEY SHARP"
    key_sharp_secondary = "KEY SHARP SECONDARY"
    key_flat = "KEY FLAT"
    key_flat_secondary = "KEY FLAT SECONDARY"
    key_secondary = "KEY SECONDARY"
    energy = "ENERGY"
    energy_variation = "ENERGY VARIATION"
    instrumentation = "INSTRUMENTATION"
    genre_secondary = "GENRE SECONDARY"
    vocal_presence = "VOCAL PRESENCE"
    vocal_gender = "VOCAL GENDER"
    quality = "QUALITY"
    instrument = "INSTRUMENT"


@dataclass
class MusiioTag:
    type: TagType
    score: int
    name: str

    def as_dict(self):
        return {
            'type': self.type.value,
            'score': self.score,
            'name': self.name,
        }

    def __post_init__(self):
        self.type = TagType(self.type)


@dataclass
class MusiioTagsResponse:
    tags: List[MusiioTag]

    def __post_init__(self):
        self.tags = [MusiioTag(**tag) for tag in self.tags]


class ImportMusiioData:
    @staticmethod
    def run(youtube_id: str):
        response = MusiioExtractionService(f'https://www.youtube.com/watch?v={youtube_id}').get_tags()
        musiio_obj: MusiioTagsResponse = MusiioTagsResponse(tags=response)
        genre_v3_tags = []
        instrument_tags = []
        musiio_result_tags = {}
        for tag in musiio_obj.tags:
            if tag.type == TagType.genre_v3:
                genre_v3_tags.append(tag)
            elif tag.type == TagType.instrument:
                instrument_tags.append(tag)
            else:
                musiio_result_tags[tag.type.name] = tag.name
                musiio_result_tags[f'{tag.type.name}_score'] = tag.score

        for index, tag in enumerate(genre_v3_tags):
            musiio_result_tags[f'{tag.type.name}_{index+1}'] = tag.name
            musiio_result_tags[f'{tag.type.name}_{index+1}_score'] = tag.score

        for index, tag in enumerate(instrument_tags):
            musiio_result_tags[f'{tag.type.name}_{index+1}'] = tag.name
            musiio_result_tags[f'{tag.type.name}_{index+1}_score'] = tag.score
        return musiio_result_tags
