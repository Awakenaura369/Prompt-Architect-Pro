import streamlit as st
from groq import Groq

# إعدادات الصفحة (الفايب ديالنا ديما احترافي)
st.set_page_config(page_title="Prompt Architect Pro", page_icon="🚀", layout="centered")

st.title("🚀 Prompt Architect AI")
st.markdown("---")
st.subheader("حول 'الفايب' ديالك لبرومبت احترافية (Groq Edition)")

# Sidebar للإعدادات
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    model_choice = st.selectbox("Choose AI Model:", ["llama3-70b-8192", "llama3-8b-instant"])
    st.info("هاد الأداة كتخدم بـ Framework (Role-Task-Context) باش تخرج أحسن نتيجة.")

# واجهة المستخدم الأساسية
user_vibe = st.text_area("شنو الفكرة اللي فبالك (Vibe)؟", 
                         placeholder="مثلاً: بغيت نصاوب إعلان فيسبوك لمنتج رقمي بـ الدارجة...")

if st.button("Generate Pro Prompt ✨"):
    if not api_key:
        st.error("عفاك دخل API Key ديال Groq أولاً!")
    elif not user_vibe:
        st.warning("كتب لينا شي فكرة باش نقدروا نخدموا عليها!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # السيستم برومبت "المعلم"
            system_logic = """
            You are a Master Prompt Engineer. Your job is to transform a simple user idea into a 
            highly structured, professional AI prompt using the RTF (Role, Task, Format) Framework.
            
            STRUCTURE:
            - Role: Who is the AI?
            - Context: Why are we doing this?
            - Task: Detailed instructions.
            - Constraints: What to avoid.
            - Output: Specify the exact format.
            
            Make the output professional, clear, and optimized for LLMs. 
            ONLY output the final optimized prompt.
            """

            with st.spinner('جاري هندسة البرومبت...'):
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_logic},
                        {"role": "user", "content": f"Transform this vibe: {user_vibe}"}
                    ],
                    model=model_choice,
                )
                
                result = completion.choices[0].message.content
                
                st.success("✅ تم بنجاح!")
                st.markdown("### 📝 البرومبت الاحترافية:")
                st.code(result, language="text")
                st.balloons()
                
        except Exception as e:
            st.error(f"وقع واحد المشكل: {e}")

st.markdown("---")
st.caption("Powered by Groq & Streamlit | Created for the Vibe Coding Journey 🚀")
