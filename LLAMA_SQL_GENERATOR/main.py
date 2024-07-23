import re
import streamlit as st
import google.generativeai as genai

Gemeni_Ai_key = "AIzaSyDC26RYHFY7FXBBHvstklxI9a5r-bQUjFY"

genai.configure(api_key=Gemeni_Ai_key)

model = genai.GenerativeModel("gemini-pro")

def extract_sql_query(text):
    match = re.search(r"```sql\n(.*?)\n```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main():
    st.set_page_config(page_title="Sql Query Generative", page_icon=":robot:")
    st.markdown(
        """
        <div  style="text-align: center;"> 
        <h1> SQL QUERY GENERATOR 🤖🦾🦿 </h1>
        <h3> I can generate sql for you!!! </h3>
        <h4> With Explanation as Well </h4>
        <p> This is a simple tool that allows you to generate SQL queries based on your prompt </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    text_input = st.text_area("Enter your Query here in Plain English")
    
    submit = st.button("Generate SQL Query")
    
    if submit:
        with st.spinner("Generating SQL Query...."):
            template = """
            Create a SQL query snippet with the below text:
            
            ```
            {text_input}
            ```
            
            I just want sql query
            """
            
            formatted_template = template.format(text_input=text_input)
            
            response = model.generate_content(formatted_template)
            raw_output = response.text
            sql_query = extract_sql_query(raw_output)
            
            print(sql_query)

            expected_output = f"""
            What would be the expected response of the sql query snippet:
            
            ```
            {sql_query}
            ```
            
            Provide a sample tabular Response with no explanation
            """
            
            eout = model.generate_content(expected_output).text
            
            explanation = f"""
            Explain this sql query:
            
            Please provide the simplest explanation
            
            ```
            {sql_query}
            ```
            """
            
            explainout = model.generate_content(explanation).text
            
            with st.container():
                st.success("SQL Query generated successfully! Here is your sql query below:")
                st.code(sql_query, language="sql")
                
                st.success("Expected output of this SQL query will be:")
                st.markdown(eout)
                
                st.success("Explanation of this Query is:")
                st.markdown(explainout)
                
main()
