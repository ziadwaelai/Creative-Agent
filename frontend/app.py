
import streamlit as st
import requests
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Creative Agent -  المحتوى الإبداعي",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Global RTL support for Arabic */
    html {
        direction: rtl;
        text-align: right;
    }

    body {
        direction: rtl;
        text-align: right;
    }

    /* Hide sidebar */
    [data-testid="collapsedControl"] {
        display: none;
    }

    /* Main container styling */
    .main {
        padding: 0 20px;
        direction: rtl;
        text-align: right;
    }

    /* Title styling */
    h1 {
        color: #667eea;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }

    h2 {
        color: #667eea;
        margin-top: 30px;
        margin-bottom: 20px;
        text-align: right;
        direction: rtl;
    }

    h3 {
        text-align: right;
        direction: rtl;
    }

    /* Input styling - RTL */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        direction: rtl;
        text-align: right;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        text-align: right;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    /* Progress container - RTL with right border */
    .progress-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border-right: 5px solid #667eea;
        direction: rtl;
        text-align: right;
    }

    .step-item {
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        background: white;
        border-right: 4px solid #667eea;
        direction: rtl;
        text-align: right;
    }

    .step-item.active {
        background: #f0f4ff;
        border-right-color: #667eea;
    }

    .step-item.complete {
        border-right-color: #10b981;
    }

    .step-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 5px;
        text-align: right;
    }

    .step-message {
        color: #666;
        font-size: 14px;
        text-align: right;
    }

    /* Content display - RTL */
    .content-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-right: 5px solid #667eea;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        direction: rtl;
        text-align: right;
        line-height: 1.8;
    }

    .content-box p {
        color: #333;
        font-size: 16px;
        margin-bottom: 15px;
        text-align: right;
        direction: rtl;
    }

    /* Success message - RTL */
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        direction: rtl;
        text-align: right;
    }

    /* Status indicator - RTL margin */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-left: 8px;
        vertical-align: middle;
    }

    .status-indicator.active {
        background: #667eea;
        animation: pulse 1.5s infinite;
    }

    .status-indicator.complete {
        background: #10b981;
    }

    .status-indicator.error {
        background: #ef4444;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    /* Multiselect styling - RTL */
    .stMultiSelect > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        direction: rtl;
        text-align: right;
    }

    /* Expander styling - RTL */
    .streamlit-expanderHeader {
        background: #f5f7fa;
        border-radius: 8px;
        direction: rtl;
        text-align: right;
    }

    /* Markdown RTL support */
    [data-testid="stMarkdownContainer"] {
        direction: rtl;
        text-align: right;
    }

    /* Columns RTL support */
    [data-testid="column"] {
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "api_url" not in st.session_state:
    st.session_state.api_url = st.secrets.get("API_URL",)
if "last_content" not in st.session_state:
    st.session_state.last_content = None
if "stream_data" not in st.session_state:
    st.session_state.stream_data = []

# Main header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1>✨ المحتوى الإبداعي </h1>
        <p style="font-size: 16px; color: #666; margin: 0;">
            إنشاء محتوى تسويقي احترافي باستخدام الذكاء الاصطناعي
        </p>
        <p style="font-size: 13px; color: #999; margin-top: 5px;">
            مع عرض مباشر للتقدم خطوة بخطوة
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Input section
st.markdown("### 📝 أدخل معلومات المنتج والجمهور")

# Create two columns for input
col1, col2 = st.columns([1, 1])

with col1:
    client_name = st.text_input(
        "🏢 اسم العميل/العلامة التجارية",
        placeholder="مثال: لومين - عصير طبيعي",
        max_chars=200,
        help="أدخل اسم العميل أو العلامة التجارية"
    )

    product_description = st.text_area(
        "📦 وصف المنتج",
        placeholder="وصف تفصيلي للمنتج أو الخدمة...",
        height=120,
        max_chars=2000,
        help="وصف شامل يشمل الميزات والفوائد"
    )

with col2:
    target_audience = st.text_area(
        "👥 الجمهور المستهدف",
        placeholder="وصف فئات الجمهور المستهدف...",
        height=120,
        max_chars=500,
        help="من هو الجمهور الذي تستهدفه؟"
    )

    # Tone of voice selection
    st.markdown("**🎤 نبرة الصوت المطلوبة**")
    tone_options = [
        "شاعري", "طبيعي", "احترافي", "فكاهي",
        "منعش", "موثوق", "فاخر", "حديث",
        "عائلي", "صحي", "ودود", "مثير","شبابي","طبيعي"
    ]

    selected_tones = st.multiselect(
        "اختر نبرة أو أكثر (1-10 نبرات)",
        tone_options,
        default=["طبيعي","شبابي","طبيعي","منعش"],
        max_selections=10,
        label_visibility="collapsed"
    )

# Validation section
st.markdown("---")

validation_cols = st.columns(4)

validation_states = {
    "client": (client_name, 1, 200),
    "product": (product_description, 10, 2000),
    "audience": (target_audience, 5, 500),
    "tones": (selected_tones, 1, 10)
}

validation_results = {}
for key, (value, min_val, max_val) in validation_states.items():
    if isinstance(value, list):
        length = len(value)
    else:
        length = len(value)

    is_valid = length >= min_val and length <= max_val
    validation_results[key] = is_valid

with validation_cols[0]:
    if validation_results["client"]:
        st.success(f"✅ العميل ({len(client_name)}/200)")
    else:
        st.error("❌ العميل مطلوب")

with validation_cols[1]:
    if validation_results["product"]:
        st.success(f"✅ المنتج ({len(product_description)}/2000)")
    else:
        st.error("❌ المنتج (10+ أحرف)")

with validation_cols[2]:
    if validation_results["audience"]:
        st.success(f"✅ الجمهور ({len(target_audience)}/500)")
    else:
        st.error("❌ الجمهور (5+ أحرف)")

with validation_cols[3]:
    if validation_results["tones"]:
        st.success(f"✅ النبرات ({len(selected_tones)}/10)")
    else:
        st.error("❌ اختر نبرة واحدة")

# Generate button
st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    all_valid = all(validation_results.values())
    generate_button = st.button(
        "🚀 توليد المحتوى",
        use_container_width=True,
        type="primary",
        disabled=not all_valid
    )

if generate_button:
    payload = {
        "client_name": client_name,
        "product_description": product_description,
        "target_audience": target_audience,
        "tone_of_voice": selected_tones
    }

    # Create containers for streaming display
    st.markdown("---")

    # Create two-column layout
    left_col, right_col = st.columns([1, 1])

    # Use placeholders for progress and content that update without redrawing
    progress_placeholder = right_col.empty()
    content_header = left_col.empty()
    content_placeholder = left_col.empty()

    steps_status = {
        1: {"title": "تحليل المنتج", "emoji": "📦", "status": "pending", "data": None, "streaming": None},
        2: {"title": "تحليل الجمهور", "emoji": "👥", "status": "pending", "data": None, "streaming": None},
        3: {"title": "توليد الأفكار", "emoji": "💡", "status": "pending", "data": None, "streaming": None},
        4: {"title": "توليد المحتوى", "emoji": "✍️", "status": "pending", "data": None, "streaming": None},
        5: {"title": "الاقتراحات التسويقية", "emoji": "📊", "status": "pending", "data": None, "streaming": None},
        6: {"title": "الصياغة النهائية", "emoji": "🎨", "status": "pending", "data": None, "streaming": None}
    }

    final_content = ""
    step_6_started = False

    try:
        # Connect to streaming endpoint
        response = requests.post(
            f"{st.session_state.api_url}/api/generate-creative-content-stream",
            json=payload,
            stream=True,
            timeout=600
        )

        if response.status_code == 200:
            # Parse streaming events
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                    if line_str.startswith("data: "):
                        try:
                            event_data = json.loads(line_str[6:])

                            # Update status based on event
                            step_num = event_data.get("step")
                            step_type = event_data.get("type")

                            if step_num and step_num in steps_status:
                                if step_type == "step_start":
                                    steps_status[step_num]["status"] = "active"
                                    steps_status[step_num]["streaming"] = ""  # Initialize streaming content
                                elif step_type == "step_stream":
                                    # Append streamed content
                                    if steps_status[step_num]["streaming"] is None:
                                        steps_status[step_num]["streaming"] = ""
                                    steps_status[step_num]["streaming"] += event_data.get("content", "")

                                elif step_type == "step_complete":
                                    steps_status[step_num]["status"] = "complete"
                                    # Store the final step data
                                    if "data" in event_data:
                                        steps_status[step_num]["data"] = event_data.get("data")
                                elif step_type == "step_error":
                                    steps_status[step_num]["status"] = "error"

                            # For step 6 streaming, accumulate final content for left column
                            if step_num == 6 and step_type == "step_stream":
                                final_content += event_data.get("content", "")

                                # Show header on first step 6 event
                                if not step_6_started:
                                    content_header.markdown("### 📨 المحتوى المُولد")
                                    step_6_started = True

                                # Update final content in real-time
                                content_placeholder.markdown(f"""
<div style="
    direction: rtl;
    text-align: right;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-right: 5px solid #667eea;
    padding: 25px;
    border-radius: 12px;
    margin: 20px 0;
    line-height: 1.8;
    font-size: 16px;
    color: #333;
">

{final_content}

</div>
""", unsafe_allow_html=True)

                            # Update progress display on the right column (single update, not redrawn)
                            with progress_placeholder.container():
                                st.markdown("### ⏱️ تقدم التوليد")

                                # Display steps 1-5 with expandable details (step 6 is the final output shown on left)
                                for step_num in range(1, 6):
                                    status = steps_status[step_num]["status"]
                                    title = steps_status[step_num]["title"]
                                    emoji = steps_status[step_num]["emoji"]
                                    step_data = steps_status[step_num].get("data")
                                    streaming_content = steps_status[step_num].get("streaming")

                                    # Display step
                                    status_icon = {
                                        "pending": "⏳",
                                        "active": "⚙️",
                                        "complete": "✅",
                                        "error": "❌"
                                    }.get(status, "⏳")

                                    color = {
                                        "pending": "#999",
                                        "active": "#667eea",
                                        "complete": "#10b981",
                                        "error": "#ef4444"
                                    }.get(status, "#999")

                                    # Show streaming content while active, then final data when complete
                                    if status == "active" and streaming_content:
                                        # Show streaming content while being generated
                                        with st.expander(f"{status_icon} {emoji} {step_num}. {title}", expanded=True):
                                            st.markdown(streaming_content)
                                    elif step_data and status == "complete":
                                        # Show final data when complete
                                        with st.expander(f"{status_icon} {emoji} {step_num}. {title}", expanded=False):
                                            # Display markdown content from the persona agent
                                            st.markdown(step_data)
                                    else:
                                        st.markdown(f"""
                                        <div style="padding: 12px; margin: 8px 0; border-right: 4px solid {color}; background: #f9f9f9; border-radius: 6px;">
                                            <span style="color: {color}; font-weight: 600;">{status_icon} {emoji} {step_num}. {title}</span>
                                        </div>
                                        """, unsafe_allow_html=True)

                            # Handle different event types
                            if event_data.get("type") == "step":
                                pass  # Just update progress

                            elif event_data.get("type") == "step_complete":
                                pass  # Step completed

                            elif event_data.get("type") == "error":
                                st.error(f"❌ {event_data.get('message', 'حدث خطأ')}")

                        except json.JSONDecodeError:
                            pass

            # Final display of content after streaming completes
            if final_content:
                st.session_state.last_content = final_content

                with content_placeholder.container():
                    st.markdown("### 📨 المحتوى المُولد")

                    # Display content with markdown rendering and RTL support
                    st.markdown(f"""
<div style="
    direction: rtl;
    text-align: right;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-right: 5px solid #667eea;
    padding: 25px;
    border-radius: 12px;
    margin: 20px 0;
    line-height: 1.8;
    font-size: 16px;
    color: #333;
">

{final_content}

</div>
""", unsafe_allow_html=True)

                    st.markdown("---")

                    # Prepare download content
                    download_text = f"""
╔════════════════════════════════════════════════════════╗
║                    Creative Agent                      ║
╚════════════════════════════════════════════════════════╝

📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🏢 العميل: {client_name}
📦 المنتج: {product_description[:100]}...
👥 الجمهور: {target_audience[:100]}...
🎤 النبرات: {', '.join(selected_tones)}

════════════════════════════════════════════════════════

{final_content}

════════════════════════════════════════════════════════
Generated by Creative Agent ✨
                    """

                    st.download_button(
                        label="⬇️ تحميل المحتوى",
                        data=download_text,
                        file_name=f"creative_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    # Display metadata
                    st.markdown("---")
                    st.markdown("### 📊 معلومات")

                    meta_col1, meta_col2 = st.columns(2)

                    with meta_col1:
                        st.metric("🎤 النبرات", len(selected_tones))

                    with meta_col2:
                        st.metric("📝 الكلمات", len(final_content.split()))

        else:
            st.error(f"❌ خطأ من الخادم: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.Timeout:
        st.error("❌ انتهاء المهلة الزمنية - الطلب يستغرق وقتاً أطول من المتوقع")
        st.info("💡 تلميح: قد تستغرق عملية التوليد 3-5 دقائق. يرجى الانتظار...")

    except requests.exceptions.ConnectionError:
        st.error("❌ لا يمكن الاتصال بـ API")
        st.info(f"تأكد من أن الخادم يعمل على: {st.session_state.api_url}")
        st.code(f"python -m uvicorn backend.app:app --reload")

    except Exception as e:
        st.error(f"❌ حدث خطأ: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
    <p>Creative Agent | المحتوى الإبداعي</p>
    <p>مع عرض مباشر للتقدم خطوة بخطوة</p>
    <p>© 2025 جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
