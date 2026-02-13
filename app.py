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
    initial_sidebar_state="collapsed",
)

# ------------------------------
# Custom CSS - FIXED LAYOUT + LOADING SCREEN
# ------------------------------
st.markdown(
    """
    <style>
    /* Import elegant font */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&display=swap');
    
    /* Reset Streamlit's default white container */
    .stApp {
        background-color: #FAF3F5;
        font-family: 'Cormorant Garamond', 'Times New Roman', serif;
    }
    
    /* Fix the white background container */
    .block-container {
        background-color: transparent !important;
        border-radius: 0 !important;
        padding: 2rem 3rem !important;
        max-width: 900px;
    }
    
    /* Ensure no unwanted backgrounds */
    .main > div {
        background-color: transparent;
    }
    
    /* Main title */
    .main-title {
        font-size: 3.2rem;
        font-weight: 300;
        letter-spacing: 2px;
        color: #4A0E1F;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    
    .sub-title {
        font-size: 1.4rem;
        font-weight: 300;
        letter-spacing: 4px;
        color: #9F2B68;
        text-align: center;
        margin-top: -0.5rem;
        margin-bottom: 2rem;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(159, 43, 104, 0.2);
        padding-bottom: 1.5rem;
    }
    
    /* Name input styling */
    .name-section {
        max-width: 400px;
        margin: 0 auto 2rem auto;
        text-align: center;
    }
    
    .name-label {
        color: #4A0E1F;
        font-size: 1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    /* Soft card containers */
    .category-card {
        background-color: white;
        border-radius: 24px;
        padding: 2rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(74, 14, 31, 0.05);
        border: 1px solid rgba(159, 43, 104, 0.1);
        transition: all 0.3s ease;
    }
    
    .category-card:hover {
        box-shadow: 0 20px 40px rgba(74, 14, 31, 0.08);
        border-color: rgba(159, 43, 104, 0.2);
    }
    
    /* Category title */
    .category-title {
        font-size: 1.8rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        color: #4A0E1F;
        letter-spacing: 1px;
        border-bottom: 1px solid #F0D1DC;
        padding-bottom: 0.75rem;
    }
    
    /* Item rows */
    .item-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 0;
        border-bottom: 1px solid #F8E8ED;
    }
    
    .item-name {
        font-size: 1.2rem;
        font-weight: 400;
        color: #2D2D2D;
        letter-spacing: 0.3px;
    }
    
    .claimed-by {
        font-size: 1rem;
        color: #9F2B68;
        font-style: italic;
        font-weight: 300;
    }
    
    .available {
        font-size: 1rem;
        color: #9F2B68;
        opacity: 0.5;
        font-style: italic;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 30px;
        border: 1px solid #F0D1DC;
        background-color: white;
        color: #4A0E1F;
        font-weight: 300;
        font-size: 0.85rem;
        padding: 0.15rem 1.2rem;
        transition: all 0.2s ease;
        letter-spacing: 0.5px;
        font-family: 'Cormorant Garamond', serif;
    }
    
    .stButton button:hover {
        border-color: #9F2B68;
        background-color: #FDF8FA;
        color: #9F2B68;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(159, 43, 104, 0.1);
    }
    
    .stButton button:disabled {
        opacity: 0.3;
        border-color: #E5E7EB;
        transform: none;
        box-shadow: none;
    }
    
    /* Delete button */
    .delete-button button {
        color: #9F2B68;
        border-color: #F8E8ED;
        font-size: 0.8rem;
        padding: 0.15rem 1rem;
    }
    
    .delete-button button:hover {
        border-color: #800020;
        background-color: #FFF0F5;
        color: #800020;
    }
    
    /* Input fields */
    .stTextInput input {
        border-radius: 30px;
        border: 1px solid #F0D1DC;
        background-color: white;
        padding: 0.6rem 1.2rem;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
    }
    
    .stTextInput input:focus {
        border-color: #9F2B68;
        box-shadow: 0 0 0 2px rgba(159, 43, 104, 0.1);
    }
    
    .stTextInput input::placeholder {
        color: #D4A5B5;
        font-style: italic;
        font-weight: 300;
    }
    
    /* Export button */
    .export-section {
        text-align: center;
        margin: 3rem 0 2rem 0;
        padding-top: 1rem;
        border-top: 1px solid #F0D1DC;
    }
    
    .export-button button {
        background-color: #4A0E1F;
        color: white;
        border: none;
        padding: 0.4rem 2.5rem;
        font-size: 1rem;
        letter-spacing: 2px;
    }
    
    .export-button button:hover {
        background-color: #9F2B68;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(74, 14, 31, 0.2);
    }
    
    /* Hint message */
    .hint-message {
        color: #9F2B68;
        font-style: italic;
        text-align: center;
        margin: 1rem 0 2rem 0;
        opacity: 0.7;
        font-size: 1.1rem;
    }
    
    /* Empty state */
    .empty-message {
        color: #9F2B68;
        opacity: 0.5;
        font-style: italic;
        text-align: center;
        margin: 1.5rem 0;
        font-size: 1.1rem;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #F0D1DC;
    }
    
    /* Loading screen */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #FAF3F5;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        opacity: 1;
        transition: opacity 0.5s ease;
        cursor: pointer;
    }
    
    .loading-content {
        text-align: center;
        animation: subtlePulse 2s ease-in-out infinite;
        pointer-events: none;
    }
    
    .loading-icon {
        font-size: 3.5rem;
        color: #4A0E1F;
        opacity: 0.9;
    }
    
    .loading-text {
        color: #9F2B68;
        font-size: 1.3rem;
        margin-top: 1rem;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    .loading-overlay.fade-out {
        opacity: 0;
    }
    
    @keyframes subtlePulse {
        0% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.02); opacity: 1; }
        100% { transform: scale(1); opacity: 0.7; }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    
    <div id="loading-overlay" class="loading-overlay">
        <div class="loading-content">
            <div class="loading-icon">🥂</div>
            <div class="loading-text">Galentine's</div>
        </div>
    </div>
    
    <script>
        // Function to remove loading overlay
        function removeLoadingOverlay() {
            var overlay = document.getElementById('loading-overlay');
            if (overlay && !overlay.classList.contains('fade-out')) {
                overlay.classList.add('fade-out');
                setTimeout(function() {
                    if (overlay && overlay.parentNode) {
                        overlay.parentNode.removeChild(overlay);
                    }
                }, 500);
            }
        }
        
        // Remove on any key press
        document.addEventListener('keydown', function() {
            removeLoadingOverlay();
        });
        
        // Remove on any click
        document.addEventListener('click', function() {
            removeLoadingOverlay();
        });
        
        // Also remove after 3 seconds as fallback
        setTimeout(function() {
            removeLoadingOverlay();
        }, 3000);
    </script>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Initialize session state
# ------------------------------
if "potluck_items" not in st.session_state:
    st.session_state.potluck_items = []
    
if "name" not in st.session_state:
    st.session_state.name = ""

# ------------------------------
# Header
# ------------------------------
st.markdown('<h1 class="main-title">Galentine\'s Potluck</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Who\'s Bringing What</p>', unsafe_allow_html=True)

# ------------------------------
# Name input
# ------------------------------
st.markdown('<div class="name-section">', unsafe_allow_html=True)
st.markdown('<p class="name-label">Your Name</p>', unsafe_allow_html=True)
st.text_input(
    "Your name",
    key="name",
    placeholder="Enter your name",
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)

current_name = st.session_state.name.strip() if st.session_state.name else ""

if not current_name:
    st.markdown('<p class="hint-message">Please enter your name to continue</p>', unsafe_allow_html=True)

# ------------------------------
# Helper functions
# ------------------------------
def get_items_for_category(category):
    return [item for item in st.session_state.potluck_items if item["category"] == category]

def is_duplicate(new_name, exclude_item=None):
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
    st.session_state.potluck_items.append({
        "name": item_name.strip(), 
        "category": category, 
        "claimed_by": None,
        "added_by": current_name
    })
    st.session_state[f"new_item_{category}"] = ""

def claim_item(item, claimer):
    claimer = claimer.strip() if claimer else None
    if claimer and item["claimed_by"] is None:
        item["claimed_by"] = claimer

def unclaim_item(item, claimer):
    claimer = claimer.strip() if claimer else None
    if claimer and item["claimed_by"] == claimer:
        item["claimed_by"] = None

def delete_item(item):
    if item in st.session_state.potluck_items:
        st.session_state.potluck_items.remove(item)

# ------------------------------
# Categories
# ------------------------------
categories = ["Snacks", "Main Dishes", "Beverages", "Alcohol", "Desserts"]

# ------------------------------
# Render categories
# ------------------------------
for category in categories:
    with st.container():
        st.markdown(f'<div class="category-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="category-title">{category}</div>', unsafe_allow_html=True)

        items_in_cat = get_items_for_category(category)

        if not items_in_cat:
            st.markdown('<p class="empty-message">No items yet</p>', unsafe_allow_html=True)
        else:
            for item in items_in_cat:
                cols = st.columns([3, 2, 2])
                
                with cols[0]:
                    st.markdown(f'<span class="item-name">{item["name"]}</span>', unsafe_allow_html=True)
                
                with cols[1]:
                    if item["claimed_by"]:
                        st.markdown(f'<span class="claimed-by">{item["claimed_by"]}</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="available">Available</span>', unsafe_allow_html=True)
                
                with cols[2]:
                    button_cols = st.columns([1, 1])
                    
                    with button_cols[0]:
                        if item["claimed_by"] is None:
                            st.button(
                                "Claim",
                                key=f"claim_{category}_{item['name']}_{id(item)}",
                                on_click=claim_item,
                                args=(item, st.session_state.name),
                                disabled=not current_name,
                            )
                        elif item["claimed_by"] == current_name:
                            st.button(
                                "Unclaim",
                                key=f"unclaim_{category}_{item['name']}_{id(item)}",
                                on_click=unclaim_item,
                                args=(item, st.session_state.name),
                                disabled=not current_name,
                            )
                    
                    with button_cols[1]:
                        if current_name and item.get("added_by") == current_name:
                            st.button(
                                "✕",
                                key=f"delete_{category}_{item['name']}_{id(item)}",
                                on_click=delete_item,
                                args=(item,),
                                help="Delete item",
                            )

        # Add new item
        st.markdown("<hr />", unsafe_allow_html=True)
        col_input, col_button = st.columns([4, 1])
        with col_input:
            st.text_input(
                "New item",
                key=f"new_item_{category}",
                placeholder="Add an item...",
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

        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Export
# ------------------------------
if st.session_state.potluck_items:
    st.markdown('<div class="export-section">', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.potluck_items)
    df["Status"] = df["claimed_by"].apply(lambda x: "Claimed" if x else "Available")
    df = df.rename(columns={
        "name": "Item", 
        "category": "Category", 
        "claimed_by": "Claimed By",
        "added_by": "Added By"
    })
    df = df[["Item", "Category", "Claimed By", "Status", "Added By"]]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Potluck")
        
        # Style the Excel sheet
        workbook = writer.book
        worksheet = writer.sheets["Potluck"]
        
        header_format = workbook.add_format({
            'bold': False,
            'font_color': '#4A0E1F',
            'bg_color': '#F8E8ED',
            'border': 0,
            'font_name': 'Cormorant Garamond',
            'font_size': 11
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 18)
    
    output.seek(0)

    st.download_button(
        label="Export to Excel",
        data=output,
        file_name=f"galentine_potluck_{time.strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="export",
    )
    st.markdown('</div>', unsafe_allow_html=True)
