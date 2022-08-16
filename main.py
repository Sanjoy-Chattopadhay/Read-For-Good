import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
conn = sqlite3.connect('data.db')

c = conn.cursor()


# Functions
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate DATE)')


def add_data(author, title, article, postdate):
    c.execute('INSERT INTO blogtable (author, title, article, postdate) VALUES (?,?,?,?)',
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


# Layout Templates


title_temp = """
<div style="background-color:#80e8d5;border-radius:10px;margin:10px;padding:10px">
<h4 style="text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >

<h6 style="text-align:center;">Author:{}</h6>

<br>
<br> 
<p style="text-align:justify">{}</p>
</div>
"""
article_temp = """
<div style="background-color:#80e8d5;border-radius:10px;margin:10px;padding:10px;text-align:center">
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
<div style="background-color:#80e8d5;border-radius:10px;margin:10px;padding:10px">
<h4 style="text-align:center;">{}</h4>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
<h6 style="text-align:center;">Author:{}</h6>

<h6 style='text-align:right;'>Post Date: {}</h6> 
</div>
"""
full_message_temp = """
<div style="background-color:#80e8d5;overflow-x: auto; padding:20px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""


def main():
    """A simple CRUD BLOG"""
    st.title('Simple Blog')
    manu = ['Home', 'View Posts', 'Add Post', 'Search', 'Manage Blog']
    choice = st.sidebar.selectbox("Manu", manu)

    if choice == 'Home':
        st.subheader("Home")
        result = view_all_notes()
        for i in result:
            b_author = (i[0])
            b_title = i[1]
            b_article = str(i[2])[0:30]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_title, b_author, b_article, b_post_date), unsafe_allow_html=True)

    elif choice == 'View Posts':
        st.subheader("View Articles")
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Posts:", all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_author = (i[0])
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
            st.markdown(full_message_temp.format(b_article), unsafe_allow_html=True)


    elif choice == "Search":
        st.subheader("Search Articles")
        search_term = st.text_input('Enter Search Term')
        search_choice = st.radio("Field to Search By", ("title", "author"))
        article_result = ''
        if st.button("Search"):

            if search_choice == "title":
                article_result = get_blog_by_title(search_term)
            elif search_choice == "author":
                article_result = get_blog_by_author(search_term)

            for i in article_result:
                b_author = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.markdown(head_message_temp.format(b_title, b_author, b_post_date), unsafe_allow_html=True)
                st.markdown(full_message_temp.format(b_article), unsafe_allow_html=True)

    elif choice == 'Add Post':
        st.subheader("Add Articles")
        create_table()
        blog_author = st.text_input("Enter Author Name ", max_chars=50)
        blog_title = st.text_input("Enter Post Title ")
        blog_article = st.text_area("Enter Article Here ", height=200)
        blog_post_date = st.date_input("Date")
        if st.button("Add"):
            add_data(blog_author, blog_title, blog_article, blog_post_date)
            st.success("Post:{} saved".format(blog_title))

    elif choice == 'Manage Blog':
        st.subheader("Manage Articles")
        result = view_all_notes()
        clean_db = pd.DataFrame(result,columns=['Author','Title','Author','Post Date'])


if __name__ == '__main__':
    main()
