## Why the API was modified? 

After considering the clarifications provided in milestone 5 specifications, we decided 
to modify the API to make it more adaptive to the project requirements and 
and well-docummented.

## What changes were made to the API?
- **Adaptability**: The API was modified to be more adaptive to the project requirements.
  In this way, we grouped modules into 4 main parts of the pipeline: `Data Acquisition`, `Data Processing`, `Data Manipulation`, and `Visualization`. Now, the required modules
  falls into one of these categories. This meant that the `query_interface` that used to 
  be a sub-package in milestone 4 is now a sub-sub-package of `Data Acquisition`.

- **Documentation**: The API was modified to have a clear structure broken down into packages, sub-packages, modules, and classes. The API_diagram was also updated to reflect the changes made to the API.

- **Integration**:
  In this milestone, we focused on integrating the adjacent Annex A modules that falls 
  withing the `Data Acquisition` sub-package: namely, `query_handler` and `spectra_data_retrieval`.
