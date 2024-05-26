import streamlit as st
import cv2
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# إعداد جلسة Streamlit
st.set_page_config(page_title="الفصل الافتراضي", layout="wide")

# متغيرات الجلسة
if "role" not in st.session_state:
    st.session_state["role"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None
if "session_started" not in st.session_state:
    st.session_state["session_started"] = False

# وظيفة لاستخدام كاميرا الويب
def use_camera():
    webrtc_streamer(key="camera")

# واجهة المستخدم
def main():
    st.sidebar.title("تسجيل الدخول")
    name = st.sidebar.text_input("أدخل اسمك:")
    role = st.sidebar.selectbox("اختر دورك:", ["معلم", "طالب"])

    if st.sidebar.button("بدء"):
        if name and role:
            st.session_state["name"] = name
            st.session_state["role"] = role
            st.experimental_rerun()
        else:
            st.sidebar.error("الرجاء إدخال اسمك واختيار دورك")

# صفحة المعلم
def teacher_dashboard():
    st.sidebar.title("لوحة التحكم")
    st.sidebar.header(f"مرحبًا، {st.session_state['name']} (معلم)")

    if st.sidebar.button("بدء جلسة"):
        st.session_state["session_started"] = True
        st.sidebar.success("الجلسة بدأت")
    
    if st.session_state["session_started"]:
        st.write("الجلسة جارية...")
        use_camera()
    
    # دردشة نصية
    st.sidebar.subheader("الدردشة")
    chat_message = st.sidebar.text_input("أدخل رسالتك:")
    if st.sidebar.button("إرسال"):
        st.sidebar.write(f"{datetime.now().strftime('%H:%M:%S')} - {chat_message}")

    # العرض الرئيسي
    st.title("مرحبًا بكم في لوحة إدارة الفصل الافتراضي")
    st.write("اختر خيارًا من لوحة التحكم للبدء.")

# صفحة الطالب
def student_dashboard():
    st.sidebar.title("لوحة التحكم")
    st.sidebar.header(f"مرحبًا، {st.session_state['name']} (طالب)")

    if st.session_state["session_started"]:
        st.sidebar.info("الجلسة جارية، يمكنك الانضمام.")
        use_camera()
    else:
        st.sidebar.warning("لا توجد جلسة جارية حالياً.")

    # دردشة نصية
    st.sidebar.subheader("الدردشة")
    chat_message = st.sidebar.text_input("أدخل رسالتك:")
    if st.sidebar.button("إرسال"):
        st.sidebar.write(f"{datetime.now().strftime('%H:%M:%S')} - {chat_message}")

    # العرض الرئيسي
    st.title("مرحبًا بكم في الفصل الافتراضي")
    st.write("اختر خيارًا من لوحة التحكم للبدء.")

# التحقق من الدور وتوجيه المستخدم
if st.session_state["role"] is None:
    main()
else:
    if st.session_state["role"] == "معلم":
        teacher_dashboard()
    elif st.session_state["role"] == "طالب":
        student_dashboard()
