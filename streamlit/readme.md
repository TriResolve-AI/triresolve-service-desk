# TriResolve AI – Streamlit Application


This folder contains the full **UI layer** for the TriResolve AI Service Desk platform.  
It includes the main app shell, multi-page navigation, page components, and custom styling.

The goal of this README is to help collaborators quickly understand **how the Streamlit UI is organized, how to extend it, and where to place new files.**

---

## 📁 Folder Structure

```text
streamlit/
├── streamlit_app.py        # Main entry point / home page
├── pages/                  # Auto-loaded sidebar pages
│   ├── 1_Maps.py
│   ├── 2_Assistant.py
│   └── 3_About.py
├── styles/
│   └── theme.css           # Global CSS overrides
└── assets/                 # (Optional) images, icons, logos
````

---

## 🧠 How the App Works

### Main Entry File – `streamlit_app.py`

* Defines the page config (title, icon, layout)
* Injects global CSS from `styles/theme.css`
* Controls sidebar navigation behavior
* Renders the **Overview / home** content
* Displays high-level system status badges / links

This file acts as the **shell and home page** for the TriResolve UI.

---

## 📄 Pages System (Sidebar Navigation)

Streamlit auto-detects files inside `streamlit/pages` and displays them in the sidebar.

### Naming Convention

Use numeric prefixes to control order:

```text
1_Maps.py
2_Assistant.py
3_About.py
4_YourNewPage.py
```

Inside each page:

```python
import streamlit as st

