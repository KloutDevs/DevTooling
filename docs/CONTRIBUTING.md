# Contributing Guidelines

¡Thanks for your interest in contributing to DevTooling CLI! This document provides the guidelines and processes for contributing to the project.

## 🤝 Contributing Process

1. **Fork & Clone**
   - Make a fork of the project
   - Clone your fork to your local machine
   ```bash
   git clone https://github.com/YOUR-USERNAME/devtooling-cli.git
   ```

2. **Configuaation**
   - Install the project dependencies
   ```bash
   pip install -r requirements.txt
   ```
   - Configure the virtual environment (recommended)
   ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Make a new branch**

```bash	   
git checkout -b feature/feature-name
# o
git checkout -b fix/bug-name
```

4. **Coding Conventions**

Without define...

5. **Commits**
   - Ensure of write an detailed and significant commit message
   - Use the format

     ```
    <type>[(scope)]: <description>
    [optional body]
     ```

   - Types: feat, fix, docs, style, refactor, test

   - Examples: `feat(git): add .gitignore create functionality`

6. **Testing**

- Add tests for new features
- Ensure all tests pass
- Maintain or improve test coverage


# 📝 Adding new features

## Detection rules
For add new project types, you need to add a new rule in the detection_rules.json file.

1. Update detection_rules.json 
2. Document the new rule in the README.MD and CHANGELOG.md

## New functionalities

1. Discuss the new feature with the team in issues
2. Follow the project structure
3. Update the docs
4. Add tests

# 🐛 Reporting bugs
1. Use the template in issues
2. Includes:
    - DevTooling CLI version
    - Steps to reproduce
    - Expected behavior and actual behavior
    - Relevants logs

# 📋 Pull Requests

1. Update the CHANGELOG.md
2. Reference relationed issues
3. Update the docs
4. Wait a review
5. Response to the feedback if necessary

# 🚀 Release Process

1. Semantic Versioning (MAJOR.MINOR.PATCH)
2. Update the version in setup.py
3. Update CHANGELOG.md
4. Create an annotated tag

# ⚖️ Code of Conduct

* Be respectful
* Accept constructive feedbacks
* Focus in the best interest of the project community
* Show empathy

# 📮 Contact

- Issues of GitHub
- Discussions of GitHub
- Email: schmidtnahuel09@gmail.com