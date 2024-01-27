# Milestone 4 Markdown

## Directory Structure
At the root of our team15_2023 repository, we have three sub-directories: .github/workflows, API_draft, and docs. We also have a README.md file at the root of our repo that includes badges indicating whether our CI workflows are passing or failing. The LICENSE file also lives at the root of our repository.

Within our .github/workflows directory, we have two .yml files, coverage.yml and test.yml.
Within our API_draft directory, we have a schematic diagram of our API schema, as well as a README.md file that details the modules, classes, and functions in our project.
Within our docs directory, we have organized documentation and tutorials for our final package. This includes the current markdown, milestone4.md.

Within the src directory, which lives at our root, there will be the classes and modules we are implementing for our project. We will have a AstroLibrary package that houses our subpackages, specifically MainModule, QueryHandler, DataPreprocessor, MetadataExtractor, and VisualizationHandler. Within these subpackages will be __init__.py files and the corresponding python code for each module. 

## Test Suite
Our test suite will live in a separate directory called tests at the root of our repo. It will include run_coverage.sh, which tests the code coverage, a directory for each sub-package that tests each module within the sub-package.

## Package Distribution
We will create a distribution package to make our Python package available for users to install. Using setuptools, we will create a file called setup.py at the root of our project, which contains metadata about our package and instructions for its distribution. 
We will then upload our package to PyPI so that users can install our package using pip.

## Licensing 
**License:** The MIT License. 
**Our Motivation:** We used the MIT License due to its high permissiveness, simplicity, and widespread adoption. Its minimal restrictions encourage collaboration, compatibility with other licenses, and align with the principles of free and open-source software, promoting the free exchange of ideas and code.

## Other Considerations

**As mentioned in the QueryHandler Module: Advantages/Design Considerations**

- Make the library more user-friendly, as the users only interact with the high-level `QueryHandler` class without needing to understand the underlying details.

- The `QueryHandler` class is dataset-agnostic, i.e. it can be used to query any dataset without having the client/user to memorize specific API calls for each dataset: simply query it with ADQL & SQL.

- This design allows for the addition of new datasets without modifying the existing codebase.

- Can be easily extended to support users' own provided datasets in addition to core ones like SDSS.
