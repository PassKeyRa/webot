# WeBot

This is a [Telegram](https://telegram.org/) bot that helps you to publish your chats in the web.

With the help of this bot you will be able to easily access your messages in your favorite web browser.

## TOC

- 1. [TOC](#toc)
- 2. [Development plan](#development-plan)
  - 2.1. [Business Goals and Objectives](#business-goals-and-objectives)
  - 2.2. [Roles and responsibilities](#roles-and-responsibilities)
  - 2.3. [Project Glossary](#project-glossary)
  - 2.4. [Technical Stack](#technical-stack)
  - 2.5. [Requirement Analysis and Specifications](#requirement-analysis-and-specifications)
    - 2.5.1. [Features](#features)
    - 2.5.2. [User Stories](#user-stories)
  - 2.6. [Quality Attributes](#quality-attributes)
  - 2.7. [Constraints](#constraints)
  - 2.8. [Architecture](#architecture)
  - 2.9. [Prototype Screenshots](#prototype-screenshots)
  - 2.10. [Installation and run](#installation-and-run)
  - 2.11. [Software Development Plan](#software-development-plan)
- 3. [Authors](#authors)
- 4. [Problem](#problem)

## Development plan

### Business Goals and Objectives

- We will make paid software without ads.
- We plan to make this app available with paid subscriptions.
- We plan to make this app widely used around the world (with help of ads).
- We will make deploying infrastructure as simple as possible.
- We plan to expand the capabilities of the application over time.

### Roles and responsibilities

| Stakeholder's Name | Roles             | Responsibilities                        |
| ------------------ | ----------------- | --------------------------------------- |
| Developer          | Backend engineer  | Telegram bot development                |
|                    | Backend engineer  | Backend development                     |
|                    | DevOps engineer   | Deployment                              |
|                    | Frontend engineer | Frontend development                    |
|                    | QA                | Requirement analysis                    |
| Manager            | Product manager   | Create plan                             |
|                    | Product owner     | Determine user stories                  |
|                    | Product owner     | Determine business goals and objectives |

### Project Glossary

- Backend - Part of code that is not visible to end user
- Frontend - Part of code with which end user directly interacts
- Unit test - a piece of code that checks whether another piece of code works as expected
- Admin - a user that has “admin” role in telegram chat
- DevOps - assistance in integrating development and operation
- QA - quality assurance of code and infrastructure
- Chat update - receiving a new message and adding it to the database
- Bot - an automated tool that is added to the telegram chat and publishes a link to the web interface with messages from the chat

### Technical Stack

- [Azure](https://azure.microsoft.com/) hosting server
- [AWS SQS](https://aws.amazon.com/ru/sqs/) queue service
- [Python](https://www.python.org/) programming language
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework
- [Docker](https://docs.docker.com/desktop/) container runtime
- [Docker-Compose](https://docs.docker.com/compose/) container orchestrator
- [Pytest](https://pytest.org/) testing library
- [MongoDB](https://www.mongodb.com/) database
- [Bootstrap](https://getbootstrap.com/) css framework
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) programming language
- [Telegram](https://telegram.org/) messaging platform for bot
- [SonarQube](https://www.sonarqube.org/) code style and errors checker
- [Flake8](https://gitlab.com/pycqa/flake8) code style and errors checker (with github actions integration)

### Requirement Analysis and Specifications

#### Features

| ID  | User Story Title  | Priority |
| --- | ----------------- | -------- |
| 1   | Chat publication  | Must     |
| 2   | Web chat reading  | Must     |
| 3   | Access control    | Normal   |
| 4   | Admin rights      | Normal   |
| 5   | Chat updates      | Low      |
| 6   | Media processing  | Low      |
| 7   | Publishing rights | Low      |

#### User Stories

| Status        | User Type    | User Story Title  | User Stories                                                                               |
| ------------- | ------------ | ----------------- | ------------------------------------------------------------------------------------------ |
| **Done**      | Chat Admin   | Chat publication  | As a chat admin I want to publish my chat in the internet with telegram bot                |
| **Done**      |              | Access control    | As a chat admin I want to be the only want who can publish the chat                        |
| `TODO`        |              | Admin rights      | As a chat admin I want to be able to revoke access to chat in web                          |
| `TODO`        | Chat User    | Chat updates      | As a user I want the chat to update automatically                                          |
| `TODO`        |              | Media processing  | As a user I want to see not only text messages but also assets such as videos and pictures |
| _In progress_ |              | Web chat reading  | As a user I want to read chat messages from published chat in web browser                  |
| `TODO`        | Legal Lawyer | Publishing rights | As a copywriter I want to be able to complain about the materials in published chats       |

### Quality Attributes

| Characteristics        | Sub-Characteristics Definition | How we will achieve it                                                                                                                  |
| ---------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Usability              | User interface aesthetics      | Client will use Telegram app user interface to communicate with our bot                                                                 |
| Reliability            | Recoverability                 | Bot should be able to recover in case of crash or failure automatically (automatic restart)                                             |
| Reliability            | Fault tolerance                | At least some nodes of bot should be available at any time (replication)                                                                |
| Security               | Confidentiality                | The published chat history is available for viewing by users who followed the link                                                      |
| Performance Efficiency | Time-behavior                  | Maximum load time should not be bigger than 5 s. To achieve this we need to test load speeds of the app and optimize the code if needed |

### Constraints

- Do not store more than 5000 messages per chat
- The bot should not read chats for which it does not have permission
- The bot should not publish chats unless an admin asked him to do it
- The bot should not publish chats if admin haven’t paid for the subscription

### Architecture

[Link to the board](https://miro.com/app/board/o9J_lzxVDsw=)

### Prototype Screenshots

![1](https://i.ibb.co/1sMw7wT/screen01.jpg)
![2](https://i.ibb.co/Tbv0j0K/screen02.jpg)

### Installation and run

To run, pull this repository and create two `.env` files in `api/` and `bot/` directory:

```bash
api/.env
AWS_ACCESS_KEY_ID=<>
AWS_SECRET_ACCESS_KEY=<>
REGION_NAME=<>
QUEUE_NAME_IN=<>
QUEUE_NAME_OUT=<>
MONGODB_URL=<>
```

```bash
bot/.env
AWS_ACCESS_KEY_ID=<>
AWS_SECRET_ACCESS_KEY=<>
REGION_NAME=<>
API_ID=<>
API_HASH=<>
```

Then you can build Docker Images:

```bash
docker-compose build
```

And finally start instances (by default backend listen on port `51212`, but you have access to `docker-compose.yml` file):

```bash
docker-compose up -d
```

### Software Development Plan

| Status        | **Inception Phase**    |                         |                    |                                                                                                                                   |                                                                                                                                        |
| ------------- | ---------------------- | ----------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
|               | # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts                                                                                                                              |
| **Done**      | 1                      | 25/08/2021 - 26/08/2021 | Manager            | Determine Business goals and objectives with valid justification, Identify the stakeholders, Establish roles and responsibilities | Deliver the documentation of achieved milestones                                                                                       |
| **Done**      | 2                      | 25/08/2021 - 26/08/2021 | Developer          | Requirement engineering (20% user stories)                                                                                        | Update the documentation of achieved milestones with User stories                                                                      |
|               | **Elaboration Phase**  |                         |                    |                                                                                                                                   |                                                                                                                                        |
|               | # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts                                                                                                                              |
| **Done**      | 1                      | 25/08/2021 - 26/08/2021 | Manager            | Revise User Stories (100%)                                                                                                        | Document 100% user stories                                                                                                             |
| **Done**      | 2                      | 25/08/2021 - 26/08/2021 | Developer, Manager | Software development planning                                                                                                     | Iteration Plan                                                                                                                         |
| **Done**      | 3                      | 25/08/2021 - 26/08/2021 | Developer          | Software Architecture, Test Plan                                                                                                  | Software architecture document, Test Plan Document                                                                                     |
| **Done**      | 4                      | 25/08/2021 - 26/08/2021 | Developer, Manager | Transition plan                                                                                                                   | Transition plan document                                                                                                               |
|               | **Construction Phase** |                         |                    |                                                                                                                                   |                                                                                                                                        |
|               | # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts                                                                                                                              |
| **Done**      | 1                      | 30/08/2021 - 12/09/2021 | Developer          | Implement Chat publication, Unit test cases                                                                                       | Telegram chat bot, Unit test results                                                                                                   |
| **Done**      | 1                      | 30/08/2021 - 12/09/2021 | Developer          | Implement Web chat reading, Unit test cases                                                                                       | Simple web page with text messages from the chat, Unit test results for backend                                                        |
| **Done**      | 1                      | 30/08/2021 - 12/09/2021 | Developer          | Implement Access control, Unit test cases                                                                                         | Working feature 1 branch, Unit test results                                                                                            |
| **Done**      | 2                      | 13/09/2021 - 26/09/2021 | Developer          | Implement Admin rights, Unit test cases                                                                                           | Error page, Unit test results                                                                                                          |
| _In progress_ | 2                      | 13/09/2021 - 26/09/2021 | Developer          | Implement Chat updates, Unit test cases                                                                                           | Refreshable page, Unit test results                                                                                                    |
| `TODO`        | 3                      | 27/09/2021 - 03/10/2021 | Developer          | Implement Media processing                                                                                                        | Web page with integrated media viewer                                                                                                  |
| `TODO`        | 3                      | 27/09/2021 - 03/10/2021 | Developer          | Implement Publishing rights                                                                                                       | Documentation of complaint procedure "Fill complaint report" button                                                                    |
|               | **Transition Phase**   |                         |                    |                                                                                                                                   |                                                                                                                                        |
|               | # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts                                                                                                                              |
| `TODO`        | 1                      | 25/09/2021 - 06/10/2021 | Developer          | Integration, end to end testing, training for Users and Developers                                                                | Github repository, merged branches, integration and ended to end test results, final README for developers and Users, deployed product |
| `TODO`        | 2                      | 01/10/2021 - 06/10/2021 | Developer, Manager | Final product release                                                                                                             | Working Product                                                                                                                        |

### Milestones

| Milestone | Timeline                | Status        |
| --------- | ----------------------- | ------------- |
| Alpha     | 31/08/2021 - 06/09/2021 | **Done**      |
| Beta      | 18/09/2021 - 25/09/2021 | **Done**      |
| Gamma     | 04/10/2021 - 09/10/2021 | _In progress_ |

## Authors

- German Vechtomov
- Alexey Posikera
- Bogdan Kondratev
- Dmitrii Chermnykh

## Problem

Many Telegram chats can be of great benefit to people.

Therefore, many people want to export chats, and publish them - so that people can read and share knowledge in this way.

For this we need a convenient tool that will not need additional actions on the part of the user.
