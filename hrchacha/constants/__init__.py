from pathlib import Path


USER_CHAT_INPUT_KEY = "ucik"

USER_ROLE = "user"
BOT_ROLE = "system"
PROJECT_ROOT = Path(__file__).parent.parent.parent

USER_DATA_PATTERN = r'USER_DATA\s*```json\s*([\s\S]*?)\s*```'

DB_NAME = "HRChacha"
COLLECTION_NAME = "CandidateData"


HR_CHACHA_THINKING_LINES = [
    "🧠 *HR Chacha is calling up his industry friends...*",
    "📞 *HR Chacha is pulling strings in his HR network...*",
    "💼 *HR Chacha is flipping through his big black recruitment diary...*",
    "🧐 *HR Chacha is adjusting his specs and reading your profile carefully...*",
    "📠 *HR Chacha is faxing your info to his corporate buddies...*",
    "📊 *HR Chacha is matching your skills with job listings he 'knows a guy' at...*",
    "🧳 *HR Chacha is rolling up his sleeves to get you placed...*",
    "☕ *HR Chacha just took a sip of chai and is deep in HR thought...*",
    "📚 *HR Chacha is brushing up on tech trends before responding...*",
    "🛠️ *HR Chacha is fixing something under the hood... probably a resume...*",
    "🔎 *HR Chacha is scanning your skills like a pro...*",
    "🔗 *HR Chacha is calling in favors from his LinkedIn gang...*",
    "🗂️ *HR Chacha is checking the dusty HR files...*",
    "📬 *HR Chacha is drafting a message to his cousin in Big Tech...*"
]

PAGE_CONFIG_MENU_ITEMS = {
                'Get Help': 'https://github.com/Phantom-VK/HRChacha',
                'Report a bug': 'https://github.com/Phantom-VK/HRChacha/issues',
                'About': 'HR Chacha - Your AI-powered HR assistant for career guidance and interview preparation.'
            }
