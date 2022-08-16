# DB
import streamlit as st

import pandas as pd
import webbrowser

# Database
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

# Page title and page logo
# from PIL import Image
# img = Image.open('head.jpg')
st.set_page_config(page_title="Good to Read")

# Declaration
def self_declaration():
    self = """
    <div style="background-color:#cedef0;border-radius:10px;margin:10px;padding:10px;text-align:center">

    <h6 style="text-align:center">This website is built by <a href = 
    'https://sanjoy-chattopadhay.github.io/portfolio/'> Sanjoy </a> </h6> </div> """
    st.markdown(self, unsafe_allow_html=True)


hide_menu_style = '''

<style>

#MainMenu { visibility: hidden;}
footer { visibility : hidden;}

</style>

'''
st.markdown(hide_menu_style, unsafe_allow_html=True)


# Functions
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')


def add_data(author, title, article, postdate):
    c.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',
              (author, title, article, postdate))
    conn.commit()


def view_all_notes():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data


def view_all_titles():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data


def get_blog_by_title(title):
    c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data


def get_blog_by_author(author):
    c.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
    data = c.fetchall()
    return data


def delete_data(title):
    c.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
    conn.commit()


# Layout Templates


html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Enrich Life with Blogs</h1>
</div>
"""

title_temp = """
<div style="background-color:#dae0eb; border-radius:10px;margin:10px;padding:10px">
<h4 style="text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
<h6 style="text-align:center;">Author:{}</h6>
<br>
<br> 
<p style="text-align:justify">{}</p>
</div>
"""

article_temp = """
<div style="background-color:#dae0eb;border-radius:10px;margin:10px;padding:10px;text-align:center">
<h4 style="text-align:center;">{}</h4>
<h6 style="text-align:center;">Author:{}</h6>
<h6>Post Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""

head_message_temp = """
<div style="background-color:#cedef0;border-radius:10px;margin:10px;padding:10px">

<h4 style="text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar"  style="vertical-align: middle; float:left;width: 50px; height: 50px; border-radius: 50%;">
<h6 style="text-align:center;">Author:{}</h6>
<h6 style='text-align:center;'>Post Date: {}</h6> 
</div>
<center>
"""

full_message_temp = """
<div style="background-color:#dae0eb;overflow-x: auto; padding:20px;border-radius:5px;margin:10px;">

<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""


def main():
    """A Simple CRUD  Blog"""

    st.markdown(html_temp.format('white', 'Gray'), unsafe_allow_html=True)

    menu = ["Home", "Content", "Read a Post", "Add a Post", "Connect to Me"]
    choice = st.sidebar.selectbox("Select where to go ", menu)

    # Home
    if choice == "Home":
        st.subheader("Home")
        result = view_all_notes()
        for i in result:
            b_author = i[0]
            b_title = i[1]
            b_article = str(i[2])[0:70] + " ..."
            st.write("To read more Go to Read Post on the Top Left Menu ")
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)
        self_declaration()

    # Read Posts
    elif choice == "Read a Post":
        st.subheader("Read Articles")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("Select a Post", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_article), unsafe_allow_html=True)
            self_declaration()

    elif choice == "Add a Post":
        st.subheader("Add Articles")
        create_table()
        blog_author = st.text_input("Enter Author Name", max_chars=50)
        blog_title = st.text_input("Enter Post Title")
        blog_article = st.text_area("Post Article Here", height=200)
        blog_post_date = st.date_input("Date")
        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success("Post:{} saved".format(blog_title))

        # elif choice == "Search":
        #     st.subheader("Search Articles")
        #     search_term = st.text_input('Enter Search Term')
        #     search_choice = st.radio("Field to Search By", ("title", "author"))
        #     article_result = ''
        #     if st.button("Search"):
        #
        #         if search_choice == "title":
        #             article_result = get_blog_by_title(search_term)
        #         elif search_choice == "author":
        #             article_result = get_blog_by_author(search_term)
        #
        #         for i in article_result:
        #             b_author = i[0]
        #             b_title = i[1]
        #             b_article = i[2]
        #             b_post_date = i[3]
        #             st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
        #             st.markdown(full_message_temp.format(b_article), unsafe_allow_html=True)      se
        self_declaration()

    elif choice == "Content":
        st.subheader("Overview Of the Blogs")

        result = view_all_notes()
        clean_db = pd.DataFrame(result, columns=["Author", "Title", "Articles", "Post Date"])
        st.dataframe(clean_db)

        unique_titles = [i[0] for i in view_all_titles()]
        delete_blog_by_title = st.selectbox("Unique Title", unique_titles)
        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Deleted: '{}'".format(delete_blog_by_title))
        self_declaration()

    elif choice == "Connect to Me":
        fb_url = 'https://www.facebook.com/abhik.chattopadhyay.14'
        lk_url = 'https://www.linkedin.com/in/sanjoy-chattopadhyay-390b3a1a6/'
        gthb_url = 'https://github.com/Sanjoy-Chattopadhay'
        twt_url = 'https://twitter.com/Sanjoychattopa7'
        prt_url = 'https://sanjoy-chattopadhay.github.io/portfolio/'
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button('Facebook'):
                webbrowser.open_new_tab(fb_url)
        with col2:
            if st.button('Linkedin'):
                webbrowser.open_new_tab(lk_url)
        with col3:
            if st.button('Twitter'):
                webbrowser.open_new_tab(twt_url)
        with col4:
            if st.button('Github'):
                webbrowser.open_new_tab(gthb_url)
        with col5:
            if st.button('Portfolio'):
                webbrowser.open_new_tab(prt_url)
        self_declaration()


if __name__ == '__main__':
    main()
