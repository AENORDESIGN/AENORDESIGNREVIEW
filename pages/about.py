
import streamlit as st
def render_about():
    st.markdown("""
    <div class='centered'>
        <h2>About</h2>
        <p>
        AENOR DESIGN은<br>
        설계를 앞두고 행정 절차를 마주하는 건축가와 기획자들을 위해 만들어졌습니다.<br><br>
        우리는 설계자의 시선에서,<br>
        심의라는 복잡한 절차를 더 명확하고 간결하게 정리하고자 합니다.<br><br>
        전국 지자체의 조례와 법령을 바탕으로<br>
        대지와 건축물의 조건에 따라 어떤 심의가 필요한지를 판단하고,<br>
        그 근거를 정리해 보여주는 도구입니다.<br><br>
        설계를 더 잘하기 위한 준비가<br>
        조금 더 단순하고, 정확해지기를 바랍니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.image("static/building_line.png", use_column_width=True)
