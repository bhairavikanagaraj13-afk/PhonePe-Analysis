import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import json
from streamlit_plotly_events import plotly_events
import streamlit.components.v1 as components

conn = psycopg2.connect(
    dbname="phonepe_db",
    user="postgres",
    password="B130899",
    host="localhost"
)

st.set_page_config(layout="wide")
st.markdown(
    """
    <div style="width:100%; background-color:purple; padding:12px 0;">
        <h1 style="color:white; text-align:center; margin:0;">
            PhonePe Dashboard
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)
menu=st.sidebar.selectbox("Select Page",["Home","Analysis"])
if menu == "Home":

    c1, c2, c3 = st.columns([3,1,1])

    with c1:
        category = st.radio(
        "Select Category",
        ["Transaction", "User", "Insurance"],
        horizontal=True
    )

    with c2:
        year = st.selectbox(
        "Year",
        [2018,2019,2020,2021,2022,2023,2024]
    )

    with c3:
        quarter = st.selectbox(
        "Quarter",
        [1,2,3,4]
    )
        
    left_col, right_col = st.columns([2.2, 1])
    with left_col:
         if category=="Transaction": 
            kpi_query1 = """
            SELECT 
                state,
                SUM(dis_t_count) AS total_transactions,
                SUM(dis_t_amount) AS total_transaction_amount
            FROM 
                map_transaction
            GROUP BY 
                state
            ORDER BY 
                state;
                    """

            kpi_df = pd.read_sql(kpi_query1, conn, params=(year, quarter))
            #st.dataframe(kpi_df)
            #st.dataframe(kpi_df)
            #df = pd.read_csv("C:\\Users\\Bhairavi\\OneDrive\\DataScience\\Transaction_data_indiamap.csv")
            fig = px.choropleth(
            kpi_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='state',
            color='total_transaction_amount',
            color_continuous_scale='Reds'
            )

            fig.update_geos(fitbounds="locations", visible=False)
    
            st.plotly_chart(fig, use_container_width=True)
         elif category=="User":
            kpi_query1 = """
            SELECT 
                state,
                SUM(registered_users) AS total_registered_users,
                SUM(appopens_u) AS app_opens
            FROM 
                map_user
            GROUP BY 
                state
            ORDER BY 
                state;
                    """

            kpi_df = pd.read_sql(kpi_query1, conn, params=(year, quarter))
            #st.dataframe(kpi_df)
            #st.dataframe(kpi_df)
            #df = pd.read_csv("C:\\Users\\Bhairavi\\OneDrive\\DataScience\\Transaction_data_indiamap.csv")
            fig = px.choropleth(
            kpi_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='state',
            color='app_opens',
            color_continuous_scale='Reds'
            )

            fig.update_geos(fitbounds="locations", visible=False)
    
            st.plotly_chart(fig, use_container_width=True)
         elif category=="Insurance":
            kpi_query1 = """
            SELECT 
                state,
                SUM(ins_amount_m) AS total_insurance_amount,
                SUM(ins_count_M) AS total_insurance_count
            FROM 
                map_insurance
            GROUP BY 
                state
            ORDER BY 
                state;
                    """

            kpi_df = pd.read_sql(kpi_query1, conn, params=(year, quarter))
            #df = pd.read_csv("C:\\Users\\Bhairavi\\OneDrive\\DataScience\\Transaction_data_indiamap.csv")
            fig = px.choropleth(
            kpi_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='state',
            color='total_insurance_amount',
            color_continuous_scale='Reds'
            )

            fig.update_geos(fitbounds="locations", visible=False)
    
            st.plotly_chart(fig, use_container_width=True)
            




    with right_col:

     if category == "Transaction":
            
        kpi_query = """
        SELECT
        SUM(transaction_count) AS total_txn,
        SUM(transaction_amount) AS total_amount,
        SUM(transaction_amount)/NULLIF(SUM(transaction_count),0) AS avg_txn
        FROM agg_transaction
        WHERE year = %s AND quarter = %s;
        """

        kpi_df = pd.read_sql(kpi_query, conn, params=(year, quarter))
        
        total_txn = kpi_df.loc[0, "total_txn"] or 0
        total_amount = kpi_df.loc[0, "total_amount"] or 0
        avg_txn = kpi_df.loc[0, "avg_txn"] or 0

        total_txn = int(total_txn)
        total_amount = float(total_amount)
        avg_txn = float(avg_txn)


        cat_query = """
            SELECT
            transaction_type,
            SUM(transaction_count) AS total_txn
            FROM agg_transaction
            WHERE year = %s AND quarter = %s
            GROUP BY transaction_type
            ORDER BY total_txn DESC;
            """

        cat_df = pd.read_sql(cat_query, conn, params=(year, quarter))


        html = f"""
        <div style="
        background-color:#5d3954;
        padding:20px;
        border-radius:30px;
        color:white;
        ">

        <h3 style="color:white;font-weight:bold;font-size:30px">Transactions</h3>

        <p style="color:white; font-size:18px;">All PhonePe transactions</p>

        <h1 style="color:#fff8dc;">{total_txn:,}</h1>

        <div style="display:flex;justify-content:space-between;">
        <div>
        <p>Total payment value</p>
        <h4 style="color:#fff8dc;">₹ {total_amount/10000000:.2f} Cr</h4>
        </div>
        <div>
        <p>Avg. transaction value</p>
        <h4 style="color:#fff8dc;">₹ {avg_txn:,.0f}</h4>
        </div>
        </div>

        <hr style="opacity:0.2;">

        <h4>Categories</h4>
        
        """
        
        for _, row in cat_df.iterrows():
            html += f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span>{row['transaction_type']}</span>
                <span style="color:#fff8dc;">{int(row['total_txn']):,}</span>
            </div>
            """

        html += "</div>"
        
        components.html(html, height=550)
        
        if "top_view" not in st.session_state:
         st.session_state.top_view = "state"

        b1, b2, b3 = st.columns(3)

        with b1:
         if st.button("State", use_container_width=True):
          st.session_state.top_view = "state"


        with b2:
          if st.button("District", use_container_width=True):
             st.session_state.top_view = "district"

             
        with b3:
         if st.button("Pincode", use_container_width=True):
            st.session_state.top_view = "pincode"
                
        if category == "Transaction":
          
           if st.session_state.top_view == "state":
          
             Q = """
             SELECT
             INITCAP(state) AS name,
             SUM(top_amount_T) AS value
             FROM top_transaction
             WHERE year = %s AND quarter = %s
             AND STATE IS NOT NULL
             GROUP BY state
             ORDER BY value DESC
             LIMIT 10;
             """
             df = pd.read_sql(Q, conn, params=(year, quarter))
             df = df.reset_index(drop=True)

             table_html = """
                <div style="
                background-color:#5d3954;
                padding:15px;
                border-radius:20px;
                color:white;
                ">
                <table style="width:100%;border-collapse:collapse;">
                <p style="color:white; font-size:18px;">Top 10 States</p>
                <tr>
                <th style="text-align:left;padding:6px;">Name</th>
                <th style="text-align:right;padding:6px;">Value</th>
                </tr>
                """

             for _, r in df.iterrows():
                    table_html += f"""
                    <tr>
                        <td style="padding:6px;">{r['name']}</td>
                        <td style="padding:6px;text-align:right;color:#fff8dc;">
                            {r['value']:,.2f}
                        </td>
                    </tr>
                    """

             table_html += "</table></div>"

             components.html(table_html, height=550)

           elif st.session_state.top_view == "district":
              Q="""
             SELECT
             INITCAP(entity_name_top_T) AS name,
             SUM(top_amount_T) AS value
             FROM top_transaction
             WHERE year=%s AND quarter=%s
             AND level_top_T='district'
             AND entity_name_top_T IS NOT NULL
             GROUP BY entity_name_top_T
             ORDER BY value DESC
             LIMIT 10;
             """
              df=pd.read_sql(Q,conn, params=(year,quarter))
              df=df.reset_index(drop=True)
              table_html="""
               <div style="
               background-color:#5d3954;
               padding:15px;
               border-radius:20px;
               color:white;
               ">
               <table style="width:100%;border-collapse:collapse;">
               <p style="color:white; font-size:18px;">Top 10 Districts</p>
               <tr>
               <th style="text-align:left;padding:6px;">Name</th>
               <th style="text-align:right;padding:6px;">Values</th>
              """
              for _, r in df.iterrows():
                 table_html+=f"""
                 <tr>
                    <td style="padding:6px;">{r['name']}</td>
                    <td style="padding:6px;text-align:right;color:#fff8dc;">
                    {r['value']}
                    </td>
                </tr>
                 """
              table_html+="</table></div>"
              
              components.html(table_html,height=550)


           elif st.session_state.top_view=="pincode":
              Q="""
                 SELECT
                 entity_name_top_T AS pincode,
                 SUM(top_amount_T) AS value
                 FROM top_transaction
                 WHERE year=%s AND quarter=%s
                 AND level_top_T='pincodes' AND entity_name_top_T IS NOT NULL
                 GROUP BY entity_name_top_T
                 ORDER BY value DESC
                 LIMIT 10;
                 """
              df=pd.read_sql(Q,conn,params=(year,quarter))
              df=df.reset_index(drop=True)
              table_html="""
              <div style="
              background-color:#5d3954;
              padding:15px;
              border-radius:20px;
              color:white;
              ">
              <table style="width:100px;border-collapse:collapse;">
              <p style="color:white; font-size:18px;">Top 10 Pincode</p>
               <tr>
               <th style="text-align:left;padding:6px;">Pincodes</th>
               <th style="text-align:right;padding:6px;">Values</th>
              """
              for _, r in df.iterrows():
                 table_html+=f"""
                 <tr>
                    <td style="padding:6px;width:120px;">{r['pincode']}</td>
                    <td style="padding:6px 6px 6px 50px;text-align:right;color:#fff8dc;">
                    {r['value']}
                    </td>
                </tr>
                 """
              table_html+="</table></div>"
              
              components.html(table_html,height=550)
        
     elif category=="User":
        kpi_query = """
         SELECT
         SUM(registered_users) AS total_reg_user,
         SUM(appopens_u) AS total_appopen
         FROM map_user
         WHERE year = %s AND quarter = %s;
         """
        kpi_df = pd.read_sql(kpi_query, conn, params=(year, quarter))

        total_reg_user = kpi_df.loc[0, "total_reg_user"] or 0
        total_appopen = kpi_df.loc[0, "total_appopen"] or 0
        
        total_Reg_user = int(total_reg_user)
        total_appopen = int(total_appopen)

        html = f"""
        <div style="
        background-color:#5d3954;
        padding:20px;
        border-radius:30px;
        color:white;
        ">

        <h3 style="color:white;font-weight:bold;font-size:30px">User</h3>

        <p style="color:white; font-size:18px;">Registered Phonepe Users till Q{quarter},{year}</p>

        <h1 style="color:#fff8dc;">{total_reg_user:,}</h1>

        <div style="display:flex;justify-content:space-between;">
        <div>
        <p style="color:white; font-size:18px;">Phonepe App opens in Q{quarter},{year}</p>
        <h4 style="color:#fff8dc;">{total_appopen:,}</h4>
        </div>
        </div>

        <hr style="opacity:0.2;">

        """
        

        

        components.html(html, height=385)

        if "top_view" not in st.session_state:
          st.session_state.top_view = "state"

        b1, b2, b3 = st.columns(3)

        with b1:
          if st.button("State", use_container_width=True):
           st.session_state.top_view = "state"


        with b2:
          if st.button("District", use_container_width=True):
             st.session_state.top_view = "district"

             
        with b3:
         if st.button("Pincode", use_container_width=True):
            st.session_state.top_view = "pincode"

        if category == "User":
          
           if st.session_state.top_view == "state":
          
                Q = """
                SELECT
                INITCAP(state) AS name,
                SUM(registered_users) AS value
                FROM top_user
                WHERE year = %s AND quarter = %s
                AND STATE IS NOT NULL
                GROUP BY state
                ORDER BY value DESC
                LIMIT 10;
                """
                df = pd.read_sql(Q, conn, params=(year, quarter))
                df = df.reset_index(drop=True)

                table_html = """
                <div style="
                background-color:#5d3954;
                padding:15px;
                border-radius:20px;
                color:white;
                ">
                <table style="width:100%;border-collapse:collapse;">
                <p style="color:white; font-size:18px;">Top 10 States</p>
                <tr>
                <th style="text-align:left;padding:6px;">States</th>
                <th style="text-align:right;padding:6px;">Value</th>
                </tr>
                """

                for _, r in df.iterrows():
                    table_html += f"""
                    <tr>
                        <td style="padding:6px;">{r['name']}</td>
                        <td style="padding:6px;text-align:right;color:#fff8dc;">
                            {r['value']:,.2f}
                        </td>
                    </tr>
                    """

                table_html += "</table></div>"

              

                components.html(table_html, height=550)

           elif st.session_state.top_view == "district":
             Q="""
             SELECT
             INITCAP(entity_name_top_U) AS name,
             SUM(registered_users) AS value
             FROM top_user
             WHERE year=%s AND quarter=%s
             AND level_top_U='district'
             AND entity_name_top_U IS NOT NULL
             GROUP BY entity_name_top_U
             ORDER BY value DESC
             LIMIT 10;
             """
             df=pd.read_sql(Q,conn, params=(year,quarter))
             df=df.reset_index(drop=True)
             table_html="""
               <div style="
               background-color:#5d3954;
               padding:15px;
               border-radius:20px;
               color:white;
               ">
               <table style="width:100%;border-collapse:collapse;">
               <p style="color:white; font-size:18px;">Top 10 Districts</p>
               <tr>
               <th style="text-align:left;padding:6px;">Name</th>
               <th style="text-align:right;padding:6px;">Values</th>
              """
             for _, r in df.iterrows():
                 table_html+=f"""
                 <tr>
                    <td style="padding:6px;">{r['name']}</td>
                    <td style="padding:6px;text-align:right;color:#fff8dc;">
                    {r['value']}
                    </td>
                </tr>
                 """
             table_html+="</table></div>"

             
             components.html(table_html,height=550)
        
           elif st.session_state.top_view=="pincode":
             Q="""
            SELECT
            entity_name_top_U AS pincode,
            SUM(registered_users) AS value
            FROM top_user
            WHERE year=%s AND quarter=%s
            AND level_top_U='pincodes' AND entity_name_top_U IS NOT NULL
            GROUP BY entity_name_top_U
            ORDER BY value DESC
            LIMIT 10;
            """
             df=pd.read_sql(Q,conn,params=(year,quarter))
             df=df.reset_index(drop=True)
             table_html="""
              <div style="
              background-color:#5d3954;
              padding:15px;
              border-radius:20px;
              color:white;
              ">
              <table style="width:100px;border-collapse:collapse;">
              <p style="color:white; font-size:18px;">Top 10 Pincode</p>
               <tr>
               <th style="text-align:left;padding:6px;">Pincodes</th>
               <th style="text-align:right;padding:6px;">Values</th>
              """
             for _, r in df.iterrows():
                 table_html+=f"""
                 <tr>
                    <td style="padding:6px;width:120px;">{r['pincode']}</td>
                    <td style="padding:6px 6px 6px 100px;text-align:right;color:#fff8dc;">
                    {r['value']}
                    </td>
                </tr>
                 """
             table_html+="</table></div>"

             
             components.html(table_html,height=550)


        
     elif category=='Insurance':
            
        kpi_query = """
        SELECT
        SUM(ins_count) AS total_ins_count,
        SUM(ins_amount) AS total_ins_amount,
        SUM(ins_amount)/NULLIF(SUM(ins_count),0) AS avg_ins_amount
        FROM agg_insurance
        WHERE year = %s AND quarter = %s;
        """

        kpi_df = pd.read_sql(kpi_query, conn, params=(year, quarter))

        total_ins_count = kpi_df.loc[0, "total_ins_count"] or 0
        total_ins_amount = kpi_df.loc[0, "total_ins_amount"] or 0
        avg_ins_amount = kpi_df.loc[0, "avg_ins_amount"] or 0

        total_ins_count = int(total_ins_count)
        total_ins_amount = float(total_ins_amount)
        avg_ins_amount = float(avg_ins_amount)


        html = f"""
        <div style="
        background-color:#5d3954;
        padding:20px;
        border-radius:30px;
        color:white;
        ">

        <h3 style="color:white;font-weight:bold;font-size:30px">Insurance</h3>

        <p style="color:white; font-size:18px;">All India Insurance policy purchased</p>

        <h1 style="color:#fff8dc;">{total_ins_count:,}</h1>

        <div style="display:flex;justify-content:space-between;">
        <div>
        <p>Total premium value</p>
        <h4 style="color:#fff8dc;">₹ {total_ins_amount/10000000:.2f} Cr</h4>
        </div>
        <div>
        <p>Avg.premium value</p>
        <h4 style="color:#fff8dc;">₹ {avg_ins_amount:,.0f}</h4>
        </div>
        </div>

        <hr style="opacity:0.2;">

        """


        html += "</div>"
        

        components.html(html, height=350)

        if "top_view" not in st.session_state:
          st.session_state.top_view = "state"

        b1, b2, b3 = st.columns(3)

        with b1:
          if st.button("State", use_container_width=True):
           st.session_state.top_view = "state"


        with b2:
          if st.button("District", use_container_width=True):
             st.session_state.top_view = "district"

             
        with b3:
         if st.button("Pincode", use_container_width=True):
            st.session_state.top_view = "pincode"

        if category == "Insurance":
          
            if st.session_state.top_view == "state":
        
                Q = """
                SELECT
                INITCAP(state) AS name,
                SUM(top_amount_i) AS value
                FROM top_insurance
                WHERE year = %s AND quarter = %s
                AND STATE IS NOT NULL
                GROUP BY state
                ORDER BY value DESC
                LIMIT 10;
                """
                df = pd.read_sql(Q, conn, params=(year, quarter))
                df = df.reset_index(drop=True)

                table_html = """
                    <div style="
                    background-color:#5d3954;
                    padding:15px;
                    border-radius:20px;
                    color:white;
                    ">
                    <table style="width:100%;border-collapse:collapse;">
                    <p style="color:white; font-size:18px;">Top 10 States</p>
                    <tr>
                    <th style="text-align:left;padding:6px;">Name</th>
                    <th style="text-align:right;padding:6px;">Value</th>
                    </tr>
                    """

                for _, r in df.iterrows():
                    table_html += f"""
                        <tr>
                            <td style="padding:6px;">{r['name']}</td>
                            <td style="padding:6px;text-align:right;color:#fff8dc;">
                                {r['value']:,.2f}
                            </td>
                        </tr>
                    """

                table_html += "</table></div>"


                components.html(table_html, height=550)

            elif st.session_state.top_view == "district":
                Q="""
                SELECT
                INITCAP(entity_name_top_i) AS name,
                SUM(top_amount_i) AS value
                FROM top_insurance
                WHERE year=%s AND quarter=%s
                AND level_top_i='district'
                AND entity_name_top_i IS NOT NULL
                GROUP BY entity_name_top_i
                ORDER BY value DESC
                LIMIT 10;
                """
                df=pd.read_sql(Q,conn, params=(year,quarter))
                df=df.reset_index(drop=True)

                table_html="""
                    <div style="
                    background-color:#5d3954;
                    padding:15px;
                    border-radius:20px;
                    color:white;
                    ">
                    <table style="width:100%;border-collapse:collapse;">
                    <p style="color:white; font-size:18px;">Top 10 Districts</p>
                    <tr>
                    <th style="text-align:left;padding:6px;">Name</th>
                    <th style="text-align:right;padding:6px;">Values</th>
                    """
                for _, r in df.iterrows():
                    table_html+=f"""
                    <tr>
                        <td style="padding:6px;">{r['name']}</td>
                        <td style="padding:6px;text-align:right;color:#fff8dc;">
                        {r['value']}
                        </td>
                    </tr>
                """
                table_html+="</table></div>"

                components.html(table_html,height=550)

            elif st.session_state.top_view=="pincode":
                Q="""
                SELECT
                entity_name_top_i AS pincode,
                SUM(top_amount_i) AS value
                FROM top_insurance
                WHERE year=%s AND quarter=%s
                AND level_top_i='pincodes' AND entity_name_top_i IS NOT NULL
                GROUP BY entity_name_top_i
                ORDER BY value DESC
                LIMIT 10;
                """
                df=pd.read_sql(Q,conn,params=(year,quarter))
                df=df.reset_index(drop=True)

                table_html="""
                    <div style="
                    background-color:#5d3954;
                    padding:15px;
                    border-radius:20px;
                    color:white;
                    ">
                    <table style="width:100px;border-collapse:collapse;">
                    <p style="color:white; font-size:18px;">Top 10 Pincode</p>
                    <tr>
                    <th style="text-align:left;padding:6px;">Pincodes</th>
                    <th style="text-align:right;padding:6px;">Values</th>
                    """
                for _, r in df.iterrows():
                    table_html+=f"""
                    <tr>
                        <td style="padding:6px;width:120px;">{r['pincode']}</td>
                        <td style="padding:6px 6px 6px 100px;text-align:right;color:#fff8dc;">
                        {r['value']}
                        </td>
                    </tr>
                """
                table_html+="</table></div>"

                components.html(table_html,height=550)

elif menu=="Analysis":
         st.subheader("Business case study")

         analysis_type = st.selectbox(
        "choose case study",
        [
            "Decoding Transaction Dynamics on PhonePe",
            "Insurance Penetration and Growth Potential Analysis",
            "Transaction Analysis for Market Expansion",
            "User Engagement and Growth Strategy",
            "Transaction Analysis Across States and Districts"
        ]
         )
         if analysis_type=="Decoding Transaction Dynamics on PhonePe":

            state_q = """
            SELECT DISTINCT state
            FROM map_transaction
            ORDER BY state
            """

            state_df = pd.read_sql(state_q, conn)

            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>State-wise Transaction Analysis</b>", unsafe_allow_html=True)

            state_list = state_df["state"].tolist()

            selected_state = st.selectbox(
                "Choose State",
                state_list
             )
            left_col,right_col=st.columns(2)
            with left_col:
                q_year = """
                SELECT
                    year,
                    SUM(transaction_count) AS total_transaction
                FROM agg_transaction
                WHERE state = %s
                GROUP BY year
                ORDER BY year;
                """

                df_year = pd.read_sql(q_year, conn, params=(selected_state,))


                fig = px.line(
                    df_year,
                    x="year",
                    y="total_transaction",
                    markers=True,
                    title=f"Total Transactions over Years - {selected_state}"
                )

                st.plotly_chart(fig, use_container_width=True)
            with right_col:
               q_year = """
                SELECT
                    year,
                    SUM(transaction_amount) AS total_amount
                FROM agg_transaction
                WHERE state = %s
                GROUP BY year
                ORDER BY year;
                """

               df_year = pd.read_sql(q_year, conn, params=(selected_state,))


               fig = px.line(
                    df_year,
                    x="year",
                    y="total_amount",
                    markers=True,
                    title=f"Total Transactions amount over Years - {selected_state}"
                )

               st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>Payment category performance</b>", unsafe_allow_html=True)

            left_col,right_col=st.columns(2)
            with left_col:
               q_type = """
                SELECT
                    transaction_type,
                    SUM(transaction_count) AS total_transaction_count
                FROM agg_transaction
                GROUP BY transaction_type
                ORDER BY total_transaction_count DESC;
                """

               df_type = pd.read_sql(q_type, conn)


               fig = px.pie(
                df_type,
                names="transaction_type",
                values="total_transaction_count",
                hole=0.45,
                title=f"Transaction count Distribution"
            )

               st.plotly_chart(fig, use_container_width=True)
            with right_col:
               q_type="""
               SELECT
                  transaction_type,
                  SUM(transaction_amount) AS total_amount
               FROM agg_transaction
               GROUP BY transaction_type
               ORDER BY total_amount DESC;
               """
               df_type=pd.read_sql(q_type,conn)

               fig = px.pie(
                  df_type,
                  names="transaction_type",
                  values="total_amount",
                  hole=0.45,
                  title=f"Transaction Amount Distribution"
            )
               st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>Payment category performance state-wise</b>", unsafe_allow_html=True)

            
            state_q = """
            SELECT DISTINCT state
            FROM map_transaction
            ORDER BY state;
            """

            state_df = pd.read_sql(state_q, conn)

            state_list = state_df["state"].tolist()

            selected_state = st.selectbox(
                " ",
                state_list
            )
            cat_q = """
                SELECT
                    transaction_type,
                    SUM(transaction_amount) AS total_amount
                FROM agg_transaction
                WHERE state = %s
                GROUP BY transaction_type
                ORDER BY total_amount DESC;
                """

            cat_df = pd.read_sql(cat_q, conn, params=(selected_state,))


            fig = px.bar(
                cat_df,
                x="transaction_type",
                y="total_amount",
                color="transaction_type",   
                title=f"Top Performing Transaction Categories -{selected_state}",
                labels={
                    "transaction_type": "Transaction Category",
                    "total_amount": "Total Transaction Amount"
                },
                height=500,
                width=20                   
            )

            fig.update_layout(
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)
        
         elif analysis_type=="Insurance Penetration and Growth Potential Analysis":
            state_q = """
            SELECT DISTINCT state
            FROM map_transaction
            ORDER BY state
            """

            state_df = pd.read_sql(state_q, conn)

            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>State-wise Insurance policy Analysis</b>", unsafe_allow_html=True)

            state_list = state_df["state"].tolist()

            selected_state = st.selectbox(
                "Choose state ",
                state_list
            )
            left_col,right_col=st.columns(2)
            with left_col:
                cat_q="""
                SELECT
                    year,
                    SUM(ins_count) AS total_count
                    FROM agg_insurance
                    WHERE state = %s
                    GROUP BY year
                    ORDER BY year;
                """
                cat_df=pd.read_sql(cat_q,conn, params=(selected_state,))
                fig1 = px.line(
                    cat_df,
                    x="year",
                    y="total_count",
                    markers=True,
                    title=f"Overall Insurance Policy Growth in - {selected_state}"
                )

                
                st.plotly_chart(fig1, use_container_width=True)
            with right_col:
                cat_q="""
                  SELECT
                  quarter,
                  SUM(ins_count) AS total_count
                  FROM agg_insurance
                  WHERE state = %s
                  GROUP BY quarter
                  ORDER BY quarter;
                 """
                cat_df=pd.read_sql(cat_q,conn, params=(selected_state,))
                fig1= px.bar(
                   cat_df,
                   x="quarter",
                   y="total_count",
                   title=f"Insurance policy count Quarter wise - {selected_state}",
                   text_auto=True
                )

                st.plotly_chart(fig1, use_container_width=True)
            top5_q = """
                SELECT
                entity_name_top_I AS district,
                SUM(top_amount_I) AS total_amount
                FROM top_insurance
                WHERE state = %s AND level_top_i='district'
                GROUP BY entity_name_top_I
                ORDER BY total_amount DESC
                LIMIT 5
                """

            top5_df = pd.read_sql(top5_q, conn, params=(selected_state,))
            fig_top5 = px.bar(
                top5_df,
                x="district",
                y="total_amount",
                title=f"Top 5 Districts by Insurance Amount - {selected_state}"
            )
            
            st.plotly_chart(fig_top5, use_container_width=True)

            least5_q = """
                SELECT
                entity_name_top_I AS district,
                SUM(top_amount_I) AS total_amount
                FROM top_insurance
                WHERE state = %s AND level_top_i='district'
                GROUP BY entity_name_top_I
                ORDER BY total_amount ASC
                LIMIT 5
                """

            least5_df = pd.read_sql(least5_q, conn, params=(selected_state,))
            fig_least5 = px.bar(
                least5_df,
                x="district",
                y="total_amount",
                title=f"Least 5 Districts by Insurance Amount - {selected_state}"
            )
            
            st.plotly_chart(fig_least5, use_container_width=True)
        
            df2 = """
                SELECT
                entity_name_top_i AS district,
                SUM(top_amount_i) / NULLIF(SUM(top_count_i),0) AS avg_policy_value
                FROM top_insurance
                WHERE state = %s
                AND level_top_i = 'district'
                GROUP BY entity_name_top_i
                ORDER BY avg_policy_value DESC
                LIMIT 5;
                """
            df_tp5 = pd.read_sql(df2, conn, params=(selected_state,))
            fig2 = px.bar(
                df_tp5,
                x="district",
                y="avg_policy_value",
                title=f"High value insurance district - {selected_state}"
            )

            
            st.plotly_chart(fig2, use_container_width=True)
        
         elif analysis_type=="Transaction Analysis for Market Expansion":
            state_q = """
            SELECT DISTINCT state
            FROM map_transaction
            ORDER BY state
            """

            state_df = pd.read_sql(state_q, conn)

            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>State-wise transaction Analysis for Market expansion</b>", unsafe_allow_html=True)

            state_list = state_df["state"].tolist()

            selected_state = st.selectbox(
                "Choose state ",
                state_list
            )

            #Transaction intensity across districts
            q1 = """
            SELECT
                district_name_t,
                SUM(dis_t_count) AS total_txn
            FROM map_transaction
            WHERE state = %s
            GROUP BY district_name_t
            """
            df1 = pd.read_sql(q1, conn, params=(selected_state,))
            fig1 = px.histogram(
                df1,
                x="district_name_t",
                y="total_txn",
                nbins=20,
                title=f"Transaction intensity across districts- {selected_state}"
            )

            st.plotly_chart(fig1, use_container_width=True)
            #Transaction category dependency
            q2 = """
            SELECT
                transaction_type,
                SUM(transaction_count) AS total_txn
            FROM agg_transaction
            WHERE state = %s
            GROUP BY transaction_type
            ORDER BY total_txn DESC
            """
            df2 = pd.read_sql(q2, conn, params=(selected_state,))

            fig2 = px.pie(
                df2,
                names="transaction_type",
                values="total_txn",
                hole=0.45,
                title=f"Transaction category dependency - {selected_state}"
            )
            st.plotly_chart(fig2, use_container_width=True)
            # emerging districts
            q3 = """
            SELECT
                district_name_t,
                year,
                SUM(dis_t_count) AS total_txn
            FROM map_transaction
            WHERE state = %s
            GROUP BY district_name_t, year
            ORDER BY district_name_t, year
            """
            df3 = pd.read_sql(q3, conn, params=(selected_state,))

            last_year = df3["year"].max()

            top_d = (
                df3[df3["year"] == last_year]
                .sort_values("total_txn", ascending=False)
                .head(5)["district_name_t"]
            )

            df3_plot = df3[df3["district_name_t"].isin(top_d)]
            fig3 = px.line(
            df3_plot,
            x="year",
            y="total_txn",
            color="district_name_t",
            markers=True,
            title=f"Emerging districts - yearly transaction growth- {selected_state}"
            )

            st.plotly_chart(fig3, use_container_width=True)

            # high value low usauge

            q4 = """
            SELECT
                district_name_t,
                SUM(dis_t_count) AS total_txn,
                SUM(dis_t_amount) AS total_amount,
                SUM(dis_t_amount)/NULLIF(SUM(dis_t_count),0) AS avg_value
            FROM map_transaction
            WHERE state = %s
            GROUP BY district_name_t
            """
            df4 = pd.read_sql(q4, conn, params=(selected_state,))
            median_txn = df4["total_txn"].median()
            df4_low = df4[df4["total_txn"] <= median_txn]

            df4_top = df4_low.sort_values("avg_value", ascending=False).head(5)
            fig4 = px.bar(
                df4_top,
                x="district_name_t",
                y="avg_value",
                title=f"High value but low usage districts- {selected_state}"
            )

            st.plotly_chart(fig4, use_container_width=True)

            #quarter wise

            q5 = """
            SELECT
                quarter,
                SUM(transaction_count) AS total_txn
            FROM agg_transaction
            WHERE state = %s
            GROUP BY quarter
            ORDER BY quarter
            """
            df5 = pd.read_sql(q5, conn, params=(selected_state,))
            fig5 = px.bar(
            df5,
            x="quarter",
            y="total_txn",
            title=f"Quarter-wise transaction seasonal- {selected_state}"
            )
            st.plotly_chart(fig5, use_container_width=True)

            ##User Engagement and Growth Strategy

         elif analysis_type=="User Engagement and Growth Strategy":
            state_q = """
            SELECT DISTINCT state
            FROM map_transaction
            ORDER BY state
            """

            state_df = pd.read_sql(state_q, conn)

            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>State-wise User Engagement and Growth </b>", unsafe_allow_html=True)

            state_list = state_df["state"].tolist()

            selected_state = st.selectbox(
                "Choose state ",
                state_list
            )

            # intensity across districts

            q1 = """
            SELECT
                user_district AS district,
                SUM(registered_users) AS total_users,
                SUM(appopens_u) AS total_opens,
                SUM(appopens_u)/NULLIF(SUM(registered_users),0) AS engagement_ratio
            FROM map_user
            WHERE state = %s
            GROUP BY user_district
            ORDER BY engagement_ratio DESC
            LIMIT 10
            """
            df1 = pd.read_sql(q1, conn, params=(selected_state,))
            fig1 = px.bar(
                df1,
                x="engagement_ratio",
                y="district",
                title=f"Top engaged districts -App opens per user-{selected_state}"
            )

            st.plotly_chart(fig1, use_container_width=True)

            # Least engaged district

            q2 = """
            SELECT
                user_district AS district,
                SUM(appopens_u) AS total_opens
            FROM map_user
            WHERE state = %s
            GROUP BY user_district
            ORDER BY total_opens ASC
            LIMIT 5
            """
            df2 = pd.read_sql(q2, conn, params=(selected_state,))
            fig2 = px.bar(
                df2,
                x="district",
                y="total_opens",
                title=f"Least engaged districts - {selected_state}"
            )

            st.plotly_chart(fig2, use_container_width=True)

            #High registration- low engagement

            q3 = """
            SELECT
                user_district AS district,
                SUM(registered_users) AS total_users,
                SUM(appopens_u) AS total_opens,
                SUM(appopens_u)/NULLIF(SUM(registered_users),0) AS engagement_ratio
            FROM map_user
            WHERE state = %s
            GROUP BY district
            """
            df3 = pd.read_sql(q3, conn, params=(selected_state,))
            median_users = df3["total_users"].median()
            df3_low = df3[df3["total_users"] >= median_users]

            df3_low = df3_low.sort_values("engagement_ratio").head(10)
            fig3 = px.bar(
                df3_low,
                x="district",
                y="engagement_ratio",
                
                title=f"High registration but low engagement districts-{selected_state}"
            )

            st.plotly_chart(fig3, use_container_width=True)

            #user growth trend

            q4 = """
            SELECT
                year,
                SUM(registered_users) AS total_users
            FROM map_user
            WHERE state = %s
            GROUP BY year
            ORDER BY year
            """
            df4 = pd.read_sql(q4, conn, params=(selected_state,))

            fig4 = px.line(
                df4,
                x="year",
                y="total_users",
                markers=True,
                title=f"Registered user growth over years- {selected_state}"
            )

            st.plotly_chart(fig4, use_container_width=True)

            #District engagement consistency

            q5 = """
            SELECT
                user_district AS district,
                quarter,
                SUM(appopens_u) AS total_opens
            FROM map_user
            WHERE state = %s
            GROUP BY user_district, quarter
            """
            df5 = pd.read_sql(q5, conn, params=(selected_state,))
            stability = (
                df5
                .groupby("district")["total_opens"]
                .std()
                .reset_index()
                .rename(columns={"total_opens":"engagement_std"})
            )

            stable = stability.sort_values("engagement_std").head(10)
            fig5 = px.bar(
                stable,
                x="district",
                y="engagement_std",
                title=f"Most stable engagement districts (lower variation)-{selected_state}"
            )

            st.plotly_chart(fig5, use_container_width=True)

            #Transaction Analysis Across States and Districts
         elif analysis_type=="Transaction Analysis Across States and Districts":

            st.markdown("<b style='color:red;font-weight:bold;font-size:30px;'>Transaction Analysis Across States and Districts </b>", unsafe_allow_html=True)

            

            # top 10 states transaction volume

            q1 = """
            SELECT
                state,
                SUM(dis_t_count) AS total_txn
            FROM map_transaction
            GROUP BY state
            ORDER BY total_txn DESC
            LIMIT 10
            """
            df1 = pd.read_sql(q1, conn)
            fig1 = px.bar(
                df1,
                x="state",
                y="total_txn",
                title=f"Top 10 states by transaction volume"
            )
            st.plotly_chart(fig1, use_container_width=True)
            #top 10 states transaction value
            q2 = """
            SELECT
                state,
                SUM(dis_t_amount) AS total_amount
            FROM map_transaction
            GROUP BY state
            ORDER BY total_amount DESC
            LIMIT 10
            """
            df2 = pd.read_sql(q2, conn)

            fig2 = px.bar(
                df2,
                x="state",
                y="total_amount",
                title="Top 10 states by transaction value"
            )
            st.plotly_chart(fig2, use_container_width=True)

            # least 10 states
            q = """
            SELECT
                state,
                SUM(dis_t_amount) AS total_amount
            FROM map_transaction
            GROUP BY state
            ORDER BY total_amount ASC
            LIMIT 10
            """
            df = pd.read_sql(q, conn)

            fig = px.bar(
                df,
                x="state",
                y="total_amount",
                title="least 10 states by transaction value"
            )
            st.plotly_chart(fig, use_container_width=True)


            state_q = """
            SELECT DISTINCT state
            FROM map_transaction
            ORDER BY state
            """

            state_df = pd.read_sql(state_q, conn)
            state_list = state_df["state"].tolist()

            selected_state = st.selectbox(
                "Choose state ",
                state_list
            )
            # top 10 district for selected state
            q3 = """
            SELECT
                district_name_t AS district,
                SUM(dis_t_count) AS total_txn
            FROM map_transaction
            WHERE state = %s
            GROUP BY district_name_t
            ORDER BY total_txn DESC
            LIMIT 10
            """
            df3 = pd.read_sql(q3, conn, params=(selected_state,))
            fig3 = px.bar(
                df3,
                x="district",
                y="total_txn",
                title=f"Top 10 districts by transaction volume - {selected_state}"
            )
            st.plotly_chart(fig3, use_container_width=True)

            # least 10 districts for selected states

            q4 = """
            SELECT
                district_name_t AS district,
                SUM(dis_t_count) AS total_txn
            FROM map_transaction
            WHERE state = %s
            GROUP BY district_name_t
            ORDER BY total_txn ASC
            LIMIT 10
            """
            df4 = pd.read_sql(q4, conn, params=(selected_state,))
            fig4 = px.bar(
                df4,
                x="district",
                y="total_txn",
                title=f"Least performing districts by transaction volume-{selected_state}"
            )
            st.plotly_chart(fig4, use_container_width=True)














            



             


        


               


     

