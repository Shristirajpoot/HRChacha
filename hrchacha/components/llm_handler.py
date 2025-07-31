import os
import sys

import streamlit as st
from dotenv import load_dotenv
from together import Together

from hrchacha.exceptions.exception import HRChachaException
from  hrchacha.logging.logger import logging
load_dotenv()

class LLM:
    def __init__(self):
        self.client = Together(api_key=st.secrets["TOGETHER_API_KEY"])


    def get_llama_response(self):
        """
        Stream response from LLaMA 3.3 70B via Together API.

        Args:
            messages (list): List of dicts [{"role": "user", "content": "Hi"}]

        Yields:
            str: Token stream
        """
        try:
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.4,
                top_p=0.9,
                repetition_penalty=1.1,
                presence_penalty=0.0,
                frequency_penalty=0.0,
            )

            return response

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))
            return None




