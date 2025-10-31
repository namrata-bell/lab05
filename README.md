
**Known Issue Table**
| **#** | **Tool**            | **Code / Description**                             | **Line in Old File** | **Fixed?**     | **How It Was Fixed**                                                                           |
| :---: | :------------------ | :------------------------------------------------- | :------------------: | :------------- | :--------------------------------------------------------------------------------------------- |
|   1   | **Bandit / Pylint** | `B110` / `W0702`: Bare `except:` (try/except/pass) |          19          | Yes            | Replaced with `except KeyError as e:` and `except Exception as e:` → proper logging + re-raise |
|   2   | **Bandit / Pylint** | `B307` / `W0123`: Use of `eval()`                  |          59          | Yes            | Removed completely; added comment noting Bandit fix                                            |
|   3   | **Pylint**          | `W0102`: Mutable default argument (`logs=[]`)      |           8          | Yes            | Changed to `logs=None`, with in-function initialization (`if logs is None: logs = []`)         |
|   4   | **Pylint**          | `R1732`: Missing `with` for file I/O               |        26, 32        | Yes            | Replaced manual `open()`/`close()` with `with open(..., encoding="utf-8"):`                    |
|   5   | **Pylint**          | `W1514`: No encoding in open()                     |        26, 32        | Yes            | Added `encoding="utf-8"` explicitly                                                            |
|   6   | **Pylint**          | `W0603`: Use of `global`                           |          27          | Minimized      | Initially required for lab simplicity; later removed entirely via in-place dictionary update   |
|   7   | **Pylint**          | `C0116`: Missing function docstrings               |     All functions    | Yes            | Added concise docstrings for every function                                                    |
|   8   | **Pylint**          | `C0103`: Function name not snake_case              |     All functions    | Yes            | Renamed all functions: e.g., `addItem` → `add_item`, etc.                                      |
|   9   | **Pylint**          | `C0209`: Prefer f-strings                          |          12          | Yes            | Replaced `%` formatting with f-strings                                                         |
|   10  | **Pylint**          | `W0611`: Unused import `logging`                   |           2          | Yes            | Logging module now actively used for structured messages                                       |


**Reflection**


**1. Which issues were the easiest to fix, and which were the hardest? Why?**

Easiest fixes:

Replacing the mutable default list (logs=[]) with None was simple and immediately resolved the W0102 warning.

Updating to f-strings, adding docstrings, and specifying file encoding (utf-8) were straightforward and improved readability.

Removing unused imports and renaming functions to snake_case were purely cosmetic fixes guided directly by Pylint.

Hardest fixes:

Handling the bare except: issue properly required redesigning the error handling to log and raise specific exceptions without breaking logic.

Removing the global statement needed structural thinking — updating the dictionary in place rather than reassigning it.

Eliminating the eval() call safely while preserving intended functionality was also a key security fix.


**2. Did the static analysis tools report any false positives? If so, describe one example.**

No clear false positives appeared after review.

However, Pylint’s earlier flag on the global statement was contextually acceptable for the lab since global variables were used intentionally for simplicity.
In a real project, though, encapsulating state inside a class would remove the need for that entirely.


**3. How would you integrate static analysis tools into your actual software development workflow?**

Continuous Integration (CI):

Integrate Pylint, Flake8, and Bandit into a GitHub Actions or GitLab CI pipeline to run automatically on every pull request.

Example CI snippet:

- name: Static Code Analysis
  run: |
    pylint inventory_system.py
    flake8 inventory_system.py
    bandit -r .


Local Development:

Set up pre-commit hooks to auto-run these tools before each commit.

Enable built-in linting in IDEs like VS Code to catch problems in real time.

This ensures consistent quality and prevents regressions before code merges.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

Security: Removed eval() and added explicit exception handling — eliminating unsafe and unpredictable behavior.

Reliability: Using with open() and specifying encodings prevents file-handling errors and resource leaks.

Readability: PEP8-compliant names, added docstrings, and f-strings improved clarity and maintainability.

Maintainability: Replacing print statements with proper logging provides traceable and configurable output.

Metrics:

Pylint: Improved from 4.8/10 → 10.0/10

Bandit: 0 issues remaining

Flake8: Clean (no warnings)

Overall, static analysis transformed the script from functional but risky into secure, maintainable, and professional-grade code.
