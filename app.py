import streamlit as st
import pandas as pd
from io import BytesIO
import time

# ------------------------------
# Page configuration
# ------------------------------
st.set_page_config(
    page_title="Galentine's Potluck",
    page_icon="🥂",
    layout="centered",
)

# ------------------------------
# Custom CSS for refined aesthetic
# ------------------------------
st.markdown(
    """
    <style>
    /* Overall background and typography */
    .stApp {
        background-color: #FFF0F5;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    h1, h2, h3 {
        font-weight: 300;
        letter-spacing: 0.5px;
        color: #800020;
    }
    /* Soft card containers - no decorative borders */
    .category-card {
        background-color: white;
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(128, 0, 32, 0.05);
        border: 1px solid rgba(128, 0, 32, 0.1);
        transition: box-shadow 0.2s ease;
    }
    .category-card:hover {
        box-shadow: 0 12px 28px rgba(128, 0, 32, 0.08);
    }
    /* Category title */
    .category-title {
        font-size: 1.8rem;
        font-weight: 350;
        margin-bottom: 1.5rem;
        color: #9F2B68;
        border-bottom: 1px solid #F8C8DC;
        padding-bottom: 0.5rem;
    }
    /* Item rows */
    .item-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0;
        border-bottom: 1px solid #E5E7EB;
    }
    .item-name {
        font-size: 1.1rem;
        color: #2D2D2D;
    }
    .claimed-by {
        font-size: 0.9rem;
        color: #9F2B68;
        font-style: italic;
    }
    .available {
        font-size: 0.9rem;
        color: #800020;
        opacity: 0.7;
    }
    /* Buttons */
    .stButton button {
        border-radius: 40px;
        border: 1px solid #F8C8DC;
        background-color: white;
        color: #800020;
        font-weight: 300;
        transition: all 0.2s;
        padding: 0.2rem 1.2rem;
        font-size: 0.9rem;
    }
    .stButton button:hover {
        border-color: #9F2B68;
        background-color: #FFF0F5;
        color: #9F2B68;
    }
    .stButton button:disabled {
        opacity: 0.5;
        border-color: #E5E7EB;
    }
    /* Input fields */
    .stTextInput input {
        border-radius: 40px;
        border: 1px solid #F8C8DC;
        background-color: white;
        padding: 0.5rem 1rem;
    }
    .stTextInput input:focus {
        border-color: #9F2B68;
        box-shadow: 0 0 0 1px #9F2B68;
    }
    /* Export button special */
    .export-button button {
        background-color: #800020;
        color: white;
        border: none;
    }
    .export-button button:hover {
        background-color: #9F2B68;
        color: white;
    }
    /* Name input message */
    .hint-message {
        color: #800020;
        font-style: italic;
        margin: 0.5rem 0 1.5rem 0;
        opacity: 0.7;
    }
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #F8C8DC;
    }
    /* Loading animation */
    .loading-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #FFF0F5;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        transition: opacity 1s ease;
        pointer-events: none;
    }
    .loading-content {
        text-align: center;
    }
    .loading-heart {
        font-size: 3rem;
        color: #800020;
        animation: pulse 1.5s ease-in-out infinite;
    }
    .loading-text {
        color: #9F2B68;
        font-size: 1.2rem;
        margin-top: 1rem;
        font-style: italic;
        letter-spacing: 1px;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    .fade-out {
        opacity: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Initialize session state with empty lists
# ------------------------------
if "potluck_items" not in st.session_state:
    st.session_state.potluck_items = []  # Start with empty list - no pre-populated items
    
if "name" not in st.session_state:
    st.session_state.name = ""

# ------------------------------
# Loading animation (appears once on first load)
# ------------------------------
if "loading_complete" not in st.session_state:
    st.session_state.loading_complete = False
    
    # Create loading placeholder
    loading_placeholder = st.empty()
    
    with loading_placeholder.container():
        st.markdown(
            """
            <div class="loading-container" id="loading-container">
                <div class="loading-content">
                    <div class="loading-heart">🥂</div>
                    <div class="loading-text">gathering the galentines...</div>
                </div>
            </div>
            <script>
                setTimeout(function() {
                    var container = document.getElementById('loading-container');
                    if (container) {
                        container.classList.add('fade-out');
                        setTimeout(function() {
                            container.style.display = 'none';
                        }, 1000);
                    }
                }, 1500);
            </script>
            """,
            unsafe_allow_html=True
        )
    
    # Small delay to show animation
    time.sleep(0.5)
    st.session_state.loading_complete = True
    loading_placeholder.empty()

# ------------------------------
# Helper functions
# ------------------------------
def get_items_for_category(category):
    return [item for item in st.session_state.potluck_items if item["category"] == category]

def is_duplicate(new_name, exclude_item=None):
    """Case‑insensitive duplicate check across all items."""
    new_lower = new_name.lower()
    for item in st.session_state.potluck_items:
        if exclude_item and item == exclude_item:
            continue
        if item["name"].lower() == new_lower:
            return True
    return False

def add_item(category, item_name):
    if not item_name or not item_name.strip():
        st.error("Please enter an item name.")
        return
    if is_duplicate(item_name):
        st.error(f"“{item_name}” is already on the list.")
        return
    st.session_state.potluck_items.append(
        {"name": item_name.strip(), "category": category, "claimed_by": None}
    )
    # Clear input field
    st.session_state[f"new_item_{category}"] = ""

def claim_item(item, claimer):
    claimer = claimer.strip() if claimer else None
    if claimer and item["claimed_by"] is None:
        item["claimed_by"] = claimer

def unclaim_item(item, claimer):
    claimer = claimer.strip() if claimer else None
    if claimer and item["claimed_by"] == claimer:
        item["claimed_by"] = None

# ------------------------------
# Name input (always on top)
# ------------------------------
st.markdown("<h1 style='font-weight: 300;'>🥂 Galentine's Potluck</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #9F2B68; margin-top: -0.5rem;'>who’s bringing what</p>", unsafe_allow_html=True)

# Create the text input widget
st.text_input(
    "Your name",
    key="name",
    placeholder="Enter your name to continue",
    help="Please enter your name to start adding or claiming items",
)

# Get the current name value (trimmed) for logic
current_name = st.session_state.name.strip() if st.session_state.name else ""

if not current_name:
    st.markdown('<p class="hint-message">✨ Please enter your name to continue ✨</p>', unsafe_allow_html=True)

# ------------------------------
# Categories definition
# ------------------------------
categories = ["Snacks", "Main Dishes", "Beverages", "Alcohol", "Desserts"]

# ------------------------------
# Render each category as a card
# ------------------------------
for category in categories:
    with st.container():
        # Wrap in a div with class 'category-card' using st.markdown
        st.markdown(f'<div class="category-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="category-title">{category}</div>', unsafe_allow_html=True)

        items_in_cat = get_items_for_category(category)

        if not items_in_cat:
            st.markdown("<p style='color: #800020; opacity: 0.5; font-style: italic; margin-bottom: 1rem;'>No items yet. Add something below ✨</p>", unsafe_allow_html=True)
        else:
            for item in items_in_cat:
                cols = st.columns([3, 2, 1])
                with cols[0]:
                    st.markdown(f'<span class="item-name">{item["name"]}</span>', unsafe_allow_html=True)
                with cols[1]:
                    if item["claimed_by"]:
                        st.markdown(f'<span class="claimed-by">✨ {item["claimed_by"]}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="available">Available</span>', unsafe_allow_html=True)
                with cols[2]:
                    if item["claimed_by"] is None:
                        # Claim button
                        st.button(
                            "Claim",
                            key=f"claim_{category}_{item['name']}_{id(item)}",
                            on_click=claim_item,
                            args=(item, st.session_state.name),
                            disabled=not current_name,
                        )
                    elif item["claimed_by"] == current_name:
                        # Unclaim button (only for current user)
                        st.button(
                            "Unclaim",
                            key=f"unclaim_{category}_{item['name']}_{id(item)}",
                            on_click=unclaim_item,
                            args=(item, st.session_state.name),
                            disabled=not current_name,
                        )
                    else:
                        # Claimed by someone else – no button
                        st.markdown("")

        # Add new item row
        st.markdown("<hr style='margin: 1rem 0;' />", unsafe_allow_html=True)
        col_input, col_button = st.columns([4, 1])
        with col_input:
            st.text_input(
                "New item",
                key=f"new_item_{category}",
                placeholder="e.g., Chocolate strawberries",
                label_visibility="collapsed",
                disabled=not current_name,
            )
        with col_button:
            st.button(
                "Add",
                key=f"add_btn_{category}",
                on_click=add_item,
                args=(category, st.session_state[f"new_item_{category}"]),
                disabled=not current_name,
            )

        st.markdown('</div>', unsafe_allow_html=True)  # close category-card

# ------------------------------
# Export to Excel
# ------------------------------
if st.session_state.potluck_items:  # Only show export if there are items
    st.markdown("<hr />", unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.potluck_items)
    df["Status"] = df["claimed_by"].apply(lambda x: "Claimed" if x else "Available")
    df = df.rename(columns={"name": "Item Name", "category": "Category", "claimed_by": "Claimed By"})
    df = df[["Item Name", "Category", "Claimed By", "Status"]]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Potluck")
    output.seek(0)

    st.download_button(
        label="📄 Export to Excel",
        data=output,
        file_name="galentine_potluck.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="export",
        help="Download the current list as an Excel file",
    )
