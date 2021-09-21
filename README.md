# WeBot

This is a [Telegram](https://telegram.org/) bot that helps you to publish your chats in the web.

With the help of this bot you will be able to easily access your messages in your favorite web browser.

## TOC

_add TOC here later_

## Development plan

**TODO: REMOVE THE LINK AFTER MIGRATION**
<https://docs.google.com/document/d/1SMETg42oXbHJIspYPbVgaMAqGvKnp5CD/edit>

### Business Goals and Objectives

- We will make paid software without ads.
- We plan to make this app available with paid subscriptions.
- We plan to make this app widely used around the world (with help of ads).
- We will make deploying infrastructure as simple as possible.
- We plan to expand the capabilities of the application over time.

### Roles and responsibilities

| Stakeholder's Name | Roles              | Responsibilities                         |
| ------------------ | ------------------ | ---------------------------------------- |
| German Vechtomov   | DevOPS             | CI, Deployment                           |
|                    | QA                 | Testing                                  |
| Alexey Posikera    | Backend Developer  | Telegram bot development                 |
| Bogdan Kondratev   | Backend Developer  | API development                          |
| Dmitrii Chermnykh  | Frontend Developer | Frontend, UI/UX design, Frontend testing |

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

- [AWS EC2](https://aws.amazon.com/ru/ec2/) hosting server
- [AWS SQS](https://aws.amazon.com/ru/sqs/) queue service
- [Python](https://www.python.org/) programming language
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework
- [MongoDB](https://www.mongodb.com/) database
- [Bootstrap](https://getbootstrap.com/) css framework
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) programming language
- [Telegram](https://telegram.org/) messaging platform for bot

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

| User Type    | User Story Title  | User Stories                                                                               |
| ------------ | ----------------- | ------------------------------------------------------------------------------------------ |
| Chat Admin   | Chat publication  | As a chat admin I want to publish my chat in the internet with telegram bot                |
|              | Access control    | As a chat admin I want to be the only want who can publish the chat                        |
|              | Admin rights      | As a chat admin I want to be able to revoke access to chat in web                          |
| Chat User    | Chat updates      | As a user I want the chat to update automatically                                          |
|              | Media processing  | As a user I want to see not only text messages but also assets such as videos and pictures |
|              | Web chat reading  | As a user I want to read chat messages from published chat in web browser                  |
| Legal Lawyer | Publishing rights | As a copywriter I want to be able to complain about the materials in published chats       |

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

### Software Development Plan

| **Inception Phase**    |                         |                    |                                                                                                                                   |           |
| ---------------------- | ----------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | --------- |
| # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts |
| 1                      | 25/08/2021 - 26/08/2021 | Manager            | Determine Business goals and objectives with valid justification, Identify the stakeholders, Establish roles and responsibilities |           |
| 2                      | 25/08/2021 - 26/08/2021 | Developer          | Requirement engineering (20% user stories)                                                                                        |           |
| **Elaboration Phase**  |                         |                    |                                                                                                                                   |           |
| # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts |
| 1                      | 25/08/2021 - 26/08/2021 | Manager            | Revise User Stories (100%)                                                                                                        |           |
| 2                      | 25/08/2021 - 26/08/2021 | Developer, Manager | Software development planning                                                                                                     |           |
| 3                      | 25/08/2021 - 26/08/2021 | Developer          | Software Architecture, Test Plan                                                                                                  |           |
| 4                      | 25/08/2021- 26/08/2021  | Developer, Manager | Transition plan                                                                                                                   |           |
| **Construction Phase** |                         |                    |                                                                                                                                   |           |
| # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts |
| 1                      | 30/08/2021- 12/09/2021  | Developer          | Implement Chat publication, Unit test cases                                                                                       |           |
| 1                      | 30/08/2021- 12/09/2021  | Developer          | Implement Web chat reading, Unit test cases                                                                                       |           |
| 1                      | 30/08/2021- 12/09/2021  | Developer          | Implement Access control, Unit test cases                                                                                         |           |
| 2                      | 13/09/2021- 26/09/2021  | Developer          | Implement Admin rights, Unit test cases                                                                                           |           |
| 2                      | 13/09/2021- 26/09/2021  | Developer          | Implement Chat updates, Unit test cases                                                                                           |           |
| 3                      | 27/09/2021- 03/10/2021  | Developer          |                                                                                                                                   |           |
| 3                      | 27/09/2021- 03/10/2021  | Developer          |                                                                                                                                   |           |
| **Transition Phase**   |                         |                    |                                                                                                                                   |           |
| # Iteration            | Timeline                | Stakeholder        | Activities                                                                                                                        | Artifacts |
| 1                      |                         |                    |                                                                                                                                   |           |
| 2                      |                         |                    |                                                                                                                                   |           |

## Authors

- German Vechtomov
- Alexey Posikera
- Bogdan Kondratev
- Dmitrii Chermnykh

## Problem

Many Telegram chats can be of great benefit to people.

Therefore, many people want to export chats, and publish them - so that people can read and share knowledge in this way.

For this we need a convenient tool that will not need additional actions on the part of the user.
