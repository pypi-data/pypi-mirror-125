# streamlit-vtkjs
A streamlit component for viewing vtkjs files.


## Installation

`pip install streamlit-vtkjs`

## Local development

### Install frontend dependencies

```
cd streamlit_vtkjs/frontend
npm i
npm start build
```

### Install Python package

Install the package locally from inside this folder after cloning the repository.

`pip install -e .`


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

Have fun!


## Release to PyPI

Here is the manual process to release the app to PyPI as a reference for setting up the
CI.

### Create the build folder for frontend

```
cd streamlit_vtkjs/frontend
npm i
npm run build
```

### Bump the version

Open `setup.py` and bump the version.

### Build the package and push it to PyPI

```
python setup.py sdist bdist_wheel
twine upload dist/* -u $PYPI_USERNAME -p $PYPI_PASSWORD
```
