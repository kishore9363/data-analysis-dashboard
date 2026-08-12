import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROFESSIONAL UI
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #666;
    margin-bottom: 25px;
}

.section-title {
    font-size: 26px;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# PDF REPORT FUNCTION
# =========================================================

def generate_pdf_report(df, file_name):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    elements = []

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Data Analysis Report",
            title_style
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # DATASET NAME
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            f"<b>Dataset:</b> {file_name}",
            normal_style
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # -----------------------------------------------------
    # DATASET SUMMARY
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Dataset Summary",
            heading_style
        )
    )

    summary_data = [
        ["Metric", "Value"],
        ["Total Rows", str(len(df))],
        ["Total Columns", str(len(df.columns))],
        [
            "Missing Values",
            str(
                int(
                    df.isnull()
                    .sum()
                    .sum()
                )
            )
        ],
        [
            "Duplicate Rows",
            str(
                int(
                    df.duplicated()
                    .sum()
                )
            )
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[250, 150]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),
            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    elements.append(
        summary_table
    )

    elements.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # COLUMN INFORMATION
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Column Information",
            heading_style
        )
    )

    column_data = [
        [
            "Column",
            "Data Type",
            "Missing",
            "Unique"
        ]
    ]

    for column in df.columns:

        column_data.append([
            str(column),
            str(df[column].dtype),
            str(
                int(
                    df[column]
                    .isnull()
                    .sum()
                )
            ),
            str(
                int(
                    df[column]
                    .nunique()
                )
            )
        ])

    column_table = Table(
        column_data,
        repeatRows=1
    )

    column_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                5
            )
        ])
    )

    elements.append(
        column_table
    )

    elements.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # STATISTICAL SUMMARY
    # -----------------------------------------------------

    numeric_columns = (
        df
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )

    if numeric_columns:

        elements.append(
            Paragraph(
                "Statistical Summary",
                heading_style
            )
        )

        stats = (
            df[numeric_columns]
            .describe()
        )

        stats_data = [
            ["Statistic"] +
            [
                str(column)
                for column in stats.columns
            ]
        ]

        for index, row in stats.iterrows():

            stats_data.append(
                [str(index)] +
                [
                    f"{value:.2f}"
                    for value in row
                ]
            )

        stats_table = Table(
            stats_data,
            repeatRows=1
        )

        stats_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.grey
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.black
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    4
                )
            ])
        )

        elements.append(
            stats_table
        )

        elements.append(
            Spacer(1, 20)
        )

    # -----------------------------------------------------
    # AUTOMATIC INSIGHTS
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Automatic Insights",
            heading_style
        )
    )

    # Dataset size

    elements.append(
        Paragraph(
            f"The dataset contains "
            f"<b>{len(df)}</b> rows and "
            f"<b>{len(df.columns)}</b> columns.",
            normal_style
        )
    )

    elements.append(
        Spacer(1, 8)
    )

    # Missing values

    missing_total = int(
        df.isnull()
        .sum()
        .sum()
    )

    if missing_total == 0:

        elements.append(
            Paragraph(
                "The dataset has no missing values.",
                normal_style
            )
        )

    else:

        elements.append(
            Paragraph(
                f"The dataset contains "
                f"<b>{missing_total}</b> missing values.",
                normal_style
            )
        )

    elements.append(
        Spacer(1, 8)
    )

    # Duplicate values

    duplicate_total = int(
        df.duplicated()
        .sum()
    )

    if duplicate_total == 0:

        elements.append(
            Paragraph(
                "No duplicate records were detected.",
                normal_style
            )
        )

    else:

        elements.append(
            Paragraph(
                f"<b>{duplicate_total}</b> duplicate "
                f"records were detected.",
                normal_style
            )
        )

    elements.append(
        Spacer(1, 8)
    )

    # Numeric insights

    for column in numeric_columns:

        mean_value = df[column].mean()
        min_value = df[column].min()
        max_value = df[column].max()

        elements.append(
            Paragraph(
                f"<b>{column}</b>: "
                f"Average = {mean_value:.2f}, "
                f"Minimum = {min_value:.2f}, "
                f"Maximum = {max_value:.2f}.",
                normal_style
            )
        )

        elements.append(
            Spacer(1, 5)
        )

    # Categorical insights

    categorical_columns = (
        df
        .select_dtypes(
            exclude=np.number
        )
        .columns
        .tolist()
    )

    for column in categorical_columns:

        if df[column].nunique() > 0:

            counts = (
                df[column]
                .value_counts()
            )

            top_value = counts.index[0]
            top_count = counts.iloc[0]

            elements.append(
                Paragraph(
                    f"Most common value in "
                    f"<b>{column}</b>: "
                    f"<b>{top_value}</b> "
                    f"({top_count} records).",
                    normal_style
                )
            )

            elements.append(
                Spacer(1, 5)
            )

    elements.append(
        Spacer(1, 15)
    )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Generated using Python, Pandas, "
            "Plotly and Streamlit.",
            normal_style
        )
    )

    # Build PDF

    doc.build(
        elements
    )

    buffer.seek(0)

    return buffer


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '📊 Data Analysis Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload, clean, analyze and visualize your dataset '
    'with automatic insights.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Dashboard")

