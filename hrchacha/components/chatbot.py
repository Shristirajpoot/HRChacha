import json
import re
import sys

import streamlit as st

from hrchacha.components.data_handler import Database
from hrchacha.components.llm_handler import LLM
from hrchacha.constants import BOT_ROLE, USER_DATA_PATTERN
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging


class HRChacha:

    def __init__(self):
        self.message_history = st.session_state.messages

        if "llm" not in st.session_state:
            st.session_state.llm = LLM()

        if "database" not in st.session_state:
            st.session_state.database = Database()

        self.llm = st.session_state.llm
        self.db = st.session_state.database

    def get_response_stream(self):
        """
        Gets generator response from LLM.
        """
        try:
            return self.llm.get_llama_response()
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return None

    def _extract_user_info(self, corpus: str) -> str | None:
        """
        Extracts user data from the llm response and saves to
        database
        :param corpus: str llm response
        :return: str Extracted data
        """
        try:
            logging.info("Extracting user info from USER_DATA message...")

            match = re.search(USER_DATA_PATTERN, corpus, re.DOTALL)
            if not match:
                raise ValueError("No JSON object found in the message.")

            json_str = match.group(1)

            user_data = json.loads(json_str)
            user_data["session_chat"] = st.session_state.messages

            self.db.insert_user(user_data)

            logging.info("User data extracted successfully.")
            return user_data

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return None

    def stream_and_capture_response(self, response_generator):
        """
        Gets response from llm via provided generator and adds in current session messages.
        Checks for USER_DATA inside response and forwards to extract.
        :param response_generator: llm response generator
        :return: Nothing
        """
        try:
            logging.info("Streaming and capturing response...")


            full_response = ""


            def content_generator():
                nonlocal full_response
                for chunk in response_generator:
                    if hasattr(chunk, "choices"):
                        delta = chunk.choices[0].delta.content
                        if delta:
                            full_response += delta
                            yield delta


            st.write_stream(content_generator())


            st.session_state.messages.append({
                "role": BOT_ROLE,
                "content": full_response
            })


            if "USER_DATA" in full_response:
                extracted_result = self._extract_user_info(full_response)
                st.session_state.user_data = extracted_result
                print(st.session_state.user_data)

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))