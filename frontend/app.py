import streamlit as st
import requests

st.set_page_config(
    page_title="Engineering Intelligence Hub",
    page_icon="🔎"
)

st.title("🔎 Engineering Intelligence Hub")

st.write(
    "Upload engineering documents or source code "
    "and ask questions about them."
)

api_url = st.sidebar.text_input(
    "Backend URL",
    "https://engineering-intelligence-hub.onrender.com"
)

uploaded_files = st.file_uploader(
    "Upload documents or source-code files",
    type=[
        "pdf", "txt", "md", "py", "js", "ts",
        "java", "cpp", "c", "h", "json", "yaml", "yml"
    ],
    accept_multiple_files=True
)

if st.button("Upload Documents"):
    if not uploaded_files:
        st.warning("Please select at least one document.")
    else:
        for uploaded_file in uploaded_files:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue()
                )
            }

            response = requests.post(
                f"{api_url}/ingest",
                files=files
            )

            if response.ok:
                data = response.json()

                st.success(
                    f"{data['file']} uploaded successfully. "
                    f"Created {data['chunks']} chunks."
                )
            else:
                st.error(
                    f"Failed to upload {uploaded_file.name}: "
                    f"{response.text}"
                )

st.divider()

question = st.text_area(
    "Ask a question",
    placeholder="How does authentication work?"
)

if st.button("Ask Question"):
    if not question:
        st.warning("Please enter a question.")
    else:
        response = requests.post(
            f"{api_url}/query",
            params={"question": question}
        )

        if response.ok:
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources")

            for source in data["sources"]:
                st.write(f"• {source}")
        else:
            st.error(response.text)