st.sidebar.markdown(
    "### Navigation"
)

page = st.sidebar.radio(
    "Go to",
    [
        "📊 Overview",
        "🧹 Data Cleaning",
        "📈 Analytics",
        "💡 Automatic Insights",
        "📥 Export"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Built with Python, Pandas, NumPy, "
    "Plotly and Streamlit."
)


# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📂 Upload CSV, Excel or JSON",
    type=[
        "csv",
        "xlsx",
        "json"
    ]
)


# =========================================================
# NO FILE
# =========================================================

if uploaded_file is None:

    st.info(
        "👆 Upload a dataset to start your analysis."
    )

    st.markdown(
        "### Supported Files"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write(
            "📄 **CSV**"
        )

    with col2:

        st.write(
            "📊 **Excel**"
        )

    with col3:

        st.write(
            "🗂️ **JSON**"
        )

    st.stop()


# =========================================================
# READ FILE
# =========================================================

file_name = uploaded_file.name

file_type = (
    file_name
    .split(".")[-1]
    .lower()
)


try:

    if file_type == "csv":

        df = pd.read_csv(
            uploaded_file
        )

    elif file_type == "xlsx":

        df = pd.read_excel(
            uploaded_file
        )

    elif file_type == "json":

        df = pd.read_json(
            uploaded_file
        )

    else:

        st.error(
            "Unsupported file format."
        )

        st.stop()


except Exception as e:

    st.error(
        f"Error reading file: {e}"
    )

    st.stop()


# =========================================================
# SUCCESS MESSAGE
# =========================================================

st.success(
    f"✅ {file_name} loaded successfully!"
)


# =========================================================
# BASIC INFORMATION
# =========================================================

total_rows = len(df)

total_columns = len(
    df.columns
)

missing_values = int(
    df.isnull()
    .sum()
    .sum()
)

duplicate_rows = int(
    df.duplicated()
    .sum()
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "📊 Overview":

    st.markdown(
        '<div class="section-title">'
        '📊 Dataset Overview'
        '</div>',
        unsafe_allow_html=True
    )

    # KPI

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📋 Total Rows",
            f"{total_rows:,}"
        )

    with col2:

        st.metric(
            "📊 Columns",
            total_columns
        )

    with col3:

        st.metric(
            "⚠️ Missing Values",
            f"{missing_values:,}"
        )

    with col4:

        st.metric(
            "♻️ Duplicate Rows",
            f"{duplicate_rows:,}"
        )

    # Preview

    st.markdown(
        "### 📋 Dataset Preview"
    )

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    # Column information

    st.markdown(
        "### 🔤 Column Information"
    )

    column_info = pd.DataFrame({

        "Column": df.columns,

        "Data Type": [
            str(dtype)
            for dtype in df.dtypes
        ],

        "Missing Values": [
            int(
                df[column]
                .isnull()
                .sum()
            )
            for column in df.columns
        ],

        "Unique Values": [
            int(
                df[column]
                .nunique()
            )
            for column in df.columns
        ]
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )


# =========================================================
# DATA CLEANING
# =========================================================

elif page == "🧹 Data Cleaning":

    st.markdown(
        '<div class="section-title">'
        '🧹 Data Cleaning'
        '</div>',
        unsafe_allow_html=True
    )

    clean_data = df.copy()

    # Duplicate removal

    st.markdown(
        "### ♻️ Duplicate Records"
    )

    remove_duplicates = st.checkbox(
        "Remove duplicate rows"
    )

    if remove_duplicates:

        before = len(
            clean_data
        )

        clean_data = (
            clean_data
            .drop_duplicates()
        )

        removed = (
            before -
            len(clean_data)
        )

        st.success(
            f"Removed {removed} duplicate rows."
        )

    # Missing values

    st.markdown(
        "### ⚠️ Missing Values"
    )

    missing_option = st.selectbox(
        "Select a cleaning method",
        [
            "Do nothing",
            "Remove rows with missing values",
            "Fill numeric values with mean",
            "Fill numeric values with median",
            "Fill missing values with 0"
        ]
    )

    if missing_option == (
        "Remove rows with missing values"
    ):

        clean_data = (
            clean_data
            .dropna()
        )

    elif missing_option == (
        "Fill numeric values with mean"
    ):

        numeric_columns = (
            clean_data
            .select_dtypes(
                include=np.number
            )
            .columns
        )

        for column in numeric_columns:

            clean_data[column] = (
                clean_data[column]
                .fillna(
                    clean_data[column]
                    .mean()
                )
            )

    elif missing_option == (
        "Fill numeric values with median"
    ):

        numeric_columns = (
            clean_data
            .select_dtypes(
                include=np.number
            )
            .columns
        )

        for column in numeric_columns:

            clean_data[column] = (
                clean_data[column]
                .fillna(
                    clean_data[column]
                    .median()
                )
            )

    elif missing_option == (
        "Fill missing values with 0"
    ):

        clean_data = (
            clean_data
            .fillna(0)
        )

    # Cleaned dataset

    st.markdown(
        "### ✨ Cleaned Dataset"
    )

    st.dataframe(
        clean_data,
        use_container_width=True
    )

    # Summary

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows After Cleaning",
            len(clean_data)
        )

    with col2:

        st.metric(
            "Columns",
            len(clean_data.columns)
        )

    with col3:

        st.metric(
            "Missing Values",
            int(
                clean_data
                .isnull()
                .sum()
                .sum()
            )
        )


# =========================================================
# ANALYTICS
# =========================================================

elif page == "📈 Analytics":

    st.markdown(
        '<div class="section-title">'
        '📈 Advanced Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    numeric_columns = (
        df
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        df
        .select_dtypes(
            exclude=np.number
        )
        .columns
        .tolist()
    )

    # Statistical summary

    st.markdown(
        "### 📊 Statistical Summary"
    )

    if numeric_columns:

        st.dataframe(
            df[numeric_columns]
            .describe(),
            use_container_width=True
        )

    else:

        st.info(
            "No numeric columns available."
        )

    # Histogram

    if numeric_columns:

        st.markdown(
            "### 📊 Distribution Analysis"
        )

        selected_numeric = st.selectbox(
            "Select numeric column",
            numeric_columns,
            key="histogram_column"
        )

        fig_hist = px.histogram(
            df,
            x=selected_numeric,
            title=(
                f"Distribution of "
                f"{selected_numeric}"
            )
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    # Category chart

    if (
        categorical_columns
        and numeric_columns
    ):

        st.markdown(
            "### 📊 Category Analysis"
        )

        col1, col2 = st.columns(2)

        with col1:

            category_column = st.selectbox(
                "Category",
                categorical_columns,
                key="category_column"
            )

        with col2:

            value_column = st.selectbox(
                "Numeric Value",
                numeric_columns,
                key="value_column"
            )

        grouped_data = (
            df
            .groupby(
                category_column
            )[value_column]
            .mean()
            .reset_index()
        )

        fig_bar = px.bar(
            grouped_data,
            x=category_column,
            y=value_column,
            title=(
                f"Average {value_column} "
                f"by {category_column}"
            )
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    # Correlation

    st.markdown(
        "### 🔗 Correlation Analysis"
    )

    if len(numeric_columns) >= 2:

        correlation = (
            df[numeric_columns]
            .corr()
        )

        fig_corr = px.imshow(
            correlation,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix"
        )

        st.plotly_chart(
            fig_corr,
            use_container_width=True
        )

    else:

        st.info(
            "At least two numeric columns "
            "are required for correlation."
        )

    # Outlier detection

    st.markdown(
        "### 🚨 Outlier Detection"
    )

    if numeric_columns:

        outlier_column = st.selectbox(
            "Select column",
            numeric_columns,
            key="outlier_column"
        )

        Q1 = (
            df[outlier_column]
            .quantile(0.25)
        )

        Q3 = (
            df[outlier_column]
            .quantile(0.75)
        )

        IQR = Q3 - Q1

        lower_limit = (
            Q1 - 1.5 * IQR
        )

        upper_limit = (
            Q3 + 1.5 * IQR
        )

        outliers = df[
            (
                df[outlier_column]
                < lower_limit
            )
            |
            (
                df[outlier_column]
                > upper_limit
            )
        ]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Q1",
                f"{Q1:.2f}"
            )

        with col2:

            st.metric(
                "Q3",
                f"{Q3:.2f}"
            )

        with col3:

            st.metric(
                "Outliers",
                len(outliers)
            )

        if len(outliers) > 0:

            st.warning(
                f"{len(outliers)} "
                f"outlier records detected."
            )

            st.dataframe(
                outliers,
                use_container_width=True
            )

        else:

            st.success(
                "✅ No outliers detected."
            )

    # Top / Bottom

    st.markdown(
        "### 🏆 Top & Bottom Records"
    )

    if numeric_columns:

        ranking_column = st.selectbox(
            "Select ranking column",
            numeric_columns,
            key="ranking_column"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "#### 🔝 Top 10"
            )

            top_records = (
                df
                .sort_values(
                    ranking_column,
                    ascending=False
                )
                .head(10)
            )

            st.dataframe(
                top_records,
                use_container_width=True
            )

        with col2:

            st.markdown(
                "#### 🔻 Bottom 10"
            )

            bottom_records = (
                df
                .sort_values(
                    ranking_column,
                    ascending=True
                )
                .head(10)
            )

            st.dataframe(
                bottom_records,
                use_container_width=True
            )


# =========================================================
# AUTOMATIC INSIGHTS
# =========================================================

elif page == "💡 Automatic Insights":

    st.markdown(
        '<div class="section-title">'
        '💡 Automatic Insights'
        '</div>',
        unsafe_allow_html=True
    )

    insights = []

    # Dataset size

    insights.append(
        f"📋 The dataset contains "
        f"**{len(df):,} rows** and "
        f"**{len(df.columns)} columns**."
    )

    # Missing values

    missing_total = int(
        df.isnull()
        .sum()
        .sum()
    )

    if missing_total == 0:

        insights.append(
            "✅ The dataset has "
            "**no missing values**."
        )

    else:

        insights.append(
            f"⚠️ The dataset contains "
            f"**{missing_total:,} missing values**."
        )

    # Duplicates

    duplicates = int(
        df.duplicated()
        .sum()
    )

    if duplicates == 0:

        insights.append(
            "✅ No duplicate records "
            "were detected."
        )

    else:

        insights.append(
            f"♻️ **{duplicates:,} duplicate "
            f"records** were detected."
        )

    # Numeric insights

    numeric_columns = (
        df
        .select_dtypes(
            include=np.number
        )
        .columns
        .tolist()
    )

    for column in numeric_columns:

        mean_value = df[column].mean()

        max_value = df[column].max()

        min_value = df[column].min()

        insights.append(
            f"📈 **{column}**: "
            f"Average = **{mean_value:.2f}**, "
            f"Minimum = **{min_value:.2f}**, "
            f"Maximum = **{max_value:.2f}**."
        )

        try:

            max_index = (
                df[column]
                .idxmax()
            )

            min_index = (
                df[column]
                .idxmin()
            )

            max_record = df.loc[
                max_index
            ]

            min_record = df.loc[
                min_index
            ]

            # Find a useful text column

            text_columns = (
                df
                .select_dtypes(
                    exclude=np.number
                )
                .columns
                .tolist()
            )

            if text_columns:

                name_column = (
                    text_columns[0]
                )

                max_name = (
                    max_record[name_column]
                )

                min_name = (
                    min_record[name_column]
                )

                insights.append(
                    f"🔝 Highest **{column}**: "
                    f"**{max_name}** "
                    f"({max_value:.2f})."
                )

                insights.append(
                    f"🔻 Lowest **{column}**: "
                    f"**{min_name}** "
                    f"({min_value:.2f})."
                )

        except Exception:

            pass

    # Categorical insights

    categorical_columns = (
        df
        .select_dtypes(
            exclude=np.number
        )
        .columns
        .tolist()
    )

    for column in categorical_columns:

        if df[column].nunique() > 0:

            counts = (
                df[column]
                .value_counts()
            )

            top_value = counts.index[0]

            top_count = counts.iloc[0]

            insights.append(
                f"🏆 Most common **{column}**: "
                f"**{top_value}** "
                f"({top_count} records)."
            )

    # Display

    for insight in insights:

        st.info(insight)


# =========================================================
# EXPORT
# =========================================================

elif page == "📥 Export":

    st.markdown(
        '<div class="section-title">'
        '📥 Export'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # CSV DOWNLOAD
    # -----------------------------------------------------

    st.markdown(
        "### 📄 CSV Export"
    )

    csv_data = (
        df
        .to_csv(
            index=False
        )
        .encode("utf-8")
    )

    st.download_button(
        label="⬇️ Download Dataset as CSV",
        data=csv_data,
        file_name="dataset.csv",
        mime="text/csv"
    )

    # -----------------------------------------------------
    # PDF DOWNLOAD
    # -----------------------------------------------------

    st.markdown(
        "### 📄 PDF Report"
    )

    st.write(
        "Generate a PDF containing dataset summary, "
        "data quality, statistics and automatic insights."
    )

    pdf_file = generate_pdf_report(
        df,
        file_name
    )

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_file,
        file_name="data_analysis_report.pdf",
        mime="application/pdf"
    )

    # -----------------------------------------------------
    # EXPORT INFORMATION
    # -----------------------------------------------------

    st.markdown(
        "### 📊 Dataset Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Rows",
            len(df)
        )

    with col2:

        st.metric(
            "Columns",
            len(df.columns)
        )

    with col3:

        st.metric(
            "Missing Values",
            int(
                df.isnull()
                .sum()
                .sum()
            )
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📊 Data Analysis Dashboard | "
    "Python • Pandas • NumPy • Plotly • Streamlit"
)