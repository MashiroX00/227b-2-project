import streamlit as st

def main():
    st.set_page_config(
        page_title="CS207 - Overview",
        page_icon="✨",
        layout="wide"

    )

    st.title("CS207 Data Analytics Hub")
    st.caption("แอปพลิเคชันรวมเครื่องมือประมวลผลข้อมูล สถิติ และแบบจำลองความน่าจะเป็น")
    st.markdown("---")

    st.info(

        "👋 **ยินดีต้อนรับ:** ระบบนี้เป็นส่วนหนึ่งของวิชา CS207 "

        "ถูกออกแบบมาเพื่อรวบรวมมอดูลการคำนวณต่างๆ ไว้ในจุดเดียว "

        "สามารถเลือกรันและทดสอบฟังก์ชันการทำงานผ่านเมนูทางด้านซ้าย (Sidebar) ได้ทันที"

    )

    st.write("##") 


    st.markdown("### 🧩 Modules & Features")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        with st.container(border=True):
            st.markdown("##### 📊 Descriptive Statistics")
            st.write("คำนวณค่าสถิติพื้นฐาน สรุปข้อมูลเชิงตัวเลข และแสดงกราฟแนวโน้ม")
            st.caption("Maintainer: PITIPAN")
        
        with st.container(border=True):
            st.markdown("##### 🎲 Probability & Bayes")
            st.write("คำนวณความน่าจะเป็น วิเคราะห์เงื่อนไขด้วยทฤษฎีของ Bayes")
            st.caption("Maintainer: RAPEEPHAT")

    with col2:
        with st.container(border=True):
            st.markdown("##### 🔄 Markov Chain Model")
            st.write("แบบจำลองสถานะมาร์คอฟ สำหรับการทำนายและวิเคราะห์ลำดับข้อมูล")
            st.caption("Maintainer: PHATTARAPOL")
        with st.container(border=True):
            st.markdown("##### 📈 Data Visualization")
            st.write("ดึงข้อมูล แปลงรูปแบบตาราง และจัดทำ Dashboard แสดงผล interactive")
            st.caption("Maintainer: PAPHATSON")

    st.write("##")

    with st.container(border=True):
        st.markdown("##### 👥 Team Members")
        st.write("คลิกที่เมนู **`members`** บริเวณด้านซ้ายมือ เพื่อตรวจสอบรายชื่อและข้อมูลสมาชิกผู้จัดทำโปรเจกต์")

if __name__ == "__main__":

    main()
 