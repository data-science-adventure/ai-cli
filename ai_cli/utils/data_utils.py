from pathlib import Path
import shutil

import os
from typing import List


class DataUtils:

    @staticmethod
    def group_tokens_by_sentences(examples):
        """
        Processes a batch of tokens and returns a dictionary of lists,
        where each list contains data for all the sentences in the batch.
        """
        # Dictionary to store the grouped data for the entire batch
        grouped_data = {"id": [], "tokens": [], "ner_tags": []}

        # Get all unique sentence IDs in the batch
        sentence_ids = sorted(list(set(examples["sentence_id"])))

        for sid in sentence_ids:
            # Filter tokens belonging to the current sentence_id
            sentence_tokens = []
            sentence_ner_tags = []

            for i in range(len(examples["sentence_id"])):
                if examples["sentence_id"][i] == sid:
                    sentence_tokens.append(examples["tokens"][i])
                    sentence_ner_tags.append(examples["ner_tags"][i])

            # Append the completed sentence data to the lists
            grouped_data["id"].append(sid)
            grouped_data["tokens"].append(sentence_tokens)
            grouped_data["ner_tags"].append(sentence_ner_tags)

        # Return the dictionary of lists for the entire batch
        return grouped_data
