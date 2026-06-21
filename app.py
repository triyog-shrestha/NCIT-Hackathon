import streamlit as st
from characters import CHARACTERS
from model_chat import Character
from sentiment_engine import SentimentAnalysis

st.set_page_config(page_title="Mindspace", page_icon="✶", layout="wide")

# ---------------------------------------------------------------------------
# Styling — dark, warm, Character.AI-ish. All CSS lives here, single file.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    .stApp {
        background: #0E0E10;
        color: #ECECEC;
    }

    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        color: #ECECEC !important;
    }

    .eyebrow {
        font-family: 'Montserrat', sans-serif;
        font-weight: 500;
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        color: #9C7BFF;
        text-transform: lowercase;
        margin-bottom: 6px;
    }

    /* ----------------------------------------------------------------- */
    /* Character picker — grid of cards                                  */
    /* ----------------------------------------------------------------- */

    /* Each card is a bordered vertical block. We turn the banner image
       into a background-image via a wrapper div injected just above it,
       and let Streamlit's own container supply the card chrome. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker) {
        background: #18181B;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px;
        overflow: hidden;
        transition: border-color 0.2s, transform 0.2s;
        margin-bottom: 0;
        padding: 0 !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker):hover {
        border-color: #9C7BFF !important;
        transform: translateY(-3px);
    }
    /* Kill the default inner padding Streamlit adds inside bordered
       containers so the banner image can run edge-to-edge. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker) > div {
        padding: 0 !important;
    }

    .card-banner {
        width: 100%;
        height: 120px;
        background-size: cover;
        background-position: center;
        background-color: #27272A;
        position: relative;
    }
    .card-banner.no-image {
        background-image: none !important;
    }

    .card-body {
        padding: 0 16px 16px;
        position: relative;
    }

    /* Avatar sits on top of the banner, overlapping into the body — same
       visual idea as the small circular avatar in the screenshot. */
    .card-avatar {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: #27272A;
        border: 2px solid #18181B;
        color: #ECECEC;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 1.3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        margin-top: -28px;
        margin-bottom: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    }
    .card-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .card-name {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        margin: 0 0 4px;
        line-height: 1.25;
    }

    .card-tagline {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        color: rgba(236, 236, 236, 0.6);
        margin: 0 0 12px;
        line-height: 1.35;
        min-height: 2.4em;
    }

    /* "Coming soon" placeholder card */
    .coming-soon-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        min-height: 200px;
        padding: 24px 16px;
    }
    .coming-soon-avatar {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.04);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        color: rgba(236, 236, 236, 0.5);
        font-size: 1.3rem;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    .coming-soon-label {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: rgba(236, 236, 236, 0.5);
        margin: 0;
    }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        background: transparent;
    }

    /* Buttons */
    .stButton button {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 100px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: #27272A !important;
        color: #ECECEC !important;
    }
    .stButton button:hover {
        border-color: #9C7BFF !important;
        color: #9C7BFF !important;
    }
    /* Buttons living inside a grid card need side padding since the
       card body itself has padding: 0 on the outer wrapper. */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker) .stButton {
        padding: 0 16px 16px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div.card-marker) .stButton button {
        width: 100%;
    }

    section[data-testid="stSidebar"] {
        background: #18181B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "active_character" not in st.session_state:
    st.session_state.active_character = None
if "character_instances" not in st.session_state:
    st.session_state.character_instances = {}
if "display_history" not in st.session_state:
    st.session_state.display_history = {}  # per-character list of {role, content} for rendering


@st.cache_resource
def get_sentiment_engine():
    """Load the sentiment model once per app process, not once per session —
    it's heavy, and every session re-loading it would be wasteful."""
    return SentimentAnalysis()


def get_character_instance(char_id):
    """Lazily create and cache a Character() per id so its .history persists
    across reruns within the session."""
    if char_id not in st.session_state.character_instances:
        st.session_state.character_instances[char_id] = Character(char_id)
        st.session_state.display_history[char_id] = []
    return st.session_state.character_instances[char_id]


def go_to_character(char_id):
    st.session_state.active_character = char_id
    st.rerun()


def go_home():
    st.session_state.active_character = None
    st.rerun()


def render_card_banner(char):
    """Top banner strip of a grid card. Uses `char['image']` as a cover
    background if present; otherwise a flat tinted strip so the layout
    still holds together for characters with no artwork yet."""
    image_src = char.get("image")
    if image_src:
        st.markdown(
            f'<div class="card-banner" style="background-image: url(\'{image_src}\');"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="card-banner no-image"></div>', unsafe_allow_html=True)


def render_card_avatar(char):
    """Small circular avatar overlapping the banner — falls back to the
    initial-letter circle when no dedicated avatar/image is set."""
    image_src = char.get("avatar") or char.get("image")
    if image_src:
        st.markdown(
            f'<div class="card-avatar"><img src="{image_src}" alt="{char["name"]}"></div>',
            unsafe_allow_html=True,
        )
    else:
        initial = char["name"][0].upper()
        st.markdown(f'<div class="card-avatar">{initial}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# View: Character select
# ---------------------------------------------------------------------------
def render_character_select():
    st.markdown('<p class="eyebrow">who do you want to talk to today?</p>', unsafe_allow_html=True)
    st.markdown("## Choose a voice")
    st.write("")

    char_ids = list(CHARACTERS.keys())

    if not char_ids:
        st.info(
            "No characters defined yet. Add some to `characters.py` — there's "
            "a template at the bottom of the file ready to fill in."
        )
        return

    # Grid: 4 cards per row, wrapping to new rows as needed, plus a
    # trailing "Coming soon" placeholder card.
    cards_per_row = 4
    all_items = char_ids + [None]  # None marks the "coming soon" slot

    for row_start in range(0, len(all_items), cards_per_row):
        row_items = all_items[row_start: row_start + cards_per_row]
        cols = st.columns(cards_per_row)

        for col, item in zip(cols, row_items):
            with col:
                if item is None:
                    with st.container(border=True):
                        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
                        st.markdown(
                            '<div class="coming-soon-card">'
                            '<div class="coming-soon-avatar">?</div>'
                            '<p class="coming-soon-label">Coming Soon...</p>'
                            '</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    char_id = item
                    char = CHARACTERS[char_id]
                    with st.container(border=True):
                        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
                        render_card_banner(char)
                        st.markdown('<div class="card-body">', unsafe_allow_html=True)
                        render_card_avatar(char)
                        st.markdown(f'<p class="card-name">{char["name"]}</p>', unsafe_allow_html=True)
                        tagline = char.get("tagline", "Tap to start a conversation")
                        st.markdown(f'<p class="card-tagline">{tagline}</p>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        if st.button("Start chat →", key=f"select_{char_id}", use_container_width=True):
                            go_to_character(char_id)


# ---------------------------------------------------------------------------
# View: Chat
# ---------------------------------------------------------------------------
def render_chat(char_id):
    char_data = CHARACTERS[char_id]
    character = get_character_instance(char_id)
    sentiment = get_sentiment_engine()

    # The character's own avatar/image, used as the chat-bubble icon for
    # every assistant message below (falls back to Streamlit's default
    # bot icon if neither field is set on this character).
    assistant_avatar = char_data.get("avatar") or char_data.get("image")

    header_col1, header_col2 = st.columns([1, 8])
    with header_col1:
        if st.button("← back"):
            go_home()
    with header_col2:
        st.markdown(f"### {char_data['name']}")

    st.divider()

    history = st.session_state.display_history[char_id]

    for msg in history:
        avatar = assistant_avatar if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    user_input = st.chat_input(f"Message {char_data['name']}...")

    if user_input:
        history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Track sentiment for this message. This never blocks or fails the
        # chat reply — a logging issue shouldn't break the conversation.
        try:
            sentiment.polarity_scores(user_input, character_id=char_id)
        except Exception as e:
            st.caption(f"(sentiment logging skipped: {e})")

        with st.chat_message("assistant", avatar=assistant_avatar):
            try:
                full_reply = character.chat(user_input)
                st.markdown(full_reply)
            except Exception as e:
                full_reply = None
                st.error(
                    f"Couldn't reach the model: {e}\n\n"
                    f"Check that Ollama is running and that the model "
                    f"`{character.model}` has been pulled (`ollama pull {character.model}`)."
                )

        if full_reply is not None:
            history.append({"role": "assistant", "content": full_reply})


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if st.session_state.active_character is None:
    render_character_select()
else:
    render_chat(st.session_state.active_character)