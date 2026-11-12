import streamlit as st

def main():
    st.set_page_config(
        page_title="Members - Group Project",
        page_icon="👥",
        layout="wide"

    )

    st.title("👥 สมาชิกในกลุ่มและบทบาทความรับผิดชอบ")
    st.write("ข้อมูลรายชื่อสมาชิกกลุ่ม รหัสนักศึกษา และหน้าที่ความรับผิดชอบในโปรเจกต์")
    st.markdown("---")

    members_list = [

        {
            "name": "MISS PAPHATSON WATCHARAWONGSRI",
            "student_id": "1680703335",
            "role": " display_data.py ",

        },
        {

            "name": "MR. RAPEEPHAT WANNASAMRAN",
            "student_id": "1680703947",
            "role": " bayes.py, custom_app.py main.py ",

        },
        {

            "name": "MR. PHATTARAPOL RODAUPAKARN",
            "student_id": "1680704473",
            "role": " markov.py ",

        },
        {

            "name": "MR. PEERAPOL NIMKHEAW",
            "student_id": "1680706353",
            "role": " members.py ", 

        },
        {

            "name": "MR.PITIPAN KHAMPHUKEAD",
            "student_id": "1680706486",
            "role": " statistics.py ",

        }

    ]

    col1, col2 = st.columns(2)

    for index, member in enumerate(members_list):
        target_col = col1 if index % 2 == 0 else col2

        with target_col:
            with st.container(border=True):
                st.subheader(member["name"])
                st.write(f"🆔 **รหัสนักศึกษา:** {member['student_id']}")
                st.write(f"📌 **หน้าที่รับผิดชอบ:** {member['role']}")

if __name__ == "__main__":

    main()
 