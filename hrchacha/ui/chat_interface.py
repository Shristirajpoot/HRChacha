import sys
from typing import Optional, Callable

import streamlit as st

from hrchacha.components.chatbot import HRChacha
from hrchacha.constants import (
    BOT_ROLE,
    USER_ROLE, PAGE_CONFIG_MENU_ITEMS
)
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.logging.logger import logging
from hrchacha.prompts import SYSTEM_PROMPT, INITIAL_GREETING_MESSAGE, CHATBOT_REFERENCE_QUESTIONS
from hrchacha.utils.general_utils import get_random_chacha_thinking_line


class MainWindowUI:
    def __init__(self, title: str, response_callback: Optional[Callable] = None):

        self.title = title
        st.set_page_config(
            page_title=self.title,
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items=PAGE_CONFIG_MENU_ITEMS
        )

        self._initialize_state()
        self._render_ui()

    def _initialize_state(self):
        """Initializes session state variables for chatbot."""
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": BOT_ROLE, "content": SYSTEM_PROMPT},
                {"role": BOT_ROLE, "content": CHATBOT_REFERENCE_QUESTIONS},
                {"role": BOT_ROLE, "content": INITIAL_GREETING_MESSAGE}
            ]
            logging.info("Initialized session messages")

        if "user_data" not in st.session_state:
            st.session_state.user_data = ""
            logging.info("Initialized user data")

        if "bot" not in st.session_state:
            st.session_state.bot = HRChacha()
            logging.info("Initialized HRChacha bot")

    def _render_ui(self):
        """Render the chatbot UI."""
        try:
            st.set_page_config(page_title=self.title)
            st.markdown(self.title)
            self._display_all_messages()
        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))

    def _display_all_messages(self):
        """Displays all previous chat messages (except the system prompt)."""
        try:
            for message in st.session_state.messages:
                if message["role"] == BOT_ROLE and message["content"] == SYSTEM_PROMPT or message["content"] == CHATBOT_REFERENCE_QUESTIONS :
                    continue  # skip displaying raw system prompt
                avatar = "user" if message["role"] == USER_ROLE else "ai"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))

    def process_user_input(self, prompt: str):
        """Processes the user input and triggers the bot's response."""
        try:
            prompt = prompt.strip()
            if not prompt:
                return

            st.session_state.messages.append({
                "role": USER_ROLE,
                "content": prompt
            })

            with st.chat_message(USER_ROLE, avatar="user"):
                st.markdown(prompt)

            with st.chat_message(BOT_ROLE, avatar="ai"):

                thinking_placeholder = st.empty()
                thinking_placeholder.markdown(get_random_chacha_thinking_line())

                response_stream = st.session_state.bot.get_response_stream()

                thinking_placeholder.empty()
                st.session_state.bot.stream_and_capture_response(response_stream)

        except Exception as e:
            err = HRChachaException(e, sys)
            logging.error(str(err))