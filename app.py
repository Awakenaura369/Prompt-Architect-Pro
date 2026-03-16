import streamlit as st
from groq import Groq

# إعدادات الصفحة والجمالية (Vibe)
st.set_page_config(
    page_title="Prompt Architect Pro", 
    page_icon="🏗️", 
    layout="centered"
)

# ستايل CSS خفيف باش نزيدو لمسة احترافية
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #4a4a4a;
    }
    .stButton button {
        width: 100%;
        border-radius: 20px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Prompt Architect AI")
st.write("حول أفكارك الخام لبرومبتات احترافية كيفهمها الذكاء الاصطناعي بدقة.")

# Sidebar للإعدادات التقنية
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Groq API Key:", type="password", help="جيب الـ API من console.groq.com")
    
    # تحديث الموديلات لآخر ما كاين فـ Groq (2026)
    model_choice = st.selectbox("Select Model:", [
        "llama-3.3-70b-versatile",  # الأقوى في اللوجيك
        "llama-3.1-70b-versatile", 
        "llama-3.1-8b-instant"      # الأسرع
    ])
    
    st.divider()
    st.info("💡 نصيحة: استعمل Llama 3.3 70B للحصول على أفضل هيكلة للبرومبت.")

# الواجهة الأساسية
user_vibe = st.text_area(
    "شنو بغيتي من الـ AI؟ (شرح لي الفكرة بالدارجة أو الإنجليزية)", 
    height=150,
    placeholder="مثلاً: صاوب ليا سكريبت ديال فيديو تيك توك كيهضر على الربح من CPA بالدارجة..."
)

if st.button("Generate Professional Prompt ✨"):
    if not api_key:
        st.error("عفاك دخل API Key ديالك فـ الجنب!")
    elif not user_vibe:
        st.warning("الخانة خاوية، كتب لينا شي 'Vibe' باش نخدموا عليه!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # السيستم برومبت (العقل المدبر)
            system_instruction = """
            You are an expert Prompt Engineer. Your task is to take a raw user idea and transform it into a highly structured, professional prompt for LLMs.
            Follow the RTF (Role, Task, Format) framework:
            1. **Role**: Assign a specialized persona to the AI.
            2. **Task**: Clearly define the objective with step-by-step logic.
            3. **Context**: Add relevant background info to guide the AI.
            4. **Constraints**: Specify what the AI should NOT do.
            5. **Output Format**: Define how the response should be structured (Table, Markdown, etc.).
            
            - If the user input is in Darija/Arabic, maintain the cultural context but output the 'Engineered Prompt' in English (as it works better for AI logic).
            - Only output the final optimized prompt. No conversational filler.
            """

            with st.spinner('🚀 جاري هندسة البرومبت...'):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": f"Transform this: {user_vibe}"}
                    ],
                    model=model_choice,
                    temperature=0.7,
                )
                
                final_prompt = chat_completion.choices[0].message.content
                
                st.success("✅ هاهي البرومبت ناضية!")
                st.markdown("### 📝 البرومبت الاحترافية (Copy & Paste):")
                st.code(final_prompt, language="text")
                st.balloons()
                
        except Exception as e:
            st.error(f"وقع مشكل تقني: {str(e)}")

st.markdown("---")
st.caption("Developed for Marketing Beast AI Workflow 🚀")
