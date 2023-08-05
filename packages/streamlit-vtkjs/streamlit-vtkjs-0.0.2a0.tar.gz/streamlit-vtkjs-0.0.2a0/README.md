# streamlit-vtkjs
A streamlit component for viewing vtkjs files.


## Local development

### Install frontend dependencies

```
cd streamlit_vtkjs/frontend
npm i
npm start build
```

### Install Python package

Until this package is deployed to PyPI you can install the package locally from inside
this folder after cloning the repository.

1. Open `streamlit_vtkjs/__init__.py` and change `_RELEASE` to `True`.
1. Try `pip install -e .`


Next, in a separate terminal window, create a virtual environment, install streamlit and run the python server.
```
pip install streamlit
streamlit run streamlit_vtkjs/__init__.py
```

## Including the component in a Streamlit app

```python
import pathlib
from streamlit_vtkjs import st_vtkjs

vtk_js_file = pathlib.Path('path/to/file.vtkjs')
st_vtkjs(inf.read_bytes(), menu=True)
```

You can verify that streamlit is properly installed with:

```
streamlit hello
```

[Instructions for publishing a Streamlit component to PyPI](https://docs.streamlit.io/en/stable/publish_streamlit_components.html#publish-to-pypi)

Have fun!
