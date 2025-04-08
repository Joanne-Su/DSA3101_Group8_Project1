import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import time

# Image base URL
BASE_URL = "https://raw.githubusercontent.com/NotInvalidUsername/DSA3101_Group8_Project1/main/images/B4/"

# Function to load image from GitHub with cache-busting
def load_image_from_github(image_name):
    url = BASE_URL + image_name + f"?nocache={int(time.time())}"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["Overview", "Topic Clusters", "Business Recommendations"])

# ---------------------------
# PAGE 1: OVERVIEW
# ---------------------------
if page == "Overview":
    st.title("🎢 B4: Disneyland Review Analysis")
    
    st.subheader("📌 Business Question")
    st.markdown("""
        **How can we promptly address high-risk interactions to improve guest experience?**
        
        By analyzing reviews that rated Disneyland 1 or 2 stars, we can uncover common themes and pain points. 
        This allows us to identify the most pressing issues and develop actionable insights to improve park satisfaction.
    """)

    st.subheader("🌿 Hierarchical Model of Topics")
    st.markdown("""
        The branches in the hierarchical model are colored based on topic similarity. We identified **4 clusters** 
        representing key categories extracted from the reviews. 
    """)

    try:
        model_image = load_image_from_github("hierarchical_clustering.png")
        st.image(model_image, caption="Hierarchical Topic Clustering", use_container_width=True)
    except Exception as e:
        st.error(f"Error loading hierarchical_clustering.png: {e}")

# ---------------------------
# PAGE 2: CLUSTERS
# ---------------------------
elif page == "Topic Clusters":
    st.title("💬 Topic Clusters: Key Themes from High-Risk Reviews")
    st.markdown("""
                To generate the clusters, we combined similar topic representations based on the hierarchical model.
                Each cluster represents a group of related concerns raised by Disneyland guests. 
                BERTopic also provides the mapping between reviews and topics.
                Hence, we analysed some of these reviews to identify key issues for each cluster.""" )

    # Cluster 1
    with st.expander("🟣 Cluster 1: Customer Experience"):
        try:
            img = load_image_from_github("cluster_1.png")
            st.image(img, caption="Word Cloud Cluster 1", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading cluster_1.png: {e}")
        st.markdown("**Key Issues:**")
        st.markdown("""
        - Overcrowding, high food prices, and long wait times  
        - Negative interactions with other cultures (esp. Hong Kong)  
        - Accessibility/disability issues  
        - Ride closures without notice  
        """)

    # Cluster 2
    with st.expander("🟢 Cluster 2: Ticket and Refund Issues"):
        try:
            img = load_image_from_github("cluster_2.png")
            st.image(img, caption="Word Cloud Cluster 2", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading cluster_2.png: {e}")
        st.markdown("**Key Insights:**")
        st.markdown("""
        - FastPass crucial for managing expectations  
        - Complaints about delayed refunds  
        - Confusing or unclear ticket policies  
        """)

    # Cluster 3
    with st.expander("🔴 Cluster 3: Staff Response"):
        try:
            img = load_image_from_github("cluster_3.png")
            st.image(img, caption="Word Cloud Cluster 3", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading cluster_3.png: {e}")
        st.markdown("**Key Issues:**")
        st.markdown("""
        - Overly strict security staff  
        - Inconsistency in staff behavior and quality of interactions
        """)

    # Cluster 4
    with st.expander("🔵 Cluster 4: Park Environment and Smoking"):
        try:
            img = load_image_from_github("cluster_4.png")
            st.image(img, caption="Word Cloud Cluster 4", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading cluster_4.png: {e}")
        st.markdown("**Key Issues:**")
        st.markdown("""
        - Smoking complaints, especially at Disneyland Paris  
        - Lack of designated areas or enforcement  
        """)

# ---------------------------
# PAGE 3: BUSINESS IMPACT & RECOMMENDATIONS
# ---------------------------
elif page == "Business Recommendations":
    st.subheader("🔧 Business Recommendations")
    
    st.subheader("🚨 Why These Issues Matter")
    st.markdown("""
    Negative guest experiences, especially those rated 1 or 2 stars, can significantly affect Disneyland’s reputation, brand loyalty, and revenue. 
    Ignoring these reviews allows recurring issues to fester, impacting return visits and word-of-mouth recommendations.
    """)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🟣 Cluster 1: Customer Experience", 
        "🟢 Cluster 2: Ticket and Refund Issues", 
        "🔴 Cluster 3: Staff Response", 
        "🔵 Cluster 4: Park Environment and Smoking"
    ])

    with tab1:
        st.markdown("""
        - Cultural sensitivity training: Equip staff with training for multicultural interactions.  
        - Accessibility audits: Conduct regular audits to ensure facilities meet accessibility standards.  
        - Ride notifications: Use mobile apps/messages/emails to alert guests in advance of ride closures.  
        """)

    with tab2:
        st.markdown("""
        - Clear ticket policies: Redesign ticketing pages with simpler language and visual flowcharts.  
        - Refund transparency: Provide real-time refund tracking through guests’ accounts.  
        - FastPass awareness: Educate guests pre-arrival about the value and function of FastPass systems.  
        """)

    with tab3:
        st.markdown("""
        - Staff empowerment: Offer conflict de-escalation training and empower frontline staff to make small guest recovery gestures.  
        - Feedback loops: Implement quick digital surveys tied to guest-staff interactions. Can be explored in B5  
        """)

    with tab4:
        st.markdown("""
        - Policy enforcement: Deploy trained personnel or use signage with QR-code-based reporting for non-compliance.  
        """)
