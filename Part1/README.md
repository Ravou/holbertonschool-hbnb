# HBNB UML Diagrams

This repository contains the **UML diagrams** for the HBNB project, part of the Holberton School AirBnB clone. It provides a structured and visual overview of the system architecture and behavior, focusing on clarity, modularity, and documentation.

---

## 📑 Table of Contents

- [🧩 About This Project](#-about-this-project)
- [📁 Project Structure](#-project-structure)
- [🎯 Objectives](#-objectives)
- [🛠️ Tools Used](#️-tools-used)
- [📚 Contents](#-contents)
- [📌 Focus Areas](#-focus-areas)
- [✅ Status](#-status)
- [📎 How to Use](#-how-to-use)
- [👨‍💻 Author](#-author)
- [📝 License](#-license)

---

## 🧩 About This Project

In this task, you will bring together three types of UML diagrams into a single, well-organized document that represents the overall structure and behavior of the HBNB system:

- A **high-level package diagram** to show the modular organization of the project.
- A **detailed class diagram** focusing on the Business Logic layer, describing the main entities, attributes, and relationships.
- One or more **sequence diagrams** illustrating the step-by-step process of API calls (e.g., creating a `Place`, linking `Amenities`, validating input).

The goal is to provide a complete visual overview that supports both documentation and system understanding for developers and reviewers.

---

## 📁 Project Structure

This repository includes the following diagrams:

- **Package Diagram**: Shows the organization of packages/modules and their dependencies.
- **Class Diagram**: Focused on the Business Logic layer, including main classes like `User`, `Place`, `City`, `State`, `Review`, and `Amenity`.
- **Sequence Diagrams**: Demonstrate API workflows such as creating a new Place and validating user input.

---

## 🎯 Objectives

- Provide a clear **visual representation** of the HBNB system architecture.
- Clarify the **object-oriented structure** and **API interactions** within the application.
- Support documentation and help developers understand system flows and relationships.

---


## 🛠️ Tools & Technologies

- Ubuntu 22.04 LTS
- Python 3
- GitHub
- Markdown for documentation
- [draw.io](https://drawio.com) for diagrams
- [Mermaid](https://mermaid-js.github.io/) for diagram syntax in Markdown


---

## 📚 Contents

| Diagram Type      | File Name                        | Description                                          |
|-------------------|----------------------------------|------------------------------------------------------|
| Package Diagram   | `package_diagram.png`            | Overview of modules and package relationships        |
| Class Diagram     | `class_diagram_business.png`     | Core classes of the Business Logic layer             |
| Sequence Diagram  | `sequence_create_place.png`      | API flow: Create Place with amenities and validation |
| Sequence Diagram  | `sequence_get_user_reviews.png`  | API flow: Get user reviews for a Place               |
| Sequence Diagram  | ...                              | ...                                                  |

---

## 📌 Focus Areas

- **Layer separation**: presentation, business logic, data access.
- **Entity relationships**: inheritance, composition, and association.
- **Realistic use cases** via API sequence diagrams.
- **Scalability** and **modularity** through clear packaging.

---

## ✅ Status

- ✅ Diagrams created and reviewed
- ✅ Organized and documented in Markdown
- 📝 Ready to be included in the main AirBnB clone documentation or wiki

---

## 📎 How to Use

1. Clone the repository: https://github.com/Ravou/holbertonschool-hbnb.git

2. Open the diagram files using your prefered UML viewer or any web browser.

3. Use the diagrams for documentation, development guidance, or team onboarding.

##  👩🏾Author

- Olivia Letchy - @Ravou

## 📝 License

```
This project is licensed under the MIT License. 

You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, provided that the original license notice is included in all copies or substantial portions of the Software.

> Copyright (c) 2025 Ravou  
>  
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```
