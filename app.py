# app.py

import streamlit as st
from rag_pipeline import chatbot_response, semantic_search, format_results
from recommended import recommend_similar_products
from db import log_interaction, get_recent_logs


st.set_page_config(page_title="SmartBuy 🧞", layout="wide")

st.title("🛍️ SmartBuy: AI-Powered Laptop Assistant")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Search", "💬 Chatbot", "🎁 Recommend"])

# -------------------
# 🔍 Semantic Search
# -------------------
with tab1:
    st.header("Semantic Laptop Search")
    query = st.text_input("Enter your query:", placeholder="e.g., i5 16GB SSD under 60000")

    if st.button("Search", key="search_button") and query:
        results = semantic_search(query)
        if results:
            log_interaction("search", query, format_results(results))
            st.subheader("Top Results:")
            selected_product = None
            for i, item in enumerate(results, 1):
                st.markdown(f"""
                **{i}. {item['ProductName']}**
                - 💰 Price: ₹{item['Current_Price']} (MRP: ₹{item['MRP']})
                - ⚙️ Proccessor: {item['Proccessor']}
                - 🧠 RAM: {item['Ram']}
                - 💾 Storage: {item['Storage']}
                """)
                
                if st.button(f"Select {item['ProductName']}", key=f"select_{i}"):
                    selected_product = item['ProductName']
                    # Store selected product in session state
                    st.session_state.selected_product = selected_product

            if selected_product:
                st.session_state.selected_product = selected_product
                st.success(f"Selected Product: {selected_product}")
        else:
            st.warning("No products found matching your query.")

# -------------------
# 💬 Chatbot
# -------------------
with tab2:
    st.header("Ask SmartBuy (Chatbot)")
    chat_query = st.text_area("Ask anything about laptops:", height=100, placeholder="e.g., Recommend best laptop for gaming under 70K")

    if st.button("Ask", key="chat_button") and chat_query:
        with st.spinner("Thinking..."):
            response = chatbot_response(chat_query)
        st.markdown("#### 🤖 SmartBuy says:")
        st.markdown(response)

# -------------------
# 🎁 Recommendations
# -------------------
with tab3:
    st.header("Get Recommendations")
    #product_input = st.text_input("Enter exact product name:", placeholder="e.g., HP Pavilion 15")

    #if st.button("Recommend", key="recommend_button") and product_input:
    if 'selected_product' in st.session_state:
        product_input = st.session_state.selected_product
        st.markdown(f"**Selected Product**: {product_input}")
        st.subheader("Similar Products:")

        try:
            recommendations = recommend_similar_products(product_input)
            if recommendations:
                st.subheader("You may also like:")
                for item in recommendations:
                    st.markdown(f"""
                    **{item['ProductName']}**
                    - 💰 Price: ₹{item['Current_Price']} (MRP: ₹{item['MRP']})
                    - ⚙️ Proccessor: {item['Proccessor']}
                    - 🧠 RAM: {item['Ram']}
                    - 💾 Storage: {item['Storage']}
                    """)
            else:
                st.warning("No similar products found.")
        except ValueError as e:
            st.error(str(e))
    else:
        st.info("No product selected. Please search for a laptop in the Search tab first.")

# -------------------
# Search history
# -------------------

with st.expander("🕓 View recent search history"):
    history = get_recent_logs("search", limit=5)
    for q, r, ts in history:
        st.markdown(f"**{ts}** — {q}")
