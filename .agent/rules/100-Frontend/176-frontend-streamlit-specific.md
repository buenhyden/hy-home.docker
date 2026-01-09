---
trigger: always_on
glob: "**/*.py"
description: "Streamlit: Caching, Session State, Modularization, and Layout."
---
# Streamlit Standards

## 1. Caching

- **@st.cache_data**: For serializable data (DataFrames, dicts).
- **@st.cache_resource**: For unserializable objects (DB connections, ML models).
- **Always Cache**: Cache ALL expensive computations.

### Example: Caching

**Good**

```python
@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv("large_file.csv")

df = load_data()  # Only loads once
```

**Bad**

```python
def load_data():
    return pd.read_csv("large_file.csv")

df = load_data()  # Reloads on EVERY interaction
```

## 2. Session State

- **Initialization**: Check `if 'key' not in st.session_state`.
- **Widget Keys**: ALWAYS provide unique `key` for widgets.

### Example: Session State

**Good**

```python
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment"):
    st.session_state.counter += 1
```

## 3. Code Organization

- **Modular**: Separate UI from logic. Use `pages/`, `services/`.
- **Context Managers**: Use `with st.sidebar:`, `with st.columns()[0]:`.

### Example: Layout

**Good**

```python
with st.sidebar:
    st.header("Controls")
    option = st.selectbox("Choose", ["A", "B"])

col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
```

## 4. Widget Keys

- **Unique**: Every widget in loops needs `key=f"widget_{i}"`.
- **Descriptive**: Use descriptive key names for debugging.
