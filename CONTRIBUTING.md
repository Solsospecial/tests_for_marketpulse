# 🤝 Contributing to **NewsSpeed**

We’re excited that you want to contribute to NewsSpeed!
This guide will help you set up your environment, follow our coding standards, and submit great pull requests.

___

## 📌 How You Can Contribute
- Bug Reports – Found an issue? Let us know with clear steps to reproduce.
- Feature Requests – Have an idea? Suggest it in the issues.
- Code Contributions – Improve features, fix bugs, or add new capabilities.
- Documentation – Help make our guides, README, and inline docs clearer.
- Testing – Write or enhance test cases to ensure quality.

___

## 🚀 Getting Started

1️⃣ ### Fork the repository

Click the Fork button at the top right of the **GitHub** page.

2️⃣ ### Clone your fork

git clone https://github.com/yourusername/newsspeed.git
cd newsspeed

3️⃣ Create a virtual environment

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate

4️⃣ Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

___

🛠 Development Workflow
	1.	Create a new branch

git checkout -b feature/your-feature-name


	2.	Make your changes
Follow the coding standards below.
	3.	Run the app locally

streamlit run app.py


	4.	Test your changes
Verify functionality and no existing features are broken.
	5.	Commit changes

git add .
git commit -m "feat: short description of changes"


	6.	Push to your fork

git push origin feature/your-feature-name


	7.	Open a Pull Request
Go to the main repository and submit your PR.

___

📏 Coding Standards
	•	PEP 8 compliance for Python code.
	•	Use meaningful variable/function names.
	•	Keep functions focused — small and specific.
	•	Document public functions with concise docstrings.
	•	Avoid hardcoding values — use configuration where possible.
	•	Commit messages:
	•	feat: for new features
	•	fix: for bug fixes
	•	docs: for documentation changes
	•	refactor: for code restructuring
	•	test: for adding/updating tests

___

🧪 Testing Guidelines
	•	Test all new features before submitting a PR.
	•	Ensure existing tests still pass:

pytest


	•	Write unit tests for new modules/functions.
	•	Avoid introducing breaking changes without discussion.

___

🔍 Pull Request Checklist

Before submitting a PR:
	•	Code follows PEP 8
	•	Commit messages are clear and conventional
	•	All tests pass locally
	•	Documentation updated if needed
	•	No unused imports or variables

___

📬 Communication
	•	Use **GitHub Issues** for bugs, feature requests, and discussions.
	•	Be respectful and constructive in all interactions.
	•	Large or breaking changes should be discussed before starting work.