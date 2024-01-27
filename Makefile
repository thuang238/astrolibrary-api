default: help

VENV := .tm15/bin
export PATH := $(VENV):$(PATH)

venv: # Create virtual environment if it doesn't exist. (activate with: source .tm15/bin/activate)
	@test -d .tm15 || python3 -m venv .tm15;

.PHONY: help
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done


.PHONY: install test style

install: venv # Install project dependencies.
	@$(VENV)/pip3 install -U -r requirements.txt;


test: # Run all tests.
	@echo "Running tests w/ coverage..."
	@$(VENV)/pytest --cov=src --cov-fail-under=90 tests/;

# Clean up the project.
.PHONY: clean clear

clean: # Clean up cache files and directories (recommended).
	@find . -name "*.pyc" -exec rm -f {} \;
	@find . -name "__pycache__" -type d -exec rm -rf {} +;
	@find . -name ".pytest_cache" -type d -exec rm -rf {} +;
	@find . -name ".mypy_cache" -type d -exec rm -rf {} +;

# -------------- Code Health and cleanliness --------------

# black: It reformats entire code files for consistency and adheres to PEP 8,
#        the style guide for Python code.
# isort: It sorts imports alphabetically, and automatically separated into
#        sections and by type.
# pylint: It checks for errors in Python code, tries to enforce a coding
#         standard and looks for code smells. Also, check for PEP 257 docstring
#         conventions compliance.
# mypy: It's used to enforce type hints and annotations as specified by 
#       PEP 484 and additional typing standards. Its primary use is to catch 
#       certain types of errors in Python code at compile time, before the code is run. 

.PHONY: install-dev-tools
install-dev-tools: # Install code health tools: black, isort, etc.
	@$(VENV)/pip3 install -U -r devtools_requirements.txt

.PHONY: report-issues
report-issues: # Report code health issues (^-^)
	-@$(VENV)/mypy src/;
	-@$(VENV)/pylint src/;

.PHONY: fix-style
fix-style: # Fix style issues :)
	@$(VENV)/isort src/ tests/;
	@$(VENV)/black -l 79 src/ tests/;

.PHONY: style
style: # Fix style and then report issues.
	@$(MAKE) fix-style
	@$(MAKE) report-issues
