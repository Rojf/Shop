# [Online market](https://roadmap.sh/projects/scalable-ecommerce-platform)

The project is under development and may not be perfect.

If you want to help with the development. Information will be given below.

## Get involved!

-
-
-

## Stack

- [Make](https://www.gnu.org/software/make/) - a utility designed to automate the conversion of files from one form to another.
- [Poetry](https://python-poetry.org) - it is a dependency management tool in Python projects (analogous to the built-in pip)

## Getting Started

Before you copy the project, go to the directory where you will place the project.


##### Cloning a repository.

First, clone the repository using git:

```bash
git clone https://github.com/Rojf/Shop
cd Shop
```

There are two launch options: Local or docker container.
You can run all the services or one, but for a complete understanding you will need to check the interaction between the services sometimes.


##### Running the application locally

```bash
# Installing dependencies
make local-build

# Launching a docker container..
make local-up
```

##### Stop running applications

How to stop processes using Make. If you need to stop the applications, please run the command:

Exception!!!
The make local-down command was incorrectly processed if it was not run as an administrator. The reason is the kill command.

```bash
make local-down
```


##### Startup in Docker



## Product Roadmap

[Discussion](https://github.com/Rojf/Shop/discussions) | [Roadmap Kanban](https://github.com/Rojf/Shop/projects)


✅ Completed: Finished, available on [production instance](https://example.com)

🔄 In Progress: Task or milestone is actively being worked on

📅 Planned: Task or milestone is scheduled for a future date

Status | Feature | Release
-------|---------|---------
