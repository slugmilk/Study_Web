import streamlit as st

st.title('Hello World!')
st.write('여기는 텍스트 구간')

"""
# 여기는 제목
## 여기는 작은 제목
- 첫번째
- 두번째
- 세번째
"""

# 텍스트 입력 상자
text = st.text_input('문자열')
st.write(text)

# 체크박스
selected = st.checkbox('개인정보 사용에 동의하시겠습니까?')
if selected:
    st.success('동의했습니다!')

market  = st.selectbox('시장', ('코스닥', '코스피', '나스닥'))
st.write(f'selected market: {market}')

options = st.multiselect('종목', ['카카오', '네이버', '삼성', '엘지'])
st.write(', '.join(options))

st.metric(labe='카카오', value='30000원', delta='1000원')