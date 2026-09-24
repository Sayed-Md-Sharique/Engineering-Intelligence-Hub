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

# Store uploaded document names
if "documents" not in st.session_state:
    st.session_state.documents = []


# ---------------- Upload ----------------

uploaded_files = st.file_uploader(
    "Upload documents or source-code files",
    type=[
        "pdf", "txt", "md", "py", "js", "ts",
        "java", "cpp", "c", "h", "json",
        "yaml", "yml"
    ],
    accept_multiple_files=True
)

if st.button("Upload Documents"):

    if not uploaded_files:
        st.warning("Please select at least one file.")

    else:
        for uploaded_file in uploaded_files:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue()
                )
            }

            try:
                response = requests.post(
                    f"{api_url}/ingest",
                    files=files,
                    timeout=120
                )

                if response.ok:

                    data = response.json()

                    if uploaded_file.name not in st.session_state.documents:
                        st.session_state.documents.append(
                            uploaded_file.name
                        )

                    st.success(
                        f"{data['file']} uploaded successfully. "
                        f"Created {data['chunks']} chunks."
                    )

                else:
                    st.error(
                        f"Upload failed for "
                        f"{uploaded_file.name}: "
                        f"{response.text}"
                    )

            except Exception as e:
                st.error(
                    f"Error uploading {uploaded_file.name}: {e}"
                )


# ---------------- Select documents ----------------

st.divider()

if st.session_state.documents:

    selected_documents = st.multiselect(
        "Select document(s) to search",
        options=st.session_state.documents,
        default=st.session_state.documents[-1:]
    )

else:

    selected_documents = []

    st.info(
        "Upload a document first, then select the document "
        "you want to ask questions about."
    )


# ---------------- Ask question ----------------

question = st.text_area(
    "Ask a question",
    placeholder="How does authentication work?"
)

if st.button("Ask Question"):

    if not question:
        st.warning("Please enter a question.")

    elif not selected_documents:
        st.warning(
            "Please select at least one document."
        )

    else:

        try:

            response = requests.post(
                f"{api_url}/query",
                params=[
                    ("question", question)
                ] + [
                    ("sources", source)
                    for source in selected_documents
                ],
                timeout=120
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

        except Exception as e:
            st.error(
                f"Error connecting to backend: {e}"
            )