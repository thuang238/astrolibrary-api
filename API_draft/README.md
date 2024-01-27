# Team 15 Project
### Team members: Hayat Hassan, Rachel Ok, Sam Mucyo, Theresa Huang, Hewan Kidanemariam

# AstroLibrary

AstroLibrary is a library designed for astronomical research, focusing on the classification of stars, galaxies, and QSOs. The library interfaces with Sloan Digital Sky Survey (SDSS) services and other astronomical catalogs, offering a range of functionalities from data acquisition to advanced data manipulation and visualization.

Modified API High-Level Design:
1. Main Package: `src/AstroLibrary`
2. Sub-Packages:
   - Data Acquisition
   - Data Preprocessing
   - Data Manipulation
   - Visualization

## AstroLibrary Main Package:
   - Accepts ADQL query, constraints, and SDSS data, returning processed data.
   - Oversees the entire pipeline from data acquisition to advanced data manipulation and visualization.

### 1. **Data Acquisition Sub-Package:**
- **QueryInterface Sub-Sub-Package:**
  - **QueryHandler Module:**
    - Methods:
     - `run_query`: Run the query from a specified database.
     - `check_status`: Check the status of the query.
     - `get_results`: Get the results of the query.
  - **CrossMatching Module:**
     - Method: 
       - `cross_match` - Cross-reference astronomical objects with specified catalogs.

   - **Other Internal Modules:** 

        `Connector`: A base class for connecting to external databases: SDSS, etc.

        `SDSSConnector`: A class for connecting to SDSS database and APIs.
        
        `ConstraintsParser`: A class for parsing the constraints type of inputs (e.g., redshift, etc.).
    

- **SpectraDataRetrieval Module:**
  - Methods:
    - `get_spectra_data`: Get spectra data from SDSS. 

### 2. **Data Preprocessing Sub-Package:**
   
 - **DataPreprocessing Module:**
   - Class: `DataPreprocessing`
   - Methods:
     - `normalize`: Normalize data
     - `remove_outliers`: Remove outliers
     - `interpolate`: Interpolate data
     - `correct_redshift`: Correct for redshifts
     - `wave_align`: Align spectra wavelengths within a predefined range.

 - **Metadata Extraction Module:**
   - Class: `MetadataExtractor`
   - Method: 
     - `extract_metadata` - Extracts relevant metadata from the preprocessed spectra.

### 3. **Data Manipulation Sub-Package:**

 - **Machine Learning Module:**
   - Class: `Classifier`
   - Methods:
     - `fit`: Train the model
     - `predict`: Predict the class of astronomical objects.
     - `predict_proba`: Predict the class probabilities of astronomical objects.
     - `evaluate`: Evaluate the model performance by reporting the confusion matrix, among other metrics.


### 4. **Visualization Sub-Package:**

   - **SpectralVisualization Module:**
     - Methods:
       - `plot_spectra`: Plot spectral data with Matplotlib
       - `overlay`: Add an overlay on the inferred continuum.



This framework offers a systematic and modular strategy for building the astronomical research library. Each module is designed to handle distinct aspects of data processing, analysis, or additional features. The central module orchestrates the interaction and data flow between specialized modules, fostering adaptability, ease of maintenance, and the potential for future library expansion.


