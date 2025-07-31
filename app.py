import sys

import streamlit as st

from hrchacha.constants import USER_CHAT_INPUT_KEY
from hrchacha.exceptions.exception import HRChachaException
from hrchacha.ui.chat_interface import MainWindowUI

if __name__ == "__main__":
    try:
        main_app = MainWindowUI(
                title="👴 HRChacha – Your Tech Job Uncle"
            )

        if prompt := st.chat_input("What's up?", key=USER_CHAT_INPUT_KEY):
                main_app.process_user_input(prompt)
    except Exception as e:
        raise HRChachaException(e, sys)