st.title("My Page Title")
st.write("This is where your content goes.")
```

As soon as the file exists in `/pages` and follows the naming pattern, Streamlit will show it automatically.

---

## 🎨 Styling & Theme System

Custom UI styles live in:

```text
streamlit/styles/theme.css
```

Use this file to tweak:

* Typography (font sizes, headings, body text)
* Layout spacing (margins, paddings)
* Badge / chip / tag colors
* Sidebar and header styling
* Buttons, tables, cards, etc.

`streamlit_app.py` injects the CSS:

```python
with open("streamlit/styles/theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

Edit `theme.css`, save, and the app will pick up changes on reload.

---

## 🧩 Assets (Logos, Images, Icons)

Place shared UI assets in:

```text
streamlit/assets/
```

Use them in pages like:

```python
import streamlit as st

st.image("streamlit/assets/logo.png", use_column_width=True)
```

---

## ⚙️ Install Dependencies

> 🔎 **Note for reviewers / contributors**
> The Streamlit UI depends on the `streamlit` package. Make sure it’s included in your
> environment before running the app.

If you’re using a single repo-wide `requirements.txt`, ensure it contains **`streamlit`**:

```text
streamlit
fastapi
uvicorn
python-dotenv
requests
```

Then install:

```bash
pip install -r requirements.txt
```

If you keep a separate requirements file for the UI (for example `streamlit/requirements.txt`):

```bash
pip install -r streamlit/requirements.txt
```

---

## ▶️ Running the Streamlit App

From the **repository root**:

```bash
streamlit run streamlit/streamlit_app.py
```

* Default URL: `http://localhost:8501`
* The app auto-reloads when you save Python files in `streamlit/`.

---

## ➕ Adding a New Page

1. Create a new file in:

   ```text
   streamlit/pages/
   ```

2. Name it with a numeric prefix for ordering:

   ```text
   4_Ticket_Analytics.py
   ```

3. Add page content:

   ```python
   import streamlit as st

   st.title("Ticket Analytics")
   st.write("This page shows analytics for HR / IT / Finance tickets.")
   ```

4. Save the file and refresh the browser (or let Streamlit auto-reload).

That’s it — it appears in the sidebar under its numeric position.

---

## 🏗 Streamlit UI Architecture

### ASCII Overview

```text
                           ┌─────────────────────────────┐
                           │     TriResolve UI (Web)     │
                           └──────────────┬──────────────┘
                                          │
                                          ▼
                               streamlit_app.py
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   │                                             │
            Global shell & CSS                           Auto-loaded pages
              (layout, theme)                               (/pages/*.py)
                   │                                             │
                   ▼                                             ▼
          styles/theme.css                              1_Maps.py, 2_Assistant.py,
          assets/* (logos, imgs)                        3_About.py, 4_*.py, ...
```

---

### Mermaid Diagram (for GitHub Rendering)

> ℹ️ GitHub supports Mermaid in Markdown.
> This will render as a diagram in the repo.

```mermaid
flowchart TD
    U[User in Browser] --> ST[Streamlit UI]

    ST --> APP[streamlit_app.py<br/>Shell + Home]
    APP --> CSS[styles/theme.css]
    APP --> ASSETS[assets/ (logos, images)]

    APP --> PAGES[/pages folder/]
    PAGES --> P1[1_Maps.py]
    PAGES --> P2[2_Assistant.py]
    PAGES --> P3[3_About.py]
    PAGES --> Pn[4_*.py (future pages)]
```

If you later wire this to the FastAPI backend, you can extend the diagram to show:

```mermaid
flowchart LR
    U[User] --> ST[Streamlit UI]
    ST --> API[(FastAPI Service Desk API)]
    API --> AGENTS[Multi-Agent Layer (HR / IT / Finance)]
```

---

## 🤝 Contribution Notes

When contributing to the Streamlit UI:

* **Keep pages focused** – one major concern per file (maps, assistant, about, etc.)
* **Avoid heavy business logic** in Streamlit files; call backend functions / APIs instead.
* **Use consistent naming** with numeric prefixes (`N_Name.py`).
* **Update docs** if you add new sections, navigation patterns, or reusable UI components.
* When opening a PR:

  * Include a short description of the UI change
  * Add screenshots or a short Loom if the layout changed
  * Tag relevant teammates for review

---

## 📌 Quick Reference

* Docs you are reading: `streamlit/README.md`
* Quickstart for running UI only: `streamlit/Quickstart.md` (see separate file)
* App entrypoint: `streamlit/streamlit_app.py`
* Sidebar pages: `streamlit/pages/*.py`
* CSS: `streamlit/styles/theme.css`
* Assets: `streamlit/assets/`

````

---

## 2️⃣ Separate Streamlit Quickstart File

Here’s a **standalone Quickstart** you can upload as a new file  
(e.g. `streamlit/Quickstart.md`):

```markdown
# TriResolve AI – Streamlit Quickstart

This Quickstart explains how to **install**, **run**, and **extend** the TriResolve AI Streamlit UI.

The Streamlit frontend lives in the `/streamlit` folder and provides the multi-page UI
for the Service Desk experience.

---

## 1️⃣ Prerequisites

- Python 3.10+ (recommended)
- `pip` (or `pipenv` / `poetry`)
- A clone of the `triresolve-service-desk` repository

From the repo root:

```bash
cd triresolve-service-desk
````

---

## 2️⃣ Install Dependencies

Make sure `streamlit` is installed (either via `requirements.txt` or directly).

### Option A – Using `requirements.txt` (recommended)

Ensure your requirements file contains `streamlit`:

```text
streamlit
fastapi
uvicorn
python-dotenv
requests
```

Then run:

```bash
pip install -r requirements.txt
```

### Option B – Direct install for UI only

If you just want to run the UI quickly:

```bash
pip install streamlit
```

(Plus any other libraries your pages import.)

---

## 3️⃣ Streamlit Folder Layout

```text
streamlit/
├── streamlit_app.py        # Main entry point / home
├── pages/                  # Auto-loaded sidebar pages
│   ├── 1_Maps.py
│   ├── 2_Assistant.py
│   └── 3_About.py
├── styles/
│   └── theme.css           # Global CSS overrides
└── assets/                 # (Optional) images, icons, logos
```

---

## 4️⃣ Run the Streamlit App

From the **repository root**:

```bash
streamlit run streamlit/streamlit_app.py
```

* Default URL: `http://localhost:8501`
* Auto-reloads on file save (dev-friendly).

---

## 5️⃣ Add a New Page

1. Create a file in:

   ```text
   streamlit/pages/
   ```

2. Name it with a numeric prefix:

   ```text
   4_MyNewFeature.py
   ```

3. Add minimal content:

   ```python
   import streamlit as st

   st.title("My New Feature")
   st.write("This page was added via the Streamlit Quickstart.")
   ```

4. Save → the new page appears in the sidebar automatically.

---

## 6️⃣ Customize the Theme

Global styling lives in:

```text
streamlit/styles/theme.css
```

Typical edits:

* Colors for headers / highlights / badges
* Font sizes & line-height
* Padding / spacing between sections
* Button and card styles

`streamlit_app.py` is already wired to inject this CSS at startup.

---

## 7️⃣ Architecture Snapshot

### ASCII View

```text
User Browser
    │
    ▼
Streamlit App (streamlit_app.py)
    │
    ├── Inject CSS from styles/theme.css
    ├── Show Overview / Home
    └── Load Pages from /pages
            ├── 1_Maps.py
            ├── 2_Assistant.py
            └── 3_About.py
```

### Mermaid View (for GitHub)

```mermaid
flowchart TD
    U[User in Browser] --> ST[Streamlit Frontend]

    ST --> APP[streamlit_app.py]
    APP --> CSS[styles/theme.css]
    APP --> ASSETS[assets/]

    APP --> PAGES[/pages/ folder]
    PAGES --> P1[1_Maps.py]
    PAGES --> P2[2_Assistant.py]
    PAGES --> P3[3_About.py]
    PAGES --> P4[4_YourNewFeature.py]
```

---

## 8️⃣ Troubleshooting

**❓ `ModuleNotFoundError: No module named 'streamlit'`**

* Run: `pip install streamlit`
* Or re-run: `pip install -r requirements.txt` and confirm `streamlit` is listed.

**❓ New page not showing**

* Ensure filename starts with a number (`4_YourNewFeature.py`).
* Confirm it’s under `streamlit/pages/`.
* Save the file and refresh the browser.

**❓ CSS not applying**

* Check path: `streamlit/styles/theme.css`
* Ensure the CSS injection block is present in `streamlit_app.py`.

---

You’re ready to build on the **TriResolve AI Streamlit UI**.


````
