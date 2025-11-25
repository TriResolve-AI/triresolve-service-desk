# TriResolve AI – Streamlit Application

This folder contains the full **UI layer** for the TriResolve AI Service Desk platform. It includes the main app shell, multi-page navigation, UI components, and custom styling.

The purpose of this README is to help contributors quickly understand **how the Streamlit UI is structured, how it works, how to extend it, and where new files should go.**

---

## 📁 Folder Structure

```text
streamlit/
├── streamlit_app.py        # Main entry point
├── pages/                  # Auto-loaded subpages
│   ├── 1_Maps.py
│   ├── 2_Assistant.py
│   └── 3_About.py
├── styles/
│   └── theme.css           # Custom CSS overrides
└── assets/                 # (Optional) images, icons, logos
```

---

## 🧠 How the App Works

### **Main Entry File** — `streamlit_app.py`
- Sets up page config (title, icon, layout)
- Injects the global CSS theme
- Renders the Overview / Home page
- Displays real-time system status
- Controls optional sidebar behavior

This file acts as the **home page** of the entire UI.

---

## 📄 Pages System (Sidebar Navigation)

Streamlit automatically loads files inside `/pages`, in alphabetical or numerical order.

### 🔢 Naming Convention
Use numeric prefixes to control order:

```text
1_PageName.py
2_AnotherPage.py
3_FinalPage.py
```

Inside each page:

```python
import streamlit as st

st.title("Your Page Title")
st.write("Your page content here...")
```

Pages should remain **lightweight**, with heavier logic handled in backend or utils modules.

---

## 🎨 Styling & Theme System

Custom global UI styles live in:

```text
streamlit/styles/theme.css
```

Use this file to override Streamlit defaults:
- Typography
- Colors
- Layout spacing
- Sidebar appearance
- Buttons, tables, badges

It's automatically injected via:

```python
with open("streamlit/styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

---

## ➕ Adding a New Page

1. Create a new file inside `/streamlit/pages/`
2. Use the correct prefix:
```text
4_MyNewPage.py
```
3. Add content:
```python
import streamlit as st

st.title("My Cool Feature")
st.write("This will appear in the sidebar automatically.")
```
4. Commit → Push → Open PR

Streamlit will automatically load the page.

---

## 🧩 Adding Assets (Images, Icons, Logos)
Place them in:

```text
streamlit/assets/
```

Then load them via:

```python
st.image("streamlit/assets/my_logo.png")
```

---

## 🧪 Local Development

Run the Streamlit app locally:

```bash
streamlit run streamlit/streamlit_app.py
```

The app auto-reloads whenever a file is saved.

---

## 🤝 Contribution Guidelines
- Follow the folder structure and naming conventions
- Keep UI logic modular
- Document new UI components
- Match the existing design styles
- Avoid large PRs—submit focused updates
- Include screenshots in UI-related PRs

---

## 🗺️ Auto-Generated Architecture Diagram (Text-Based)

A clean, auto-rendering architectural diagram for the Streamlit UI:

```text
                           ┌─────────────────────────────┐
                           │      Streamlit Frontend      │
                           └──────────────┬──────────────┘
                                          │
                 ┌────────────────────────┴────────────────────────┐
                 │                                                 │
      ┌──────────────────────┐                        ┌───────────────────────┐
      │   streamlit_app.py   │                        │     /pages/ Module     │
      └───────────┬──────────┘                        └──────────┬────────────┘
                  │                                              │
      Injects CSS │                                 Auto-loads pages based on
      Renders Home │                                 naming (1_, 2_, 3_, ...)
                  │                                              │
                  ▼                                              ▼
        Global UI Rendering                             Individual Page UI

                 ┌────────────────────────┬────────────────────────┐
                 │                        │                        │
        ┌────────▼────────┐     ┌─────────▼────────┐     ┌────────▼─────────┐
        │   /styles/ CSS   │     │   /assets/ imgs   │     │  /workflows (if) │
        └──────────────────┘     └───────────────────┘     └───────────────────┘
```

---

## 🚀 Quickstart Summary (Add into Quickstart.md)

Add this section under a new header: **Streamlit Frontend Setup**

```markdown
## 🖥️ Streamlit Frontend Setup

The TriResolve AI UI is built using Streamlit and lives entirely inside the `/streamlit` folder.

### 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Run the app locally
```bash
streamlit run streamlit/streamlit_app.py
```

### 📁 Key Structure
```text
streamlit/
├── streamlit_app.py  # Main UI shell
├── pages/            # Auto-loaded sidebar pages
├── styles/           # Global CSS overrides
└── assets/           # Logos, images
```

### 🧩 Adding a New Page
1. Create: `streamlit/pages/4_NewFeature.py`
2. Add your UI code
3. Commit and push

Streamlit auto-detects the page.
```

---

## 🎉 You're Ready!
Your Streamlit UI is now fully documented and structured for collaboration.

If you'd like, I can:
- Add contributor badges
- Create a Wiki version
- Add diagrams in SVG
- Sync this README with the main repo

