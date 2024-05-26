import streamlit as st
from datetime import datetime
from streamlit_webrtc import webrtc_streamer
from streamlit_server_state import server_state, server_state_lock

# إعداد جلسة Streamlit
st.set_page_config(page_title="الفصل الافتراضي", layout="wide")

# متغيرات الجلسة المحلية
if "role" not in st.session_state:
    st.session_state["role"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None

# متغيرات الجلسة المشتركة
if "session_started" not in server_state:
    server_state["session_started"] = False
if "chat_messages" not in server_state:
    server_state["chat_messages"] = []

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
        with server_state_lock["session_started"]:
            server_state["session_started"] = True
        st.sidebar.success("الجلسة بدأت")

    if server_state["session_started"]:
        st.write("الجلسة جارية...")
        use_camera()

    # الدردشة النصية
    st.sidebar.subheader("الدردشة")
    chat_message = st.sidebar.text_input("أدخل رسالتك:")
    if st.sidebar.button("إرسال"):
        if chat_message:
            timestamp = datetime.now().strftime('%H:%M:%S')
            with server_state_lock["chat_messages"]:
                server_state["chat_messages"].append(f"{timestamp} - {st.session_state['name']}: {chat_message}")
            st.experimental_rerun()

    st.sidebar.write("الدردشة:")
    for message in server_state["chat_messages"]:
        st.sidebar.write(message)

    # العرض الرئيسي
    st.title("مرحبًا بكم في لوحة إدارة الفصل الافتراضي")
    st.write("اختر خيارًا من لوحة التحكم للبدء.")

# صفحة الطالب
def student_dashboard():
    st.sidebar.title("لوحة التحكم")
    st.sidebar.header(f"مرحبًا، {st.session_state['name']} (طالب)")

    if server_state["session_started"]:
        st.sidebar.info("الجلسة جارية، يمكنك الانضمام.")
        use_camera()
    else:
        st.sidebar.warning("لا توجد جلسة جارية حالياً.")

    # الدردشة النصية
    st.sidebar.subheader("الدردشة")
    chat_message = st.sidebar.text_input("أدخل رسالتك:")
    if st.sidebar.button("إرسال"):
        if chat_message:
            timestamp = datetime.now().strftime('%H:%M:%S')
            with server_state_lock["chat_messages"]:
                server_state["chat_messages"].append(f"{timestamp} - {st.session_state['name']}: {chat_message}")
            st.experimental_rerun()

    st.sidebar.write("الدردشة:")
    for message in server_state["chat_messages"]:
        st.sidebar.write(message)

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
