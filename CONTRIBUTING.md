# Contributing to Maketree

First off, thank you for your interest in contributing to Maketree! I appreciate your efforts to help improve the project and make it even more useful for developers around the world.

## How to Contribute

There are several ways to contribute to Maketree:

-   Reporting issues
-   Proposing new features
-   Submitting pull requests with code improvements or tests
-   Improving documentation

### Reporting Issues and Proposing Features

-   **Issues:**  
    If you encounter a bug or have an idea for a new feature, please open an issue in our GitHub repository.

    -   Clearly describe the problem or feature request.
    -   Include any steps needed to reproduce the issue.
    -   Mention your expected versus actual behavior.
    -   Provide as much relevant detail as possible.

-   **Feature Requests:**  
    For new features, describe:
    -   The problem the feature would solve.
    -   How you imagine the solution working.
    -   Any potential drawbacks or challenges.

### Setting Up Your Development Environment

1. **Fork the Repository:**  
   Click the "Fork" button on our GitHub repository to create your own copy.

2. **Clone Your Fork:**

    ```sh
    git clone https://github.com/your-username/maketree-cli.git
    cd ./maketree-cli
    ```

3. **Create Virtual Environment: (Optional)**  
   It's always good practice to create a virtual environment before working on a project.

    ```sh
    python -m venv .venv
    ```

    Then activate the environment: **(Windows)**

    ```sh
    .venv/Scripts/activate
    ```

4. **Install Dev Dependencies:**  
   These dependencies are only for developers. Maketree itself doesn't have any dependency.

    ```sh
    pip install -r requirements.txt
    ```

5. **Create a Branch:**  
   Always create a new branch for your changes:

    ```sh
    git checkout -b your-feature-branch
    ```

6. **Running maketree**  
   Run maketree with this command:
    ```sh
    python ./maketree -h
    ```
    The whole `maketree/` directory acts as a module/package.

### Coding Guidelines

-   **Formatting:**  
    Maketree uses the Black formatter. Please format your code with Black before submitting any changes:

    ```sh
    black .
    ```

-   **Testing:**  
    All contributions must include tests (if applicable) and pass our test suite.

-   **Run tests using pytest:**

    ```sh
    pytest
    ```

-   Make sure all tests pass locally before opening a pull request.
-   Feel free to add or update unit tests if you are adding new features or fixing bugs.

-   **Documentation:**  
    If your changes affect the usage of Maketree, please update the documentation accordingly.

### Making a Pull Request

1. **Commit Your Changes:**

    - Write clear, concise commit messages.
    - Follow best practices for commit messages (e.g., reference issue numbers if applicable).

2. **Push Your Branch:**

    ```sh
    git push origin your-feature-branch
    ```

3. **Open a Pull Request:**

    - Navigate to the GitHub repository and open a pull request from your branch.
    - Provide a clear description of the changes.
    - Reference any related issues.
    - I will review your pull request and provide feedback.

### Additional Notes

-   **Best Practices:**  
    Follow industry-standard best practices for coding, testing, and documentation.

-   **Need Help?**  
    If you have questions about contributing or need assistance, please open an issue.

-   **Code of Conduct:**  
    While I don't have a dedicated Code of Conduct file at this time, I expect all contributors to behave respectfully and constructively.

Thank you for contributing to Maketree! Your efforts help create a better tool for everyone.
